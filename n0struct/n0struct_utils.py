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
) -> list:
    if not buffer_str:
        return []
    return [
            process_item(item)
            for item in buffer_str.split(separator_tag)
    ]
# ******************************************************************************
def deserialize_list_of_lists(
                        buffer_str: str,
                        separator_tag: str = ";",
                        process_item = lambda item: item,
                        separator_tag_for_sublists: str = ",",
                        process_sublist = None,
) -> list:
    # Example of list of lists: list1item1,list1item2;list2item1,list2item2;list3item1,list3item2
    return deserialize_list(buffer_str, separator_tag, process_sublist or (lambda item: deserialize_list(item, separator_tag_for_sublists, process_item)))
# ******************************************************************************
def create_fixed_list(
                        buffer_str: str,
                        dst_list_len: int,
                        separator_tag: str = ";",
                        default_value: typing.Any = None,
                        process_item = lambda item: item,
) -> list:
    '''
    generate list [value1, value2, ... valueN] with size of dst_list_len
    from deserialized buffer_str
    in case of value is not existed, then [value1, default_value, ... default_value]
    '''
    return (deserialize_list(buffer_str, separator_tag, process_item) + [default_value]*dst_list_len)[0:dst_list_len]
# ******************************************************************************
def deserialize_dict(
                        buffer_str: str,
                        separator_tag: str = ";",
                        equal_tag: str = "=",
) -> dict:
    return dict(
            deserialize_list(
                buffer_str,
                separator_tag, 
                lambda item: ((key_value:=item.split(equal_tag, 1))[0], (key_value[1] if len(key_value) > 1 else ""))
            )
    ) or {}
# ******************************************************************************
def get_value_by_tag(
                        tag_name: str,
                        buffer_str: str,
                        default_value: typing.Any = None,
                        separator_tag: str = ";",
                        equal_tag: str = "=",
) -> str:
    return deserialize_dict(buffer_str, separator_tag, equal_tag).get(tag_name) or default_value
# ******************************************************************************
def validate_str(value, default_value: str = "") -> str:
    return f"{default_value if not value else value}"
# ******************************************************************************
def validate_path(value, default_value: str = "") -> str:
    if not value:
        return default_value
    if value == ".":
        return ""
    return value
# ******************************************************************************
def validate_and_map(value, variants: dict, default_value: str = ""):
    if not value:
        return default_value
    if (upper_value:=value.upper()) in variants:
        return variants[upper_value]
    return default_value
# ******************************************************************************
def validate_bool(value, default_value: False):
    return validate_and_map(
                            value,
                            {
                                "TRUE": True,
                                "YES": True,
                                "Y": True,
                                "1": True,
                            },
                            default_value
    )
# ******************************************************************************
def validate_values(value: str, possible_values_the_last_is_default: typing.Union[list, tuple], default_value: str = ""):
    if not isinstance(possible_values_the_last_is_default, (list,tuple)) and not len(possible_values_the_last_is_default):
        return default_value
    if (upper_value:=(value or "").upper()) in possible_values_the_last_is_default:
        return upper_value
    return possible_values_the_last_is_default[-1]
# ******************************************************************************
# ******************************************************************************
