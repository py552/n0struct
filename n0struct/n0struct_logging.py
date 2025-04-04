import sys
import os
import re
import inspect
from loguru import logger
from logging import StreamHandler
import typing
from .n0struct_date import date_timestamp
# ******************************************************************************
# ******************************************************************************

_debug_show_object_type = True
def set_debug_show_object_type(debug_show_object_type: bool):
    global _debug_show_object_type
    _debug_show_object_type = debug_show_object_type

_debug_show_object_id = False
def set_debug_show_object_id(debug_show_object_id: bool):
    global _debug_show_object_id
    _debug_show_object_id = debug_show_object_id

_debug_show_item_count = True
def set_debug_show_item_count(debug_show_item_count: bool):
    global _debug_show_item_count
    _debug_show_item_count = debug_show_item_count


__main_log_filename = None
def init_logger(
    debug_level: str             = "TRACE",
    debug_output                 = sys.stderr,
    debug_timeformat: str        = "YYYY-MM-DD HH:mm:ss.SSS",
    debug_show_object_type: bool = _debug_show_object_type,
    debug_show_object_id: bool   = _debug_show_object_id,
    debug_show_item_count: bool  = _debug_show_item_count,
    debug_logtofile: bool        = False,
    log_file_name: str           = None,
):
    logger.level("DEBUG", color="<white>")  # Change default color of DEBUG messages from blue into light gray

    global __main_log_filename
    if debug_logtofile or log_file_name:
        if log_file_name:
            __main_log_filename = log_file_name
        else:
            if not __main_log_filename:
                __main_log_filename = os.path.splitext(os.path.split(inspect.stack()[-1].filename)[1])[0]
            if __main_log_filename == "<string>":
                __main_log_filename = "debuglog"
            __main_log_filename += "_" + date_timestamp() + ".log"

    set_debug_show_object_type(debug_show_object_type)
    set_debug_show_object_id(debug_show_object_id)
    set_debug_show_item_count(debug_show_item_count)

    logger_format = ""
    if debug_timeformat:
        logger_format += "<green>{time:" + debug_timeformat + "}</green> |"
    logger_format += "<level> {level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"

    handlers = [
        dict(sink = debug_output, level = debug_level, format = logger_format),
    ]
    if debug_logtofile:
        handlers.append(
            dict(sink = __main_log_filename, enqueue = True, level = debug_level, format = logger_format),
        )
    logger.configure(handlers = handlers)
# ******************************************************************************
def n0print(
    text: str,
    level: str = "INFO",
    internal_call: int = 0,
):
    """
    if {level} <= {__debug_level} then print {text}{end}

    :param text:
    :param level:
    :param end:
    :param internal_call:
    :return: None
    """
    logger.opt(depth=1+internal_call).log(level, text or "")
# ******************************************************************************
def n0info(text: str, internal_call: int = 0):
    n0print(text, level = "INFO", internal_call = internal_call + 1)
# ******************************************************************************
def n0error(text: str, internal_call: int = 0):
    n0print(text, level = "ERROR", internal_call = internal_call + 1)
# ******************************************************************************
def n0warning(text: str, internal_call: int = 0):
    n0print(text, level = "WARNING", internal_call = internal_call + 1)
# ******************************************************************************
json_control_characters = re.compile(r"[\x00-\x1F\"\\\x7F]")
python_control_characters = re.compile(r"[\x00-\x09\x0B-\x1F\"\\\x7F]")
not_ascii_characters = re.compile(r"[^\x00-\x7F]")
escaped_control_characters = {
    '\b':   '\\b',  # 0x08  Backspace
    '\t':   '\\t',  # 0x09  Tab
    '\n':   '\\n',  # 0x0A  New line
    '\f':   '\\f',  # 0x0C  Form feed
    '\r':   '\\r',  # 0x0D  Carriage return
    '\"':   '\\"',  # 0x22  Double quote
    '\\':   '\\\\', # 0x5C  Backslash
}
def replace_not_ascii_characters(match):
    return f"\\u{ord(match.group(0)):04X}"
def replace_control_characters(match):
    char = match.group(0)
    return escaped_control_characters.get(char, f"\\x{ord(char):02X}")
def n0pretty(
    item: typing.Any,
    indent_level: int       = 0,
    show_object_type: bool  = _debug_show_object_type,
    indent_size: int        = 4,
    quote: str              = '"',
    pairs_in_one_line: bool = True,
    json_convention: bool   = False,
    skip_empty_arrays: bool = False,
    skip_simple_types: bool = True,
    show_item_count: bool   = _debug_show_item_count,
):
    """
    :param item:
    :param indent_level:
    :return:
    """
    # ######################################################################
    def object_type(
        _object: typing.Any,
        _show_object_type: bool = show_object_type,
        _skip_simple_types: bool = skip_simple_types,
    ) -> str:
        if not _show_object_type or (_skip_simple_types and isinstance(_object, (str, int, float, bool, type(None), bytes))):
            return ''
        # removed walrus operator for compatibility with 3.7
        obj_type = str(type(_object)).replace("<class '", '').replace("'>", '')
        class_type_parts = obj_type.split('.')
        if len(class_type_parts) > 2:
            # leave just only first and last class names
            obj_type = '..'.join((class_type_parts[0], class_type_parts[-1]))

        return f"<{obj_type}{' '+str(len(_object)) if isinstance(_object, (str, list, tuple, set, frozenset, dict, bytes, bytearray)) else ''}> "
    # ######################################################################
    def indent(_indent_level = indent_level) -> str:
        return f"{(' ' * (_indent_level + 1) * indent_size) if indent_size else ''}"
    # ######################################################################
    def quote_value_if_str(value: typing.Any, _quote: str = quote, padding: typing.Union[str, int] = '') -> str:
        if json_convention:
            if isinstance(value, bool):
                return "true" if value else "false"
            if item is None:
                return "null"  # json.decoder.JSONDecodeError: Expecting value
        if isinstance(value, str):
            if json_convention:
                value = not_ascii_characters.sub(replace_not_ascii_characters, json_control_characters.sub(replace_control_characters, value))
            else:
                value = python_control_characters.sub(replace_control_characters, value)
                if '\n' in value:
                    _quote = _quote*3
        else:
            value = str(value)
            _quote = ''

        if padding:
            padding = ' '*(padding-len(value))

        return f"{_quote}{value}{_quote}{padding}"
    # ######################################################################
    def is_list_with_pairs(list_of_dicts: list) -> int:
        """
        Check if list contains dictionaries with pairs (2 keys in each dictionary)
        and return max len of the values for further adjustment
        """
        if not list_of_dicts or not isinstance(list_of_dicts, (list, tuple)):
            return None
        adjust_values = {}
        for item in list_of_dicts:
            if not isinstance(item, dict) or len(item) != 2:
                return None
            for key, value in item.items():
                adjust_values[key] = max(adjust_values.get(key, 0), len(str(value)))
                if len(adjust_values) > 2:
                    return None
        if len(adjust_values) != 2:
            return None
        return adjust_values
    # ######################################################################

    space = ' '
    newline = '\n' + indent()
    newline_previndent = '\n' + indent(indent_level - 1)
    if not indent_size:
        pairs_in_one_line = False
        space = ''
        newline = ''
        newline_previndent = ''
    comma_space = f",{space}"
    comma_newline = f",{newline}"
    colon_space = f":{space}"

    if isinstance(item, (list, tuple, dict, set, frozenset)):
        brackets = "[]"
        if isinstance(item, dict):
            brackets = "{}"
        if not json_convention:
            if isinstance(item, (set, frozenset)):
                brackets = "{}"
            elif isinstance(item, tuple):
                brackets = "()"


        result = ""
        # removed walrus operator for compatibility with 3.7
        keys_and_max_len_of_value = is_list_with_pairs(item)
        if pairs_in_one_line and keys_and_max_len_of_value:
            result = comma_newline.join(
                '{' + # 3.7 doesn't support {{
                f"{comma_space.join(f'{quote_value_if_str(k)}{colon_space}{quote_value_if_str(v, padding = keys_and_max_len_of_value[k])}' for k, v in _dict.items())}" +
                '}'   # 3.7 doesn't support }}
                for _dict in item
            )
        else:
            # dict, set, frozenset or list/tuple with complex or not paired structure
            len_item = len(item)
            possible_condense_dict_into_one_line = \
                isinstance(item, dict) \
                and len_item <= 2 \
                and all(
                    isinstance(sub_item, str)
                    for sub_item in item.values()
                )

            for i_sub_item, sub_item in enumerate(item):
                if isinstance(item, dict):
                    key = sub_item
                    sub_item = item[key]
                    sub_item_value = "{.......}"
                else:
                    sub_item_value = "[.......]"

                if indent_level < 111:
                    sub_item_value = n0pretty(
                        sub_item,
                        indent_level + 1,
                        show_object_type  = show_object_type,
                        indent_size       = indent_size,
                        quote             = quote,
                        pairs_in_one_line = pairs_in_one_line,
                        json_convention   = json_convention,
                        skip_empty_arrays = skip_empty_arrays,
                        skip_simple_types = skip_simple_types,
                        show_item_count   = show_item_count,
                    )

                    if isinstance(item, dict):
                        sub_item_value = f"{quote_value_if_str(key)}{colon_space}{sub_item_value}"
                    else:
                        if show_item_count:
                            sub_item_value = f"#{i_sub_item:<3} {sub_item_value}"

                result = f"{result}{(comma_newline if not possible_condense_dict_into_one_line else comma_space) if result else ''}{sub_item_value}"

        result_type = object_type(item)
        if result or skip_empty_arrays == False:
            if '\n' in result:
                result = f"{result_type}{brackets[0]}{newline}{result}{newline_previndent}{brackets[1]}"
            else:
                result = f"{result_type}{brackets[0]}{space}{result}{space}{brackets[1]}"

    else:
        result = f"{object_type(item)}{quote_value_if_str(item)}"

    return result
# ******************************************************************************
def n0debug_calc(
    var_object,
    var_name: str           = "",
    level: str              = "DEBUG",
    internal_call: int      = 0,

    show_object_type: bool  = _debug_show_object_type,
    indent_size: int        = 4,
    quote: str              = '"',
    pairs_in_one_line: bool = True,
    json_convention: bool   = False,
    skip_empty_arrays: bool = False,
    skip_simple_types: bool = True,
    show_item_count: bool   = _debug_show_item_count,
):
    """
    Print  calculated value (for example returned by function),
    depends of value in global variable __debug_level.

    :param var_object:
    :param var_name:
    :param level:
    :return:
    """
    n0print(
        (f"id={id(var_object)} " if _debug_show_object_id else "")
      + (f"{var_name} == " if var_name else "")
      + n0pretty(
            var_object,
            show_object_type  = show_object_type,
            indent_size       = indent_size,
            quote             = quote,
            pairs_in_one_line = pairs_in_one_line,
            json_convention   = json_convention,
            skip_empty_arrays = skip_empty_arrays,
            skip_simple_types = skip_simple_types,
            show_item_count   = show_item_count,
        ),
        level = level,
        internal_call = internal_call + 1,
    )
# ******************************************************************************
n0debug_regexp_pattern = re.compile(r'([\w\(\), ]+)|\[(\".*?\"|\d+|\'.*?\')\]')
def n0debug(
    var_name: str,
    alias: str = None,
    level: str = "DEBUG",

    show_object_type: bool  = _debug_show_object_type,
    indent_size: int        = 4,
    quote: str              = '"',
    pairs_in_one_line: bool = True,
    json_convention: bool   = False,
    skip_empty_arrays: bool = False,
    skip_simple_types: bool = True,
    show_item_count: bool   = _debug_show_item_count,
):
    """
    Print value of the variable with name {var_name},
    depends of value in global variable {__debug_level}.

    :param var_name:
    :param level:
    :return:
    """
    if not isinstance(var_name, str):
        raise TypeError("incorrect call of n0debug(..): argument MUST BE string")

    var_names = []
    for match in n0debug_regexp_pattern.finditer(var_name):
        if match.group(1):
            var_names.append((match.group(1),))         # tuple  => var_names[0] is var name else class child
        elif match.group(2):
            # element in square brackets
            value = match.group(2)
            if value.isdigit():
                var_names.append(int(value))            # int   => list index
            else:
                var_names.append((value.strip('"\''),)) # str   => dict key

    def find_var(where, var_names):
        if not var_names:
            return where
        var_name = var_names[0]
        try:
            if isinstance(var_name, tuple):
                __method_arguments = None
                var_name = var_name[0]
                if '(' in var_name:
                    var_name, __method_arguments = var_name.strip().rstrip(')').split('(')
                    if not __method_arguments:
                        __method_arguments = []
                    else:
                        __method_arguments = __method_arguments.strip().split(',')
                        __method_arguments = [
                            eval(__method_argument.strip())
                            for __method_argument in __method_arguments
                        ]
                try:
                    if isinstance(__method_arguments, list):
                        return find_var(getattr(where, var_name)(*__method_arguments), var_names[1:])
                    else:
                        return find_var(getattr(where, var_name), var_names[1:])
                except AttributeError as ex:
                    pass
            return find_var(where[var_name], var_names[1:])
        except:
            raise TypeError()

    try:
        try:
            var_object = find_var(inspect.currentframe().f_back.f_locals, var_names)
        except TypeError as ex:
            var_object = find_var(inspect.currentframe().f_back.f_globals, var_names)
    except TypeError as ex:
        raise NameError(f"impossible to find object '{var_name}'")

    n0debug_calc(
        var_object,
        alias or var_name,
        level = level,
        internal_call = 1,

        show_object_type  = show_object_type,
        indent_size       = indent_size,
        quote             = quote,
        pairs_in_one_line = pairs_in_one_line,
        json_convention   = json_convention,
        skip_empty_arrays = skip_empty_arrays,
        skip_simple_types = skip_simple_types,
        show_item_count   = show_item_count,
    )
# ******************************************************************************
def n0debug_object(object_name: str, level: str = "DEBUG"):
    class_object = inspect.currentframe().f_back.f_locals[object_name]
    class_attribs_methods = set(dir(class_object)) - set(dir(object))
    class_attribs = set()
    class_methods = set()

    prefix = (
        str(type(class_object))
        if _debug_show_object_type
        else (
             f" id={id(class_object)}"
             if _debug_show_object_id
             else ""
        )
    )
    if prefix:
        prefix = "(" + prefix + ")"
    to_print = f"{prefix}{object_name} == \n"

    for attrib_name in class_attribs_methods:
        attrib = getattr(class_object, attrib_name)
        if callable(attrib):
            class_methods.add(attrib_name)
        else:
            class_attribs.add(attrib_name)

    for attrib_name in class_methods:
        to_print += f"=*= function {attrib_name}()\n"

    for attrib_name in class_attribs:
        attrib = getattr(class_object, attrib_name)
        prefix = str(type(attrib)) if _debug_show_object_type else "" + \
                 f" id={id(attrib)}" if _debug_show_object_id else ""
        if prefix:
            prefix = "(" + prefix + ")"
        to_print += f"=== {prefix}{attrib_name} = {n0pretty(attrib)}\n"

    n0print(to_print, level = level, internal_call = True)


################################################################################
__all__ = (
    'set_debug_show_object_type',
    'set_debug_show_object_id',
    'set_debug_show_item_count',
    'init_logger',
    'n0print',
    'n0info',
    'n0error',
    'n0warning',
    'n0pretty',
    'n0debug_calc',
    'n0debug',
    'n0debug_object',
)
################################################################################
