# Python 3.8+ is required. := (walrus operator) is used in comprehension inside load_ini(...)
import typing
from .n0struct_utils import isnumber
from .n0struct_files import load_lines
# ******************************************************************************
def load_ini(
                file_path: str,
                default_value = None,
                equal_tag: str = '=',
                comment_tags: typing.Union[tuple, list] = ("#", "//"),
                parse_key: typing.Callable = lambda key_value, default_key: key_value[0].strip().upper(),
                parse_value: typing.Callable = lambda key_value, default_value:
                                                        (
                                                            round(float(stripped_value), 7)
                                                            if '.' in stripped_value
                                                            else int(stripped_value)
                                                        )
                                                        if isnumber(stripped_value:=key_value[1].strip())
                                                        else (
                                                            stripped_value[1:-1]
                                                            if len(stripped_value) >=2 and (
                                                                (stripped_value.startswith('"') and stripped_value.endswith('"'))
                                                                or (stripped_value.startswith("'") and stripped_value.endswith("'"))
                                                            ) else stripped_value
                                                        ),
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
    return {
        parse_key((key_value:=stripped_line.split(equal_tag, 1)), None): (
            parse_value(key_value, default_value)
            if len(key_value) > 1
            else default_value
        )
        for line in load_lines(file_path)
        if  (stripped_line:=line.strip())
            and not any(stripped_line.startswith(comment_tag) for comment_tag in comment_tags)
    }
# ******************************************************************************
# ******************************************************************************
