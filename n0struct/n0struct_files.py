import typing
from pathlib import Path
from .n0struct_utils import n0eval
from .n0struct_utils import isnumber
# ******************************************************************************
# ******************************************************************************
def load_file(file_path: str) -> str:
    with open(file_path, 'rt') as in_filehandler:
        return in_filehandler.read()
# ******************************************************************************
def load_lines(file_path: str) -> typing.Generator:
    with open(file_path, 'rt') as in_filehandler:
        while True:
            if not (line:=in_filehandler.readline()):
                break
            yield line.rstrip('\n')
# ******************************************************************************
def save_file(
                file_path: str,
                lines: typing.Union[tuple, list, dict, str],
                mode: str = 't',
                EOL: str = '\n',
                encoding: str = 'utf-8',
                equal_tag: str = "=",
):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    if isinstance(lines, (list, tuple)):
        output_buffer = EOL.join(lines)
    if isinstance(lines, dict):
        output_buffer = EOL.join([key+equal_tag+lines[key] for key in lines])
    elif isinstance(lines, str):
        output_buffer = lines
    else:
        output_buffer = str(lines)

    if 'b' in mode:
        output_buffer = output_buffer.encode(encoding)

    with open(file_path, 'w'+mode) as out_filehandler:
        out_filehandler.write(output_buffer)
# ******************************************************************************
def load_ini(
                file_path: str,
                default_value = None,
                equal_tag: str = '=',
                comment_tags: typing.Union[tuple, list] = ("#", "//"),
                parse_key: typing.Callable = lambda key_value, default_key: key_value[0].strip().upper(),
                parse_value: typing.Callable = lambda key_value, default_value:
                                                        (
                                                            round(float(stripped_value),7)
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
