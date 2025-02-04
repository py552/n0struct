import typing
from .n0struct_utils import isnumber
from .n0struct_utils import iterable
from .n0struct_files import load_lines
from .n0struct_arrays import split_pair
# ******************************************************************************
def default_parse_value(key_value, default_value):
    stripped_value = key_value[1].strip()
    if isnumber(stripped_value):
        if '.' in stripped_value:
            return round(float(stripped_value), 7)
        else:
            return int(stripped_value)
    else:
        if len(stripped_value) >=2 and (
                    ( stripped_value.startswith('"') and stripped_value.endswith('"') )
                 or ( stripped_value.startswith("'") and stripped_value.endswith("'") )
        ):
            return stripped_value[1:-1]
        else:
            return stripped_value


def parse_ini(
                lines: typing.Iterable,
                default_value = '',
                equal_tag: typing.Union[str, typing.Iterable] = '=',
                comment_tags: typing.Union[str, typing.Iterable] = ("#", "//"),
                parse_key: typing.Callable = lambda key_value, default_key: key_value[0].strip().upper(),
                parse_value: typing.Callable = default_parse_value,
                encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
                concatenate_sign: typing.Union[str, None] = '\x16',
) -> dict:
    """
        from lines:
            [
                "// Ini file",
                "KEY1 =VALUE1",
                "# KEY2=VALUE2",
                "KEY3= VALUE3",
            ]
        to dict:
            {
                'KEY1': "VALUE1",
                'KEY2': "VALUE2",
            }

    """
    result_dict = {}
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line and not any(stripped_line.startswith(comment_tag) for comment_tag in iterable(comment_tags)):
            key, value = split_pair(
                stripped_line,
                delimiter = equal_tag,
                transform_left = lambda x: parse_key((x, ''), ''),
                transform_right = lambda x: parse_value(('', x), default_value),
                default_element = 0,
                default_right = default_value
            )
            if key.endswith('+'):
                key = key[:-1]
                if key in result_dict:
                    value = f"{result_dict[key]}{value}"
                else:
                    value = f"{concatenate_sign}{value}"
            result_dict[key] = value
    return result_dict


def load_ini(
                file_path: str,
                default_value = '',
                equal_tag: typing.Union[str, typing.Iterable] = '=',
                comment_tags: typing.Union[str, typing.Iterable] = ("#", "//"),
                parse_key: typing.Callable = lambda key_value, default_key: key_value[0].strip().upper(),
                parse_value: typing.Callable = default_parse_value,
                encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
                concatenate_sign: typing.Union[str, None] = '\x16',
) -> dict:
    """
        load ini file as:
            // Ini file
            KEY1 =VALUE1
            # KEY2=VALUE2
            KEY3= VALUE3
        to dict:
            {
                'KEY1': "VALUE1",
                'KEY2': "VALUE2",
            }

    """
    return parse_ini(
                load_lines(file_path, encoding=encoding),
                default_value = default_value,
                equal_tag = equal_tag,
                comment_tags = comment_tags,
                parse_key = parse_key,
                parse_value = parse_value,
                concatenate_sign = concatenate_sign,
    )


################################################################################
__all__ = (
    'default_parse_value',
    'load_ini',
    'parse_ini',
)
################################################################################
