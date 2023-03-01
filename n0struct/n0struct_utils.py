import typing
# ******************************************************************************
# ******************************************************************************
def n0isnumeric(value: str) -> bool:
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, str):
        return False
    value = value.strip()
    if value.startswith('+') or value.startswith('-'):
        value = value[1:].strip()
    if len(value) > 10:
        return False
    if value.count('.') == 1:
        value = value.replace('.','0')
    return value.isnumeric()
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
    def my_split(_str: str, _separator: str) -> typing.List:
        return [
                (_separator if _separator != '+' and i else "") + itm.strip()
                for i, itm in enumerate(_str.split(_separator))
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
                        separator_tag: str = ";",
                        process_item = lambda item: item,
                        process_empty = False,
) -> list:
    '''
        buffer_str = "ITEM1;ITEM2;ITEM3"
        deserialize_list_of_lists(buffer_str) == ["ITEM1", "ITEM2", "ITEM3"]
    '''
    if not buffer_str:
        return []
    return [
            process_item(item)
            for item in buffer_str.split(separator_tag)
            if item or process_empty
    ]
# ******************************************************************************
def deserialize_list_of_lists(
                        buffer_str: str,
                        separator_tag: str = ";",
                        process_item = lambda item: item,
                        separator_tag_for_sublists: str = ",",
                        process_sublist = None,
                        process_empty = False,
) -> list:
    '''
        buffer_str = "list1item1,list1item2;list2item1,list2item2;list3item1,list3item2"
        deserialize_list_of_lists(buffer_str) == [
                                                    ["list1item1", "list1item2"],
                                                    ["list2item1", "list2item2"],
                                                    ["list3item1", "list3item2"]
                                                 ]
    '''
    return deserialize_list(
                            buffer_str,
                            separator_tag = separator_tag,
                            process_item = process_sublist or (lambda item: deserialize_list(item, separator_tag_for_sublists, process_item)),
                            process_empty = process_empty,
    )
# ******************************************************************************
def create_fixed_list(
                        buffer_str: str,
                        dst_list_len: int,
                        separator_tag: str = ";",
                        default_value: typing.Any = None,
                        process_item = lambda item: item,
                        process_empty = False
) -> list:
    '''
    generate list [value1, value2, ... value[dst_list_len]] with size of dst_list_len from deserialized buffer_str
    in case of values are not enough to fill dst_list_len list, then [value1, default_value, ... default_value]
        buffer_str = "TAG1;TAG2"
        create_fixed_list(buffer_str, 2) == ("TAG1", "TAG2")
        create_fixed_list(buffer_str, 4) == ("TAG1", "TAG2", None, None)
        create_fixed_list(buffer_str, 4, default_value = "DEFAULT_TAG") == ("TAG1", "TAG2", "DEFAULT_TAG", "DEFAULT_TAG")
    '''
    return (
        deserialize_list(
            buffer_str,
            separator_tag = separator_tag,
            process_item = process_item,
            process_empty = process_empty,
        )
        + [default_value]*dst_list_len
    )[0:dst_list_len]
# ******************************************************************************
def deserialize_key_value(
                        buffer_str: str,
                        equal_tag: str = "=",
                        process_key: typing.Callable = lambda item: item,
                        process_value: typing.Callable = lambda item: item,
                        default_value: typing.Any = None,
                        default_key: typing.Any = None,
) -> tuple:
    '''
        buffer_str = "TAG1=VALUE1"
        deserialize_key_value(buffer_str) == ("TAG1", "VALUE1")
        buffer_str = "TAG1"
        deserialize_key_value(buffer_str) == ("TAG1", None)
        buffer_str = "VALUE1"
        deserialize_key_value(buffer_str, default_key = "TAG1") == ("TAG1", "VALUE1")
    '''
    key_value = buffer_str.split(equal_tag, 1)
    if default_key is not None and len(key_value) < 2:
        return default_key, process_value(key_value[0])
    else:
        return process_key(key_value[0]), process_value(key_value[1]) if len(key_value) > 1 else default_value
# ******************************************************************************
def deserialize_dict(
                        buffer_str: str,
                        separator_tag: str = ";",
                        equal_tag: str = "=",
                        process_key: typing.Callable = lambda item: item,
                        process_value: typing.Callable = lambda item: item,
                        default_value: typing.Any = None,
                        default_key: typing.Any = None,
) -> dict:
    '''
        buffer_str = "TAG1=VALUE1;TAG2=VALUE2"
        deserialize_dict(buffer_str) == {"TAG1": "VALUE1", "TAG2": "VALUE2"}
    '''
    return dict(
            deserialize_list(
                buffer_str,
                separator_tag,
                process_item = lambda item: deserialize_key_value(
                                                    item,
                                                    equal_tag = equal_tag,
                                                    process_key = process_key,
                                                    process_value = process_value,
                                                    default_value = default_value,
                                                    default_key = default_key,
                                                 ),
                # lambda item: (
                                # process_key((key_value:=item.split(equal_tag, 1))[0]),
                                # process_value(key_value[1] if len(key_value) > 1 else default_value)
                # )
            )
    )
# ******************************************************************************
def get_value_by_tag(
                        tag_name: str,
                        buffer_str: str,
                        separator_tag: str = ";",
                        equal_tag: str = "=",
                        process_key: typing.Callable = lambda item: item,
                        process_value: typing.Callable = lambda item: item,
                        default_value: typing.Any = None,
                        default_key: typing.Any = None,

) -> str:
    '''
        buffer_str = "TAG1=VALUE1;TAG2=VALUE2"
        get_value_by_tag("TAG1", buffer_str) == "VALUE1"
        get_value_by_tag("TAG2", buffer_str) == "VALUE2"
        get_value_by_tag("TAG3", buffer_str) == None
        get_value_by_tag("TAG3", buffer_str, default_value = "VALUE3") == "VALUE3"
    '''
    return deserialize_dict(
                        buffer_str,
                        separator_tag = separator_tag,
                        equal_tag = equal_tag,
                        process_key = process_key,
                        process_value = process_value,
                        default_value = default_value,  # default VALUE will assosiated with KEY, in case of only KEY is in serialized list
                        default_key = default_key,
    ).get(tag_name) or default_value  # default VALUE will returned, in case of VALUE is None or "" assosiated with KEY
# ******************************************************************************
def validate_str(
                    value,
                    default_value: str = "",
                    process_str = lambda item: str(item),
) -> str:
    '''
        value = ""
        validate_str(value) == ""
        value = "C:\TMP"
        validate_path(value) == "C:\TMP"
        value = ""
        validate_path(value, default_value = "C:\ETC") == "C:\ETC"
        value = "."
        validate_path(value, default_value = "C:\ETC") == ""
    '''
    return default_value if not value else process_str(str)
# ******************************************************************************
def validate_path(
                    value,
                    default_value: str = "",
                    process_str = lambda item: item,
) -> str:
    '''
        value = ""
        validate_path(value) == ""
        value = "C:\TMP"
        validate_path(value) == "C:\TMP"
        value = ""
        validate_path(value, default_value = "C:\ETC") == "C:\ETC"
        value = "."
        validate_path(value, default_value = "C:\ETC") == ""
    '''
    if not value:
        return default_value
    if value == ".":
        return ""
    return process_str(value)
# ******************************************************************************
def validate_and_map(
                    value,
                    variants: dict,
                    default_value: str = "",
) -> str:
    '''
        value = "A"
        validate_and_map(value.upper(), {"A":1, "B":2}, 3) == 1
        value = "B"
        validate_and_map(value.upper(), {"A":1, "B":2}, 3) == 2
        value = "C"
        validate_and_map(value.upper(), {"A":1, "B":2}, 3) == 3
    '''
    if not value:
        return default_value
    if value in variants:
        return variants[upper_value]
    return default_value
# ******************************************************************************
def validate_bool(
                    value,
                    unknown_value_is : False
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
    return validate_and_map(
                            value.upper() if isinstance(value, str) else value,
                            {
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
                            },
                            unknown_value_is
    )
# ******************************************************************************
def validate_values(value: str,
                    possible_values_the_last_is_default: typing.Union[list, tuple],
                    default_value: str = ""
):
    '''
        value = "A"
        validate_and_map(value.upper(), ("A", "B", "C")) == "A"
        value = "B"
        validate_and_map(value.upper(), ("A", "B", "C")) == "B"
        value = "D"
        validate_and_map(value.upper(), ("A", "B", "C")) == "C"
    '''
    if not isinstance(possible_values_the_last_is_default, (list, tuple)) or not possible_values_the_last_is_default:
        return default_value
    if value in possible_values_the_last_is_default:
        return value
    return possible_values_the_last_is_default[-1]
# ******************************************************************************
# ******************************************************************************
