import typing
from .n0struct_logging import (
    n0print,
    n0debug,
    n0debug_calc,
    n0error,
)
# ******************************************************************************
# ******************************************************************************
def to_int(value: str, max_len: typing.Union[int, None] = None, default_value: typing.Any = None) -> typing.Any:
    if isnumber(value, max_len):
        return int(value)
    else:
        return default_value
def isnumber(value: str, max_len: typing.Union[int, None] = None) -> bool:
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, str):
        return False
    value = value.strip()
    if value.startswith('+') or value.startswith('-'):
        value = value[1:].strip()
    if max_len and len(value) > max_len:
        return False
    if value.count('.') == 1:
        value = value.replace('.','0')
    return value.isnumeric()
def n0isnumeric(value: str) -> bool:
    return isnumber(value, 12)
# ******************************************************************************
def get_key_by_value(dict_: dict, value_: typing.Any):
    """
    :param dict_:
    :param value_:
    :return: last key which is associated with value_ in dict_
    """
    return {value: key for key, value in dict_.items()}[value_]
# ******************************************************************************
def n0eval(_str: str) -> typing.Union[int, float, typing.Any]:
    def my_split(_str: str, _delimiter: str) -> typing.List:
        return [
                (_delimiter if _delimiter != '+' and i else "") + itm.strip()
                for i, itm in enumerate(_str.split(_delimiter))
                if itm.strip()
        ]

    if not isinstance(_str, str):
        return _str

    _str = _str.replace(" ","").lower()
    if not _str:
        return _str     # better to raise ValueError("Could not convert empty/null string into index")

    first_split = my_split(_str, '+')
    second_split = []
    for item in first_split:
        items = my_split(item, '-')
        second_split.extend(items)

    result = 0
    for item in second_split:
        if item == "new()":
            return _str
        if item == "last()":
            item = -1
        else:
            try:
                if '.' in item:
                    item = float(item)
                else:
                    item = int(item)
            except Exception:
                return _str
        result += item

    return result
# ******************************************************************************
def raise_in_lambda(ex): raise ex
# ******************************************************************************
def deserialize_list(
                        buffer_str: str,
                        delimiter: str = ";",
                        parse_item = lambda item, item_index, separated_items, previous_items: item,
                        parse_empty = False,
                        default_list_result = None,
) -> list:
    '''
        buffer_str = "ITEM1;ITEM2;ITEM3"
        deserialize_list_of_lists(buffer_str) == ["ITEM1", "ITEM2", "ITEM3"]
    '''
    if not isinstance(buffer_str, str):
        return default_list_result or []

    separated_items = buffer_str.split(delimiter)
    deserialized_list = []
    for item_index, item in enumerate(separated_items):
        if item or parse_empty:
            parsed_item = parse_item(item, item_index = item_index, separated_items = separated_items, previous_items = deserialized_list)
            deserialized_list.append(parsed_item)
    return deserialized_list
# ******************************************************************************
def deserialize_key_value(
                        buffer_str: str,
                        equal_tag: str = "=",
                        parse_key: typing.Callable = lambda key_value, default_key: key_value[0],
# Sample of calling:
#   default_key(key_value, parsed_value)
# Sample of definition:
#   lambda key_value, parsed_value: parsed_value.get('SQL_FILE') if isinstance(parsed_value, dict) else key_value
                        default_key: typing.Union[typing.Callable, typing.Any, None] = None,

                        parse_value: typing.Callable = lambda key_value, default_value: key_value[1],
# Sample of calling:
#   default_value(key_value, parsed_key)
# Sample of definition:
#   lambda key_value, parsed_key: key_value
                        default_value: typing.Union[typing.Callable, typing.Any, None] = None,
                        default_tuple_result = None,
) -> tuple:
    '''
        buffer_str = "TAG1=VALUE1"
        deserialize_key_value(buffer_str) == ("TAG1", "VALUE1")
        buffer_str = "TAG1"
        deserialize_key_value(buffer_str) == ("TAG1", None)
        buffer_str = "VALUE1"
        deserialize_key_value(buffer_str, default_key = "TAG1") == ("TAG1", "VALUE1")
    '''
    if not isinstance(buffer_str, str):
        return default_tuple_result or tuple()

    key_value = buffer_str.split(equal_tag, 1)

    parsed_key = None
    parsed_value = None
    if len(key_value) < 2:
        if default_key:
            # key_value == (single_item) -> {default_key: single_item}
            key_value = (
                            default_key((key_value[0], None), key_value[0]) if callable(default_key) else default_key,       # parsed_key
                            key_value[0]
            )
            # Skip more one manipulation with the key, because of it's already default
            parse_key = lambda key_value, default_key: key_value[0]
        else:
            # key_value == (single_item) -> {single_item: default_value}
            key_value = (
                            key_value[0],
                            default_value((None, key_value[0]), key_value[0]) if callable(default_value) else default_value  # parsed_value
            )
            # Skip more one manipulation with the value, because of it's already default
            parse_value = lambda key_value, default_value: key_value[1]
    parsed_key = parse_key(key_value, (default_key(key_value, key_value[1]) if callable(default_key) else default_key) )
    parsed_value = parse_value(key_value, default_value(key_value, parsed_key) if callable(default_value) else default_value)

    return parsed_key, parsed_value
# ******************************************************************************
def deserialize_dict(
                        buffer_str: str,
                        delimiter: str = ";",
# Sample of definition:
#   parse_item = lambda item, item_index, separated_items, previous_items: item
                        parse_item: typing.Union[typing.Callable, None] = None,
                        parse_empty = False,
                        equal_tag: str = "=",
                        parse_key: typing.Callable = lambda key_value, default_key: key_value[0],
                        default_key: typing.Any = None,
                        parse_value: typing.Callable = lambda key_value, default_value: key_value[1],
                        default_value: typing.Any = None,
                        default_dict_result = None,
                        default_list_result = None,
                        default_tuple_result = None,
) -> dict:
    '''
        buffer_str = "TAG1=VALUE1;TAG2=VALUE2"
        deserialize_dict(buffer_str) == {"TAG1": "VALUE1", "TAG2": "VALUE2"}
    '''
    deserialized_list = deserialize_list(
                            buffer_str,
                            delimiter,
                            parse_item = parse_item or (
                                            lambda item, item_index, separated_items, previous_items:
                                                deserialize_key_value(
                                                    item,
                                                    equal_tag = equal_tag,
                                                    parse_key = parse_key,
                                                    default_key = default_key,
                                                    parse_value = parse_value,
                                                    default_value = default_value,
                                                )
                                         )
                            ,
                            parse_empty = parse_empty,
    )
    deserialized_dict = dict(deserialized_list)
    return deserialized_dict
# ******************************************************************************
def get_value_by_tag(
                        tag_name: str,
                        buffer_str: str,
                        delimiter: str = ";",
                        equal_tag: str = "=",
                        parse_key: typing.Callable = lambda key_value, default_key: key_value[0],
                        default_key: typing.Any = None,
                        parse_value: typing.Callable = lambda key_value, default_value: key_value[1],
                        default_value: typing.Any = None,
) -> str:
    '''
        buffer_str = "TAG1=VALUE1;TAG2=VALUE2"
        get_value_by_tag("TAG1", buffer_str) == "VALUE1"
        get_value_by_tag("TAG2", buffer_str) == "VALUE2"
        get_value_by_tag("TAG3", buffer_str) == None
        get_value_by_tag("TAG3", buffer_str, default_value = "VALUE3") == "VALUE3"
    '''
    deserialized_dict = deserialize_dict(
                        buffer_str,
                        delimiter = delimiter,
                        equal_tag = equal_tag,
                        parse_key = parse_key,
                        default_key = default_key,
                        parse_value = parse_value,
                        default_value = default_value,  # default VALUE will be assosiated with KEY,
                                                        # in case of only the KEY is in serialized list
                        default_dict_result = {},
    )
    value_by_tag = deserialized_dict.get(tag_name)
    return value_by_tag or default_value  # default VALUE will returned, in case of VALUE is None or "" assosiated with KEY
# ******************************************************************************
def deserialize_list_of_lists(
                        buffer_str: str,
                        delimiter: str = ";",
                        parse_item = lambda item, item_index, separated_items, previous_items: item,
                        delimiter_for_sublists: str = ",",
                        parse_sublist = None,
                        parse_empty = False,
                        default_list_result = None,
) -> list:
    '''
        buffer_str = "list1item1,list1item2;list2item1,list2item2;list3item1,list3item2"
        deserialize_list_of_lists(buffer_str) == [
                                                    ["list1item1", "list1item2"],
                                                    ["list2item1", "list2item2"],
                                                    ["list3item1", "list3item2"]
                                                 ]
    '''
    deserialized_list_of_list = deserialize_list(
                            buffer_str,
                            delimiter = delimiter,
                            parse_item = parse_sublist or (
                                            lambda item, item_index, separated_items, previous_items:
                                                deserialize_list(
                                                    item,
                                                    delimiter = delimiter_for_sublists,
                                                    parse_item = parse_item,
                                                    default_list_result = default_list_result,
                                                )
                                         )
                            ,
                            parse_empty = parse_empty,
                            default_list_result = default_list_result,
    )
    return deserialized_list_of_list
# ******************************************************************************
def deserialize_fixed_list(
                        buffer_str: str,
                        fixed_list_len: int,
                        delimiter: str = ";",
                        default_item: typing.Any = None,
                        parse_item = lambda item, item_index, separated_items, previous_items: item,
                        parse_empty = False,
                        default_list_result = None,
) -> list:
    '''
    generate list [value1, value2, ... value[fixed_list_len]] with size of fixed_list_len from deserialized buffer_str
    in case of values are not enough to fill fixed_list_len list, then [value1, default_item, ... default_item]
        buffer_str = "TAG1;TAG2"
        deserialize_fixed_list(buffer_str, 2) == ("TAG1", "TAG2")
        deserialize_fixed_list(buffer_str, 4) == ("TAG1", "TAG2", None, None)
        deserialize_fixed_list(buffer_str, 4, default_item = "DEFAULT_TAG") == ("TAG1", "TAG2", "DEFAULT_TAG", "DEFAULT_TAG")
    '''
    deserialized_fixed_list = (
        deserialize_list(
            buffer_str,
            delimiter = delimiter,
            parse_item = parse_item,
            parse_empty = parse_empty,
            default_list_result = default_list_result,
        )
        + [default_item]*fixed_list_len
    )[0:fixed_list_len]
    return deserialized_fixed_list
# ******************************************************************************
def validate_str(
                    value,
                    default_value: str = "",
                    parse_str = lambda item: str(item),
) -> str:
    '''
        value = ""
        validate_str(value) == ""
        value = "C:\\TMP"
        validate_path(value) == "C:\\TMP"
        value = ""
        validate_path(value, default_value = "C:\\ETC") == "C:\\ETC"
        value = "."
        validate_path(value, default_value = "C:\\ETC") == ""
    '''
    return default_value if not value else parse_str(str)
# ******************************************************************************
def validate_path(
                    value,
                    default_value: str = "",
                    parse_str = lambda item: item,
) -> str:
    '''
        value = ""
        validate_path(value) == ""
        value = "C:\\TMP"
        validate_path(value) == "C:\\TMP"
        value = ""
        validate_path(value, default_value = "C:\\ETC") == "C:\\ETC"
        value = "."
        validate_path(value, default_value = "C:\\ETC") == ""
    '''
    if not value:
        return default_value
    if value == ".":
        return ""
    return parse_str(value)
# ******************************************************************************
def validate_bool(
                    value,
                    unknown_value_is: bool = False
):
    '''
        value = "TRUE"
        validate_bool(value) == True
        value = "YES"
        validate_bool(value) == True
        value = "FALSE"
        validate_bool(value) == False
        value = "NO"
        validate_bool(value) == False
        value = "UNKNOWN"
        validate_bool(value) == False
    '''
    return {
        "TRUE":     True,
        "T":        True,
        "YES":      True,
        "Y":        True,
        "1":        True,
        True:       True,
        1:          True,
        "FALSE":    False,
        "F":        False,
        "NO":       False,
        "N":        False,
        "0":        False,
        False:      False,
        0:          False,
    }.get(value.upper() if isinstance(value, str) else value, unknown_value_is)
# ******************************************************************************
def validate_values(value: str,
                    possible_values_the_last_is_default: typing.Union[list, tuple],
                    return_if_wrong_input: typing.Any = "",
                    raise_if_not_found: typing.Union[Exception, None] = None
):
    '''
        value = "A"
        validate_values(value.upper(), ("A", "B", "C")) == "A"
        value = "c"
        validate_values(value.upper(), ("A", "B", "C")) == "C"
        value = "D"
        validate_values(value.upper(), ("A", "B", "C")) == "C"
    '''
    if not isinstance(possible_values_the_last_is_default, (list, tuple)) or not possible_values_the_last_is_default:
        return return_if_wrong_input
    if value in possible_values_the_last_is_default:
        return value
    if isinstance(raise_if_not_found, Exception):
        raise raise_if_not_found
    return possible_values_the_last_is_default[-1]
# ******************************************************************************
def raise_exception(ex: Exception):
    raise ex
# ******************************************************************************
def catch_exception(func: callable, result_in_case_of_exception: typing.Any = None, **kw):
    """
    args == tuple, kw == mapping(dictionary)

    * == convert from tuple into list of arguments
    ** == convert from mapping into list of named arguments

    :param args:
    :param kw:
        result:typing.Any => if defined, return {result} in case of no exception
    """
    try:
        result = func()
        if "result" in kw:
            result = kw.get("result")
        return result
    except Exception:
        return result_in_case_of_exception
# ******************************************************************************
# ******************************************************************************
