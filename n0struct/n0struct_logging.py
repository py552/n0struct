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
# __prev_end = "\n"

__debug_show_object_type = True
def set_debug_show_object_type(debug_show_object_type: bool):
    global __debug_show_object_type
    __debug_show_object_type = debug_show_object_type


__debug_show_object_id = False
def set_debug_show_object_id(debug_show_object_id: bool):
    global __debug_show_object_id
    __debug_show_object_id = debug_show_object_id


__debug_show_item_count = True
def set_debug_show_item_count(debug_show_item_count: bool):
    global __debug_show_item_count
    __debug_show_item_count = debug_show_item_count


__main_log_filename = None
def init_logger(
        debug_level: str = "TRACE",
        debug_output = sys.stderr,
        debug_timeformat: str = "YYYY-MM-DD HH:mm:ss.SSS",
        debug_show_object_type = False,
        debug_show_object_id = False,
        debug_show_item_count = True,
        debug_logtofile = False,
        log_file_name: str = None,
    ):
    logger.level("DEBUG", color="<white>")  # Change default color of DEBUG messages from blue into light gray

    global __main_log_filename
    if debug_logtofile:
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
        # end: str = "\n"
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
def n0pretty(
            item: typing.Any,
            indent_: int = 0,
            show_type: bool = None,
            __indent_size: int = 4,
            __quotes: str = '"',
            pairs_in_one_line: bool = True,
            json_convention: bool = False,
            skip_empty_arrays: bool = False,
            skip_simple_types: bool = True,
            auto_quotes: bool = True,
            show_item_count: bool = None,
):
    """
    :param item:
    :param indent_:
    :return:
    """
    # ######################################################################
    def indent(indent__ = indent_):
        return "\n" + (" " * (indent__ + 1) * __indent_size) if __indent_size else ""
    # ######################################################################
    def is_list_with_pairs(item: list) -> typing.Union[None, dict]:
        element_names = {} # {keyname1: max_len_of_values1, keyname2: max_len_of_values2}
        for sub_item in item:
            if not isinstance(sub_item, dict) or len(sub_item) > 2:
                return None # Sub element not dictionary with 2 or less elements
            for key in sub_item:
                if key not in element_names:
                    element_names.update({key: 0})
                if len(element_names) > 2:
                    return None # Not more that 2 elems could be condensed into one line
                sub_item_key_value = sub_item[key]
                if not isinstance(sub_item_key_value, (str, int, float)):
                    return None # Sub element has complex structure

                # construct presentation string
                presentation_string = \
                    (
                        (str(type(sub_item_key_value)) or "") \
                            .replace("<class '", "<") \
                            .replace("'>", " ") \
                        + str(len(sub_item_key_value)) \
                        + "> "
                        if (show_type or (show_type is None and __debug_show_object_type))
                        and (not skip_simple_types or not isinstance(sub_item_key_value, (str, int, float)))
                        else ""
                    ) + \
                    (
                        f"{__quotes}{sub_item_key_value}{__quotes}"
                        if isinstance(sub_item_key_value, str)
                        else f"{str(sub_item_key_value)}"
                    )
                element_names.update({key: max(element_names[key], len(presentation_string))})
        return element_names  # Returns dict {"name of key": max length of presented (+type+len and etc) value assosiated with key}
    # ######################################################################
    if not __indent_size:
        pairs_in_one_line = False
    if auto_quotes:
        __quotes = '"'
    result_type = ""

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

        keys_and_max_len_of_value = is_list_with_pairs(item)  # removed walrus operator for compatibility with 3.7
        if pairs_in_one_line and isinstance(item, (list, tuple)) and keys_and_max_len_of_value:
            # Sturcture contains 2 items together
            for sub_item in item:
                if result:
                    result += "," + indent()
                result += "{"
                sub_result = ""
                for key in keys_and_max_len_of_value:
                    if key in sub_item:
                        sub_item_key_value = sub_item[key]

                        key_type = ""
                        value_type = ""
                        if show_type or (show_type is None and __debug_show_object_type):
                            if not skip_simple_types \
                            or not isinstance(key, (str, int, float, complex, bool, list, tuple, set, frozenset, dict, type(None))):
                                key_type = (str(type(key)) or "") \
                                    .replace("<class '", "<") \
                                    .replace("'>", "")
                                if isinstance(key, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
                                    key_type += f" {len(key)}"
                                key_type += "> "

                            if not skip_simple_types \
                            or not isinstance(sub_item_key_value, (str, int, float, complex, bool, list, tuple, set, frozenset, dict, type(None))):
                                value_type = (str(type(sub_item_key_value)) or "").replace("<class '", "<").replace("'>", "")
                                if isinstance(sub_item_key_value, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
                                    value_type += f" {len(sub_item_key_value)}"
                                value_type += "> "

                        if isinstance(sub_item_key_value, str):
                            sub_item_key_value = sub_item_key_value.replace('\"', '\\\"')  # SyntaxError: f-string expression part cannot include a backslash
                            sub_item_result = f"{__quotes}{sub_item_key_value}{__quotes}"
                        else:
                            sub_item_result = str(sub_item_key_value)
                            if isinstance(sub_item_key_value, bool) and json_convention:
                                sub_item_result = sub_item_result.lower()
                        sub_item_result = f"{value_type}{sub_item_result}".ljust(keys_and_max_len_of_value[key])

                        if isinstance(key, str):
                            key = key.replace('\"', '\\\"')  # SyntaxError: f-string expression part cannot include a backslash
                            key = f"{__quotes}{key}{__quotes}"
                        else:
                            key = str(key)

                        if sub_result:
                            sub_result += ","
                        sub_result += f" {key_type}{key}: {sub_item_result}"
                    else:
                        if sub_result:
                            sub_result += (" " if __indent_size else "")
                        sub_result += (" " if __indent_size else "")*(1+len(__quotes)+len(key)+len(__quotes)+len(": " if __indent_size else ":")+keys_and_max_len_of_value[key])
                result += sub_result + " }"
        else:
            # dict, set, frozenset or list/tuple with complex or not paired structure
            condense_dict_pairs = isinstance(item, dict) and len(item.keys()) <= 2 and all(isinstance(sub_item, str) for sub_item in item.values())

            for i_sub_item, sub_item in enumerate(item):
                if isinstance(item, dict):
                    key = sub_item

                    if indent_ < 111:
                        sub_item_value = n0pretty(
                                                item[key],
                                                indent_ + 1,
                                                show_type,
                                                __indent_size,
                                                __quotes,
                                                pairs_in_one_line,
                                                json_convention,
                                                skip_empty_arrays,
                                                skip_simple_types,
                                                auto_quotes,
                                                show_item_count,
                        )
                    else:
                        sub_item_value = "{.......}"

                    key_type = ""
                    if (show_type or (show_type is None and __debug_show_object_type)) \
                    and (not skip_simple_types or not isinstance(key, (str, int, float, type(None)))):
                        key_type = (str(type(key)) or "") \
                            .replace("<class '", "<") \
                            .replace("'>", "")
                        if isinstance(key, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
                            key_type += f" {len(key)}"
                        key_type += "> "
                    if isinstance(key, str):
                        key = f"{__quotes}{key}{__quotes}"
                    else:
                        key = str(key)

                    if not sub_item_value:
                        sub_item_value = str(sub_item_value) # None

                    sub_item_value = f"{key_type}{key}:" + (" " if __indent_size else "") + sub_item_value

                else:
                    # set, frozenset or list/tuple with complex or not paired structure
                    if show_item_count or (show_item_count is None and __debug_show_item_count):
                        sub_item_value = f"#{i_sub_item} ".ljust(5)
                    else:
                        sub_item_value = ""

                    if indent_ < 111:
                        sub_item_value += str(n0pretty(
                                                sub_item,
                                                indent_ + 1,
                                                show_type,
                                                __indent_size,
                                                __quotes,
                                                pairs_in_one_line,
                                                json_convention,
                                                skip_empty_arrays,
                                                skip_simple_types,
                                                auto_quotes,
                                                show_item_count,
                        ))
                    else:
                        sub_item_value = "[.......]"

                if sub_item_value is not None:
                    if result:
                        result += ","
                        if not condense_dict_pairs:
                            result += indent()
                        else:
                            result += (" " if __indent_size else "")
                    result += sub_item_value

        if (show_type or (show_type is None and __debug_show_object_type)) \
        and (not skip_simple_types or not isinstance(item, (str, int, float))):
            # removed walrus operator for compatibility with 3.7
            result_type = str(type(item)).replace("<class '", "<").replace("'>", " ")
            if result_type:
                class_type_parts = result_type.split('.')
                if len(class_type_parts) > 2:
                    # leave just only first and last class names
                    result_type = ".".join((class_type_parts[0], class_type_parts[-1]))

            if isinstance(item, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
                result_type += f" {len(item)}"
            result_type += "> "

        if result or skip_empty_arrays == False:
            if "\n" in result:
                result = result_type + brackets[0] + indent() + result + indent(indent_ - 1) + brackets[1]
            else:
                result = result_type + brackets[0] + (" " if __indent_size else "") + result + (" " if __indent_size else "") + brackets[1]

        if result is None:
            if json_convention:
                result = "null"  # json.decoder.JSONDecodeError: Expecting value
            else:
                result = "None"

    elif isinstance(item, str):
        if (show_type or (show_type is None and __debug_show_object_type)) \
        and (not skip_simple_types or not isinstance(item, (str, int, float))):
            result_type = (str(type(item)) or "") \
                            .replace("<class '", "<") \
                            .replace("'>", " ") \
                          + f"{len(item)}> "
        if auto_quotes and '"' in item and "'" not in item:
                result = result_type + f"'{item}'"
        else:
            result = result_type + __quotes + item.replace(__quotes, '\\"' if __quotes == '"' else "\\'") + __quotes
    elif item is None:
        if json_convention:
            result = "null"  # json.decoder.JSONDecodeError: Expecting value
        else:
            result = "None"
    else:
        result = str(item)
        if (show_type or (show_type is None and __debug_show_object_type)) \
        and (not skip_simple_types or not isinstance(item, (str, int, float))):
            result_type = (str(type(item)) or "") \
                            .replace("<class 'function'>", " ") \
                            .replace("<class '", "<") \
                            .replace("'>", "> ")
            result = result_type + result

        if isinstance(item, bool) and json_convention:
            result = result.lower()

    return result
# ******************************************************************************
def n0debug_calc(var_object, var_name: str = "", level: str = "DEBUG", internal_call: int = 0,
            show_type: bool = None,
            pairs_in_one_line: bool = True,
            json_convention: bool = False,
            skip_empty_arrays: bool = False,
            skip_simple_types: bool = True,
            auto_quotes: bool = True,
            show_item_count: bool = None,
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
        (f"id={id(var_object)} " if __debug_show_object_id else "")
      + (f"{var_name} == " if var_name else "")
      + n0pretty(
            var_object,
            show_type = show_type,
            pairs_in_one_line = pairs_in_one_line,
            json_convention = json_convention,
            skip_empty_arrays = skip_empty_arrays,
            skip_simple_types = skip_simple_types,
            auto_quotes = auto_quotes,
            show_item_count = show_item_count,
        ),
        level = level,
        internal_call = internal_call + 1,
    )
# ******************************************************************************
n0debug_regexp_pattern = re.compile(r'([\w\(\), ]+)|\[(\".*?\"|\d+|\'.*?\')\]')
def n0debug(var_name: str, alias: str = None, level: str = "DEBUG",

            show_type: bool = None,
            pairs_in_one_line: bool = True,
            json_convention: bool = False,
            skip_empty_arrays: bool = False,
            skip_simple_types: bool = True,
            auto_quotes: bool = True,
            show_item_count: bool = None,
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
        var_object, alias or var_name,
        level = level, internal_call = 1,

        show_type = show_type,
        pairs_in_one_line = pairs_in_one_line,
        json_convention = json_convention,
        skip_empty_arrays = skip_empty_arrays,
        skip_simple_types = skip_simple_types,
        auto_quotes = auto_quotes,
        show_item_count = show_item_count,
    )
# ******************************************************************************
def n0debug_object(object_name: str, level: str = "DEBUG"):
    class_object = inspect.currentframe().f_back.f_locals[object_name]
    class_attribs_methods = set(dir(class_object)) - set(dir(object))
    class_attribs = set()
    class_methods = set()

    prefix = (
        str(type(class_object))
        if __debug_show_object_type
        else (
             f" id={id(class_object)}"
             if __debug_show_object_id
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
        prefix = str(type(attrib)) if __debug_show_object_type else "" + \
                 f" id={id(attrib)}" if __debug_show_object_id else ""
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
