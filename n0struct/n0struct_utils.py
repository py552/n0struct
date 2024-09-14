import typing
import itertools
## from .n0struct_logging import n0debug, n0debug_calc
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
def split_with_escape(
    buffer_str: str,
    delimiter: str,
    maxsplit: typing.Union[int, None] = None, # None == no limit of splitted parts
    escape_character:str = '\\',
    trim_trailing_double_escape_characters: bool = True
):
    '''
        buffer_str = "AAAA1;BBBB2;CCCC3;DDDD4"
        split_with_escape(buffer_str) == ["ITEM1", "ITEM2", "ITEM3", "ITEM4"]

    Pay attention: '\\' is '\' in samples, because of r".." is not used:

        trim_trailing_double_escape_characters = True
        buffer_str = "\\\\IT\\EM1\\;\\\\IT\\EM2;\\ITE\\\\M3\\\\;ITE\\M4\\\\"
        split_with_escape(buffer_str) ==
            ["\\\\IT\\EM1;\\\\ITE\\M2", "\\ITE\\\\M3\\", "ITE\\M4\\"]

        trim_trailing_double_escape_characters = False
        buffer_str = "\\\\IT\\EM1\\;\\\\IT\\EM2;\\ITE\\\\M3\\\\;ITE\\M4\\\\"
        split_with_escape(buffer_str) ==
            ["\\\\IT\\EM1;\\\\ITE\\M2", "\\ITE\\\\M3\\\\", "ITE\\M4\\\\"]

        The reason of ONLY trailing escape characters: because of inside splitted parts could be subparts with termination of own unknown delimiters.
    '''
    separated_items = buffer_str.split(delimiter, maxsplit if maxsplit else -1)

    if escape_character:
        # Re-arrange list of separated_items in case of delimiter is terminated with '\'
        start_from_item = 0
        while True:
            for i,item in enumerate(separated_items[start_from_item:-1]):
                if item.endswith(escape_character):
                    count_of_trailing_escape_characters = sum( 1 for _ in itertools.takewhile(lambda ch: ch == escape_character, reversed(item)) )
                    if trim_trailing_double_escape_characters and (count_of_double_escape_characters:=count_of_trailing_escape_characters // 2):
                        # Trim double escape charaters before delimiter
                        separated_items[start_from_item+i] = item[:-count_of_double_escape_characters*2] + '\\'*count_of_double_escape_characters
                    if count_of_trailing_escape_characters % 2:
                        # Odd count_of_trailing_escape_characters, so last escape charater terminates delimiter
                        separated_items[start_from_item+i] = item[:-1] + delimiter + separated_items.pop(start_from_item+i+1)
                        if maxsplit and maxsplit+1 < len(separated_items) and delimiter in separated_items[-1]:
                            separated_items.extend(split_with_escape(separated_items.pop(-1), delimiter, 1, escape_character, trim_trailing_double_escape_characters))
                        start_from_item = start_from_item+i
                        break # repeat loop from the start_from_item, because of separated_items is changed
            else:
                if trim_trailing_double_escape_characters and separated_items[-1].endswith(escape_character):
                    count_of_trailing_escape_characters = sum( 1 for _ in itertools.takewhile(lambda ch: ch == escape_character, reversed(item)) )
                    if  (count_of_double_escape_characters:=count_of_trailing_escape_characters // 2):
                        # Trim double escape charaters of the last element, like it was done for previous elements
                        separated_items[-1] = separated_items[-1][:-count_of_double_escape_characters*2] + '\\'*count_of_double_escape_characters
                break # no more/no one trailing escape charaters found
    return separated_items
# ******************************************************************************
def unescape(in_elem: typing.Union[str, list, dict, typing.Any]) -> typing.Union[str, list, dict, typing.Any]:
    if isinstance(in_elem, str):
        return in_elem.encode().decode('unicode_escape')
    out_elem = in_elem.copy() # because of not possible to predict the complex types
    if isinstance(out_elem, list):
        for i, value in enumerate(out_elem):
            out_elem[i] = unescape(value)
    elif isinstance(out_elem, dict):
        for key, value in out_elem.items():
            out_elem[key] = unescape(value)
    return out_elem
# ******************************************************************************
def deserialize_list(
                        buffer_str: str,
                        delimiter: str = ";",
                        parse_item = lambda item, item_index, separated_items, previous_items: item,
                        parse_empty = False,
                        default_list_result = None,
                        escape_character = None,
) -> list:
    '''
        buffer_str = "ITEM1;ITEM2;ITEM3"
        deserialize_list_of_lists(buffer_str) == ["ITEM1", "ITEM2", "ITEM3"]
    '''
    if isinstance(buffer_str, (list, tuple)):
        return buffer_str
    elif not isinstance(buffer_str, str):
        return default_list_result or []

    separated_items = split_with_escape(buffer_str, delimiter, escape_character=escape_character)
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
    if isinstance(buffer_str, dict):
        return buffer_str
    elif not isinstance(buffer_str, str):
        return default_dict_result or {}

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
    return value_by_tag or default_value  # default VALUE will returned, in case of KEY is not found or VALUE is None or "" assosiated with KEY
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
    return default_value if not value else parse_str(value)
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
    if not possible_values_the_last_is_default or not isinstance(possible_values_the_last_is_default, (list, tuple)):
        if return_if_wrong_input:
            return return_if_wrong_input
        raise ValueError(f"{possible_values_the_last_is_default=} must be not empty list/tuple")

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
def key_value_list_into_dict(
    input_dict: dict,
    xpath: str,
    key_tag: str = '@DataElement',
    value_tag: str = '@Value',
    capitalize_key: int = 0,  # 0 == leave as is, -1 == lower case, 1 = upper case
    capitalize_value: int = 0,  # 0 == leave as is, -1 == lower case, 1 = upper case
) -> dict:
    '''
        input_dict = {
            xpath: [
                {"@DataElement": key1, "@Value": value1},
                {"@DataElement": key2, "@Value": value2},
            ]
        }
        ->
        output_dict = {
            key1: value1,
            key2: value2,
        }
    '''
    if not (capitalize_key:=int(capitalize_key)):
        capitalize_key = lambda s: s
    elif capitalize_key > 0:
        capitalize_key = lambda s: s.upper() if isinstance(s, str) else s
    else:
        capitalize_key = lambda s: s.lower() if isinstance(s, str) else s

    if not (capitalize_value:=int(capitalize_value)):
        capitalize_value = lambda s: s
    elif capitalize_value > 0:
        capitalize_value = lambda s: s.upper() if isinstance(s, str) else s
    else:
        capitalize_value = lambda s: s.lower() if isinstance(s, str) else s



    output_dict = {}
    for input_list in (input_dict.get(xpath) or tuple()):
        ## n0debug("input_list")
        if isinstance(input_list, (list, tuple)):
            for key_value_dict in input_list:
                ## n0debug("key_value_dict")
                if isinstance(key_value_dict, (list, tuple)):
                    for key_value_subdict in key_value_dict:
                        ## n0debug("key_value_subdict")
                        if isinstance(key_value_subdict, dict):
                            output_dict.update({capitalize_key(key_value_subdict[key_tag]): capitalize_value(key_value_subdict[value_tag])})
                        else:
                            raise TypeError(f"Expected {key_value_subdict=} as dict, but got {type(key_value_subdict)}")
                elif isinstance(key_value_dict, dict):
                    output_dict.update({capitalize_key(key_value_dict[key_tag]): capitalize_value(key_value_dict[value_tag])})
                else:
                    raise TypeError(f"Expected {key_value_dict=} as list/dict, but got {type(key_value_dict)}")
        elif isinstance(input_list, dict):
            ## n0debug("input_list")
            output_dict.update({capitalize_key(input_list[key_tag]): capitalize_value(input_list[value_tag])})
        else:
            raise TypeError(f"Expected {input_list=} as list/dict, but got {type(input_list)}")
    return output_dict


# ******************************************************************************
def merge_dict(*kw) -> dict:
    return {
        k: v
        for d in kw
            if isinstance(d, dict)
                for k, v in d.items()
    }


# ******************************************************************************
def merge_dict_first(*kw) -> dict:
    result_dict = {}
    for d in kw:
        if isinstance(d, dict):
            result_dict.update({k: v  for k, v in d.items() if k not in result_dict})
    return result_dict


# ******************************************************************************
def merge_dict_concatenate(
    *kw,
    # /,
    concatenate_sign: typing.Union[str, None] = '\x16',
    finalize_dict_concatenate: bool = False,
) -> dict:
    ## n0debug("concatenate_sign")
    ## n0debug("finalize_dict_concatenate")
    result_dict = {}
    for d in kw:
        ## n0debug("d")
        if isinstance(d, dict):
            result_dict.update(
                {
                    k:
                        f"{old_v}{v[1:]}"
                        if v.startswith(concatenate_sign) and ((old_v:=result_dict.get(k) or '') or finalize_dict_concatenate)
                        else v
                    for k, v in d.items()
                }
            )
    return result_dict


# ******************************************************************************
def finalize_dict_concatenate(
    input_dict: dict,
    concatenate_sign: typing.Union[str, None] = '\x16',
) -> dict:
    for k, v in d.items():
        if v.startswith(concatenate_sign):
            input_dict[k] = v[1:]
    return input_dict


# ******************************************************************************
def remove_void_elements(
    structure: typing.Union[list, dict],
    remove_empty_arrays: bool = False,
    remove_empty_strings: bool = False,
    xpath: str = "/",
    level: int = 0,
    remove_empty_elements: set = {},
) -> typing.Union[list, dict]:
    if isinstance(structure, list):
        index = len(structure)
        while index:
            index -= 1
            value = structure[index]
            element_xpath = f"{xpath}[{index}]"
            if value is None:
                structure.pop(index)
            elif not value:
                if remove_empty_elements and element_xpath in remove_empty_elements:
                    structure.pop(index)
                elif isinstance(value, str) and remove_empty_strings:
                    structure.pop(index)
                elif isinstance(value, (list, dict)) and remove_empty_arrays:
                    structure.pop(index)
            else:
                if isinstance(value, (list, dict)):
                    remove_void_elements(value, remove_empty_arrays, remove_empty_strings, element_xpath, level+1)
    elif isinstance(structure, dict):
        for key in tuple(structure.keys()):
            value = structure[key]
            element_xpath =f"{xpath}/{key}"
            if value is None:
                structure.pop(key)
            elif not value:
                if remove_empty_elements and element_xpath in remove_empty_elements:
                    structure.pop(key)
                elif isinstance(value, str) and remove_empty_strings:
                    structure.pop(key)
                elif isinstance(value, (list, dict)) and remove_empty_arrays:
                    structure.pop(key)
            else:
                if isinstance(value, (list, dict)):
                    remove_void_elements(value, remove_empty_arrays, remove_empty_strings, element_xpath, level+1)
    return structure


# ******************************************************************************
from collections.abc import Iterable
def iterable(obj):
    '''
        "abc"   -> ["abc"]
        ["abc"] -> ["abc"]
    '''
    if not isinstance(obj, str) and isinstance(obj, Iterable):
        yield from obj
    else:
        yield obj


def isiterable(obj, item_type = str):
    return isinstance(obj, item_type) or isinstance(obj, Iterable)


# ******************************************************************************
# https://code.activestate.com/recipes/577504/
# from __future__ import print_function
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    ##### Example call #####
        d = dict(a=1, b=2, c=3, d=[4,5,6,7], e='a string of chars')
        print(total_size(d, verbose=True))
    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


# ******************************************************************************
def serialize_dict(
    input_dict: str,
    delimiter: str = ";",
    equal_tag: str = "=",
    generate_empty = True,
    generate_none = True,
    capitalize_key: int = 0,  # 0 == leave as is, -1 == lower case, 1 = upper case
    capitalize_value: int = 0,  # 0 == leave as is, -1 == lower case, 1 = upper case
    level: int = 0,
) -> str:
    '''
        serialize_dict({"TAG1": "VALUE1", "TAG2": "VALUE2"}) == "TAG1=VALUE1;TAG2=VALUE2"
    '''
    if input_dict is None:
        return None

    buffer_str = ""

    if not isinstance(input_dict, (dict, list, tuple, set, frozenset)):
        in_buffer_str = str(input_dict)
        if (capitalize_value:=int(capitalize_value)) > 0:
            in_buffer_str = in_buffer_str.upper()
        elif capitalize_value < 0:
            in_buffer_str = in_buffer_str.lower()

        dangerous_characters = "{}[]\"\\" + delimiter + equal_tag
        for ch in in_buffer_str:
            if ch in dangerous_characters:
                buffer_str += f"\\x{ord(ch):x}"
            else:
                buffer_str += ch

        ## n0debug("buffer_str")
        return buffer_str


    if not (capitalize_key:=int(capitalize_key)):
        capitalize_key = lambda s: s
    elif capitalize_key > 0:
        capitalize_key = lambda s: s.upper() if isinstance(s, str) else s
    else:
        capitalize_key = lambda s: s.lower() if isinstance(s, str) else s

    if isinstance(input_dict, dict):
        for key,value in input_dict.items():
            if buffer_str:
                buffer_str += delimiter
            elif level:
                buffer_str += "{"

            serialized_value = serialize_dict(value, delimiter, equal_tag, generate_empty, generate_none, capitalize_key, capitalize_value, level+1)

            buffer_str += capitalize_key(key)
            if not serialized_value:
                if serialized_value is None and generate_none:
                    buffer_str += equal_tag
                elif generate_empty:
                    buffer_str += equal_tag
            else:
                buffer_str += equal_tag + serialized_value

        if buffer_str and level:
            buffer_str += "}"
    else:
        for value in input_dict:
            if buffer_str:
                buffer_str += delimiter
            elif level:
                buffer_str += "["
            buffer_str += serialize_dict(value, delimiter, equal_tag, generate_empty, generate_none, capitalize_key, capitalize_value, level+1)
        if buffer_str and level:
            buffer_str += "]"

    return buffer_str
# ******************************************************************************
# ******************************************************************************
################################################################################
__all__ = (
    'to_int',
    'isnumber',
    'n0isnumeric',
    'get_key_by_value',
    'n0eval',
    'raise_in_lambda',
    'split_with_escape',
    'unescape',
    'deserialize_list',
    'deserialize_key_value',
    'deserialize_dict',
    'get_value_by_tag',
    'deserialize_list_of_lists',
    'deserialize_fixed_list',
    'validate_str',
    'validate_path',
    'validate_bool',
    'validate_values',
    'raise_exception',
    'catch_exception',
    'key_value_list_into_dict',
    'merge_dict',
    'merge_dict_first',
    'merge_dict_concatenate',
    'remove_void_elements',
    'iterable',
    'isiterable',
    'total_size',
    'serialize_dict',
)
################################################################################
