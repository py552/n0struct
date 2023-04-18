import typing
# ******************************************************************************
# ******************************************************************************
def split_pair(
                in_str: str,
                delimiter: str,
                transform_left: callable = lambda x:x,
                transform_right: callable = lambda x:x,
                default_element: int = 1,
                default_left: typing.Any = None,
                default_right: typing.Any = None,
) -> tuple:
    """
    split_pair(in_str: str, delimiter: str, transform_left: callable = lambda x:x, transform_right: callable = lambda x:x, default_element: int = 1) -> tuple:

    split string into 2 sub strings in any cases:
        '' by '://'                                     => (default_left, default_right)
        'www.aaa.com' by '://'                          => (default_left, 'www.aaa.com')
        'https://www.aaa.com' by '://'                  => ('http', 'www.aaa.com')
        'www.aaa.com',default_element = 0 by '/'        => ('www.aaa.com')
        'www.aaa.com/path',default_element = 0 by '/'   => ('www.aaa.com', 'path')
    """
    if not in_str:
        return transform_left(default_left), transform_right(default_right)

    str_parts = in_str.split(delimiter, 1)
    if len(str_parts) == 1:
        if default_element:
            # second (right) element is default
            return transform_left(default_left), transform_right(str_parts[0])
        else:
            # first (left) element is default
            return transform_left(str_parts[0]), transform_right(default_right)
    return transform_left(str_parts[0]), transform_right(str_parts[1])
# ******************************************************************************
def join_triplets(
                    in_list: typing.Union[None, str, tuple, list],
                    level:int = 0
) -> str:
    """
    join_triplets(in_list: typing.Union[None, str, tuple, list], level = 0) -> str:

    join elements with middle sepataror:
        [elem1, delimiter, elem2]   => elem1, delimiter, elem2
        [elem1, delimiter, None]    => elem1
        [None, delimiter, elem2]    => elem2
    """
    if isinstance(in_list, str) or in_list is None:
        return in_list or ""
    elif not isinstance(in_list, (tuple, list)):
        raise TypeError(f"{type(in_list)} '{in_list}' should be None|str|tuple|list")
    elif not len(in_list):
        return ""
    elif len(in_list) > 3:
        raise TypeError(f"'{in_list}' should consist not more 3 elements")
    else:
        out_list = []
        for item in in_list:
            out_list.append(join_triplets(item, level+1))

        if len(in_list) == 3:
            if isinstance(in_list[1], str):
                result = out_list[0] +  (out_list[1] if out_list[0] and out_list[2] else "") + out_list[2]
            else:
                if not isinstance(in_list[1], (tuple, list)) or len(in_list[1]) not in (1,2):
                    raise TypeError(f"{type(in_list[1])} '{in_list[1]}' is not correct delimiter")
                if len(in_list[1]) == 2 and not in_list[1][0]:
                    result = out_list[0] +  (out_list[1] if out_list[2] else "") + out_list[2]
                else:
                    result = out_list[0] +  (out_list[1] if out_list[0] else "") + out_list[2]
        else:
            result = "".join(out_list)

        return result
# ******************************************************************************
# ******************************************************************************
