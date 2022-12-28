import typing
from pathlib import Path
import n0struct
# from .n0struct_logging import *
from .n0struct_utils import n0eval
# ******************************************************************************
# ******************************************************************************
def load_file(file_name: str) -> str:
    with open(file_name, 'rt') as in_file:
        return in_file.read()
# ******************************************************************************
def load_lines(file_name: str) -> list:
    with open(file_name, 'rt') as in_file:
        # return [line.strip() for line in in_file.read().split("\n") if line.strip()]
        while True:
            if not (line:=in_file.readline()):
                break
            yield line.rstrip('\n')
# ******************************************************************************
def save_file(file_name: str, lines: typing.Any):
    Path(file_name).parent.mkdir(parents=True, exist_ok=True)

    if isinstance(lines, (list, tuple)):
        buffer = "\n".join(lines)
    elif isinstance(lines, str):
        buffer = lines
    else:
        buffer = str(lines)
    with open(file_name, 'wt') as out_filehandler:
        out_filehandler.write(buffer)
# ******************************************************************************
def load_ini(file_name: str, default_value = None, equal_sign = '=') -> dict:
    ini_dict = {}
    for line in load_file(file_name):
        items = line.strip().split(equal_sign, 1)
        if items:
            ini_dict.update({
                            items[0].upper():   (
                                                int(items[1])
                                                if len(items) > 1 and items[1].isdecimal()
                                                else default_value
                                                )
            })
    return ini_dict
# ******************************************************************************
def load_serialized(file_name: str,
                    # /,  # When everybody migrates to py3.8, then we will make it much beautiful
                    equal_tag: str = "=",
                    separator_tag: str = ";",
                    comment_tags: typing.Union[tuple, list] = ("#", "//"),
                    remove_startswith: str = "",
                    remove_endswith: str = ""
                    # ) -> n0struct.n0list:
                    ) -> list:
    result = []
    for line in load_file(file_name):
        line = line.strip()
        if any(line.startswith(comment_tag) for comment_tag in comment_tags):
            continue
        if line.startswith(remove_startswith):
            line = line[len(remove_startswith):]
        if line.startswith(remove_startswith):
            line = line[len(remove_startswith):]

        pairs = line.split(separator_tag)
        if len(pairs):
            result.append({})
            for pair in pairs:
                if equal_tag in pair:
                    tag, value = pair.split(equal_tag, 1)
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    else:
                        value = n0eval(value)
                else:
                    tag = pair
                    value = None
                result[-1].update({tag.strip(): value})
                # result["root"][-1].update({tag.strip(): value})
    return result
# ******************************************************************************
# ******************************************************************************
