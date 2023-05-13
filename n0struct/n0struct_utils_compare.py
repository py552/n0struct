import typing
# ******************************************************************************
# ******************************************************************************
__flag_compare_check_different_types = False
def set__flag_compare_check_different_types(value: bool):
    """
    if __flag_compare_check_different_types == True, then
    validate type of attributes in .compare()/.direct_compare()
    and return result["difftypes"]
    """
    global __flag_compare_check_different_types
    __flag_compare_check_different_types = value
    return __flag_compare_check_different_types
def get__flag_compare_check_different_types() -> bool:
    global __flag_compare_check_different_types
    return __flag_compare_check_different_types
# ******************************************************************************
__flag_compare_return_difference_of_values = False
def set__flag_compare_return_difference_of_values(value: bool):
    """
    if __flag_compare_return_difference_of_values == True, then
    if values of attributes are different and are int, float,
    return additional element in result["not_equal"] with difference
    """
    global __flag_compare_return_difference_of_values
    __flag_compare_return_difference_of_values = value
def get__flag_compare_return_difference_of_values() -> bool:
    global __flag_compare_return_difference_of_values
    return __flag_compare_return_difference_of_values
# ******************************************************************************
__flag_compare_return_equal = False
def set__flag_compare_return_equal(value: bool):
    """
    if __flag_compare_return_equal == True, then
    if records are the same, 
    then return additional element in result["equal"] with equal records
    """
    global __flag_compare_return_equal
    __flag_compare_return_equal = value
def get__flag_compare_return_equal() -> bool:
    global __flag_compare_return_equal
    return __flag_compare_return_equal
# ******************************************************************************
__flag_compare_return_place = True
def set__flag_compare_return_place(value: bool):
    """
    if __flag_compare_return_place == True, then
        if record is the different, then return tupple of index and record in result["self_unique"]/result["other_unique"]
    else
        return only the record in result["self_unique"]/result["other_unique"]
    """
    global __flag_compare_return_place
    __flag_compare_return_place = value
def get__flag_compare_return_place() -> bool:
    global __flag_compare_return_place
    return __flag_compare_return_place
# ******************************************************************************
# xpath_match(xpath: str, xpath_list):
#   Check that real xpath (or xpath like) is equal any of xpath_list[0..n].
#   Returns i+1
# ******************************************************************************
def xpath_match(xpath: str, xpath_list: typing.Union[str, list, tuple]) -> int:
    """
    :param xpath:
        xpath: str
    :param xpath_list:
        xpath_list: str or list|tuple
    :return:
         0 not matched any of xpath_list
        >0 matched
    """
    if isinstance(xpath_list, str):
        xpath_list = [xpath_list]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
    if not isinstance(xpath_list, (tuple, list)):
        raise TypeError(f"xpath_match(..): unknown type of xpath_list = {type(xpath_list)}")

    xpath_parts = xpath.split("/")
    for i, xpath_itm in enumerate(xpath_list):
        xpath_itm_parts = xpath_itm.split("/")
        for j, part in enumerate(reversed(xpath_itm_parts)):
            if not part:  # //
                return i + 1    # MATCH: matched relative
            if j >= len(xpath_parts):
                break           # not matched: too short
            if part != "*" and part.lower() != xpath_parts[-1 - j].lower():  # /*/
                break           # not matched: not equal
        else:
            return i + 1        # MATCH: matched full
        # Let's try new loop
    return 0                    # not matched: not matched with all from list
# ******************************************************************************
def generate_composite_keys(
                            input_list: list,
                            elements_for_composite_key: tuple,
                            prefix: str = None,
                            transform: typing.List[typing.Tuple[str, typing.Callable[[str], str]]] = []
                            ) -> list:
    """
    serialization all or {elements_for_composite_key} elements of {input_list[]}
    :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
    :return:
        [[<composite_key>,[<index of entry>],...}
    """
    if isinstance(elements_for_composite_key, str):
        elements_for_composite_key = [elements_for_composite_key]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A

    composite_keys_for_all_lines = []
    if transform:
        attributes_to_transform = [itm[0] for itm in transform]
    else:
        attributes_to_transform = []

    for line_i, line in enumerate(input_list):
        if isinstance(line, dict):
            created_composite_key = ""
            if elements_for_composite_key:
                for key in elements_for_composite_key:
                    if key in line:
                        if created_composite_key:
                            created_composite_key += ";"
                        fullxpath = f"{prefix}/{key}"
                        transform_i = xpath_match(fullxpath, attributes_to_transform)
                        if transform_i:
                            transform_i -= 1
                            tranformed = transform[transform_i][1](line[key])
                        else:
                            tranformed = str(line[key])
                        created_composite_key += key + "=" + tranformed
        else:
            raise TypeError(f"generate_composite_keys(..): expected element dict inside list, but got ({type(line)}){line}")
        composite_keys_for_all_lines.append((created_composite_key, line_i))
    return composite_keys_for_all_lines
# ******************************************************************************
# ******************************************************************************
