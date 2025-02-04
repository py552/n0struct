# Because of load_ini(...) uses walrus operator inside comprehensions, it was moved into separate module n0struct_comprehensions.
# It will be imported only for Python 3.8+, so all other modules will be fully compatibility with Python 3.7
import os
import typing
from pathlib import Path
from .n0struct_utils import n0eval
from .n0struct_utils import isnumber
# ******************************************************************************
# ******************************************************************************
def load_file(
        file_path: str,
        read_mode: str = 't',
        encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
        EOL: str = os.linesep,
) -> str:
    if 'b' in read_mode or EOL not in ('\r\n', '\n', '\r'):
        with open(file_path, f"rb{read_mode[1:]}") as in_filehandler:
            if 't' in read_mode:
                if isinstance(EOL, str):
                    EOL = EOL.encode("utf-8")
                elif not isinstance(EOL, bytes):
                    raise TypeError(f"EOL='{EOL}' could be str or bytes for read_mode='{read_mode}'")
                return in_filehandler.read().replace(EOL, b'\n').decode(encoding)
            else:
                return in_filehandler.read()
    else:
        # no newline parameter for auto decoding
        with open(file_path, f"rt{read_mode[1:]}", encoding=encoding) as in_filehandler:
            return in_filehandler.read()
# ******************************************************************************
def load_lines(
        file_path: str,
        read_mode: str = 't',
        encoding: str = "utf-8-sig",    # with possible UTF-8 BOM (Byte Order Mark)
        EOL: str = '\r\n',              # used only for read_mode == 'b'
) -> typing.Generator:
    if 'b' in read_mode or EOL not in ('\r\n', '\n', '\r'):
        if isinstance(EOL, str):
            EOL = EOL.encode("utf-8")
        elif not isinstance(EOL, bytes):
            raise TypeError(f"EOL='{EOL}' could be str or bytes for read_mode='{read_mode}'")
        for line in load_file(file_path, read_mode='b').split(EOL):
            yield line
    else:
        with open(file_path, 'rt', encoding=encoding) as in_filehandler:
            while True:
                line = in_filehandler.readline()
                if not line:
                    break
                yield line.rstrip('\r\n')   # strip \r, \n, \r\n
# ******************************************************************************
def save_file(
        file_path: str,
        output_buffer: typing.Union[str, bytes, bytearray, dict, list, tuple, typing.Generator, set, frozenset],
        mode: str = 'wt',           # or 'at' for append
        encoding: str = "utf-8",    # without UTF-8 BOM (Byte Order Mark)
        EOL: str = os.linesep,
        equal_tag: str = "=",
        convert_EOL: bool = True,
):
    if mode in ('t', 'b', 't+', 'b+'):
        mode = f"w{mode}"
    if isinstance(output_buffer, (bytes, bytearray)):
        mode = f"{mode[0]}b{mode[2:]}"

    if isinstance(output_buffer, dict):
        output_buffer = '\n'.join([f"{key}{equal_tag}{value}" for key,value in output_buffer.items()])
    elif not isinstance(output_buffer, (str, bytes, bytearray, list, tuple, typing.Generator, set, frozenset)):
        output_buffer = str(output_buffer)

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    if 'b' in mode or EOL not in ('\r\n', '\n', '\r'):
        mode = f"{mode[0]}b{mode[2:]}"
        if isinstance(output_buffer, str):
            output_buffer = output_buffer.replace('\n', EOL).encode(encoding)
        if isinstance(EOL, str):
            EOL = EOL.encode(encoding)
        out_filehandler = open(file_path, mode)
    else:
        out_filehandler = open(file_path, mode, encoding=encoding, newline=EOL)
        EOL = '\n'

    if isinstance(output_buffer, (list, tuple, typing.Generator, set, frozenset)):
        for line in output_buffer:
            if 'b' in mode:
                if not isinstance(line, (bytes, bytearray)):
                    line = str(line).encode(encoding)
            else:
                if isinstance(line, (bytes, bytearray)):
                    line = line.decode(encoding)
                elif not isinstance(line, str):
                    line = str(line)
            out_filehandler.write(line)
            out_filehandler.write(EOL)
    else:
        out_filehandler.write(output_buffer)
    out_filehandler.close

# ******************************************************************************


def unique_file_path(file_path: str, purpose: str = "") -> Path:
    for i in range(1000):
        unique_file_path = Path(file_path)
        unique_file_ext = unique_file_path.suffix
        unique_file_path = unique_file_path.with_suffix(f".{i:03}{unique_file_ext}" if i else unique_file_ext)
        if not unique_file_path.exists():
            return unique_file_path
    else:
        raise FileExistsError("Impossible to find unique name for {purpose}'{file_path}'")


################################################################################
__all__ = (
    'load_file',
    'load_lines',
    'save_file',
    'unique_file_path',
)
################################################################################
