import typing
from urllib.parse import unquote as urllib__parse__unquote
# ******************************************************************************
# ******************************************************************************
def split_name_index(node_name: str) -> typing.Tuple[
                                                        str,
                                                        typing.Union[
                                                            str,
                                                            typing.Tuple[str, str, typing.Union[str, bool]]
                                                        ]
                                                    ]:
    if not isinstance(node_name, str):
        raise TypeError("node_name (%s)%s must be string" % (type(node_name), node_name))

    node_index_tuple = None
    if '[' in node_name and node_name.endswith(']'):
        node_name, node_index_str = node_name[:-1].split('[', 1)
        node_name = node_name.strip()
        node_index_str = node_index_str.strip()
        if node_index_str:
            if node_index_str.lower().startswith('contains') and node_index_str.endswith(')'):
                node_index_part1, node_index_part2 = node_index_str[8:-1].strip().split('(',1)[1].split(',',1)
                if node_index_part1.lower().startswith('text'):
                    node_index_str = "text()~~" + node_index_part2
            if '=' in node_index_str or '~' in node_index_str:
                separators = ("==","!=","~~","!~","~","=")
                for separator in separators:
                    if separator in node_index_str:
                        expected_node_name, expected_value = node_index_str.split(separator,1)
                        expected_node_name = expected_node_name.strip()
                        expected_value = expected_value.strip()
                        if separator == '=':
                            separator = '=='
                        if separator == '~':
                            separator = '~~'
                        break
                else:
                    raise SyntaxError(f"Not expected condition in index [{node_index_str}]")

                expected_value_bool = False  # Default value, in real None was used, but mypy raised error
                if expected_value.lower() == "true()":
                    expected_value = ""
                    expected_value_bool = True
                elif expected_value.lower() == "false()":
                    expected_value = ""
                    expected_value_bool = False
                elif (expected_value.startswith('"') and expected_value.endswith('"')) or \
                        (expected_value.startswith("'") and expected_value.endswith("'")):
                    expected_value = expected_value[1:-1]
                    expected_value = urllib__parse__unquote(expected_value)
                node_index_tuple = (expected_node_name, separator, expected_value or expected_value_bool)
    else:
        node_index_str = None
    return node_name, (node_index_tuple if node_index_tuple is not None else node_index_str)
# ******************************************************************************
# notemptyitems(item):
#   Check item or recursively subitems of item.
#   Return count of notempty item/subitems.
# ******************************************************************************
def notemptyitems(item):
    not_empty_items_count = 0
    # if isinstance(item, (dict, OrderedDict, n0dict)):
    if isinstance(item, dict):
        for key in item:
            not_empty_items_count += notemptyitems(item[key])
    elif isinstance(item, (list, tuple)):
        for itm in item:
            not_empty_items_count += notemptyitems(itm)
    else:
        if item:
            not_empty_items_count += 1
    return not_empty_items_count
# ******************************************************************************
# ******************************************************************************
