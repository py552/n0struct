# Because of load_ini(...) uses walrus operator inside comprehensions, it was moved into separate module n0struct_comprehensions.
# It will be imported only for Python 3.8+, so all other modules will be fully compatibility with Python 3.7
import typing
from pathlib import Path
from .n0struct_utils import n0eval
from .n0struct_utils import isnumber
# ******************************************************************************
# ******************************************************************************
def load_file(
                file_path: str,
                mode: str = 't',
                encoding: typing.Union[str, bytes] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
) -> str:
    if mode == 'b':
        encoding = None
    with open(file_path, 'r'+mode, encoding=encoding) as in_filehandler:
        return in_filehandler.read()
# ******************************************************************************
def load_lines(
                file_path: str,
                mode: str = 't',
                encoding: str = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
                EOL: str = '\n',
) -> typing.Generator:
    if mode == 'b':
        # Impossible to mix return and yield under single function
        if isinstance(EOL, str):
            EOL = bytes(EOL, encoding="utf-8")
        elif not isinstance(EOL, bytes):
            raise TypeError(f"{EOL=} could be str or bytes for {mode=}")
        for line in load_file(file_path, mode=mode, encoding=encoding).split(EOL):
            yield line
    else:
        if isinstance(EOL, bytes):
            EOL = EOL.decode("utf-8-sig")
        elif not isinstance(EOL, str):
            raise TypeError(f"{EOL=} could be str or bytes for {mode=}")
        with open(file_path, 'rt', encoding=encoding) as in_filehandler:
            while True:
                line = in_filehandler.readline()
                if not line:
                    break
                yield line.rstrip(EOL)
# ******************************************************************************
def save_file(
                file_path: str,
                lines: typing.Union[tuple, list, dict, str, bytes, bytearray],
                mode: str = 't',
                encoding: str = "utf-8",  # without UTF-8 BOM (Byte Order Mark)
                EOL: str = '\n',
                equal_tag: str = "=",
):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    if isinstance(lines, (list, tuple)):
        output_buffer = EOL.join(lines)
    if isinstance(lines, dict):
        output_buffer = EOL.join([key+equal_tag+lines[key] for key in lines])
    elif isinstance(lines, str):
        output_buffer = lines
    elif isinstance(lines, (bytes, bytearray)):
        output_buffer = lines
        mode = 'b' + ('+' if '+' in mode else '')
    else:
        output_buffer = str(lines)

    if 'b' in mode:
        if isinstance(output_buffer, str):
            output_buffer = output_buffer.encode(encoding)
        encoding = None

    with open(file_path, 'w'+mode, encoding=encoding) as out_filehandler:
        out_filehandler.write(output_buffer)
# ******************************************************************************


def unique_file_path(file_path: str, purpose: str = "") -> Path:
    for i in range(1000):
        unique_file_path = Path(str(file_path) + (f".{i:03}" if i else ""))
        if not unique_file_path.exists():
            return unique_file_path
    else:
        raise FileExistsError("Impossible to find unique name for {purpose}'{file_path}'")
# ******************************************************************************
# ******************************************************************************


