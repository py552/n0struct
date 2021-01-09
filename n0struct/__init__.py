# 0.01 = 2020-07-25 = Initial version
# 0.02 = 2020-07-26 = Enhancements
# 0.03 = 2020-08-02 = Huge enhancements
# 0.04 = 2020-08-05 = Prepared for upload to pypi.org
# 0.05 = 2020-08-11 = Huge enhancements: unification of .*compare() .toJson(), .toXml(), n0dict(JSON/XML string)
# 0.06
# 0.07 = 2020-09-02 = .compare(transform=..) and .direct_compare(transform=..) added
# 0.08 = 2020-09-05 = refactoring
# 0.09 = lost
# 0.10 = rewritten date related functions
# 0.11 = 2020-09-17 fixed returning time by date_delta(..)
# 0.12 = 2020-09-24 added function to find keys in n0dict
# 0.13 = 2020-10-11
#        n0dict.nvl(..) now supports complicated path like A/B/C
#        n0dict.__FindElem(..) previously supports modificators [i], [last()], [last()-X], [-X]
#                              now additionally supports modificators [text()="XYZ"], [text()=="XYZ"], [text()!="XYZ"], /../
#                              XYZ must be encoded with urlencode
# 0.14 = 2020-10-17 n0print prints to stderr
# 0.15 = 2020-10-19 n0pretty(..): fix for json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes
#                   strip_namespaces() is added
# 0.16 = 2020-10-20 strip_namespaces() transformed into transform_structure()
#                   n0dict.compare() is fixed to use compare_only=
# 0.17 = 2020-10-22 n0print(..): optimization
# 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
# 0.19 = 2020-10-24 fixed issue with autotests, recursive convertion is added into constructor
# 0.20 = 2020-10-26 get_composite_keys(transform=..) is added, numeric checking is fixed
# 0.21 = 2020-11-09 fixed Exception: Why parent is None?
#                   date_slash_ddmmyyyy() is added
# 0.22 = 2020-11-09 fixed date_now() -> str 20 characters YYYYMMDDHHMMSSFFFFFF
# 0.23 = 2020-11-14 fixed n0list.compare()'s issue if more that one the same records are in the list
#                   *.compare() return ["othernotfound"] -> "self_unique"
#                   *.compare() return ["selfnotfound"]  -> "other_unique"
#                   *.compare() return ["notequal"]      -> "not_equal"
#                   get_composite_keys(..) -> generate_composite_keys(..)
# 0.24 = 2020-11-20 added is_exist(..), rewritten to_json(..), AddElem(..)'s optimization started
# 0.25 = 2020-11-20 removed:
#                       n0dict. __FindElem(..)
#                       n0dict. __AddElem(..)
#                       n0dict. AddElem(..)
#                   rewritten:
#                       n0dict. __getitem__(..)
#                       n0dict. __setitem__(..)
#                   added:
#                       n0dict. _find(..)
#                       n0dict. _add(..)
# 0.26 = 2020-12-15 rewritten n0dict. nvl()
# 0.27 = 2020-12-16
#                   added:
#                       n0dict. _get(..)
#                   rewritten:
#                       n0dict. __getitem__(..)
#                       n0dict. nvl()
#                       n0dict. _add()
#                   fixed:
#                       n0pretty()
# 0.28 = 2020-12-17
#                   renamed:
#                       n0dict. nvl() -> get(..)
#                   rewritten:
#                       n0dict. __setitem__(..)
#                       n0dict. _add()
# 0.29 = 2020-12-18
#                   added:
#                       n0list. any_*()
# 0.30 = 2020-12-20
#                   added:
#                       n0list. __contains__()  # something in n0list()
#                       n0dict. valid()
# 0.31 = 2020-12-20
#                   rewritten:
#                       n0dict. _find(..)
#                       split_name_index(..)
# 0.32 = 2020-12-21
#                   fixed:
#                       n0dict. _find(..): if not parent_node: => if parent_node is None:
#                                          because of parent_node could be '' as allowed value
# 0.33 = 2020-12-22
#                   enhanced:
#                       n0dict. _find(..): parent_node become mandatory argument
#                       n0dict. _get(..): support leading '?' in xpath
# 0.34 = 2020-12-24
#                   enhanced:
#                       n0list. __init__(..): option recursively:bool = True was added
#                       n0dict. __init__(..): option recursively:bool = True was added
# 0.35 = 2020-12-26
#                   enhanced:
#                       n0dict. __xml(..): nodes int, float support added
#                       n0dict. to_xml(..): multi-root support added
#                   enhanced version of xmltodict0121 was incapsulated till changes will be merged with main branch of xmltodic
#                   xmltodict0121 enhancement: automaticaly creation n0dict/n0list structure during XML import
# 0.36 = 2020-12-27
#                   xmltodict0121 was removed -- using strandard fuctionality of json and xmltodict: just only dict to n0dict will be automatic converted
#                   during loading xml/json and automatic conversion list into n0list use named parameter recursively=True in the costructor:
#                   my_n0dict = n0dict(json_txt, recursively=True)
#                   enhanced:
#                       n0dict. __init__(..)
#                       n0list. __init__(..)
#                       n0dict. __path(..)
#                       test_n0struct.py
# 0.37 = 2020-12-28
#                   fixed:
#                       n0dict. __xml(..)
# 0.38 = 2020-12-29
#                   enhanced:
#                       n0dict. __init__(..): option force_n0dict == None|!None was added, used ONLY for JSON text convertion
#                           force_n0dict == False/0/None => create [] (ordinary dict) nodes during JSON text convertion (json.loads)
#                           force_n0dict == True/1/any => create n0dict() nodes during JSON text convertion (json.loads)
#                           recursively == True => convert all list/dict nodes created during JSON text convertion (json.loads) into n0list/n0dict
#
#                       Performance results of some real code with JSON convertion:
#                           JSON_struct = n0dict(JSON_txt, recursively=True) => n0dict/n0list:
#                               36.889860 MB memory is used, 2.566520 seconds are taken for execution
#                           JSON_struct = n0dict(JSON_txt, recursively=False) => dict/list => JSON_subnode = n0dict(JSON_struct["node/subnode"]):
#                               36.945560 MB memory is used, 2.546720 seconds are taken for execution
#                           JSON_struct = n0dict(JSON_txt, force_n0dict=True) => n0dict/list:
#                               36.995180 MB memory is used, 2.576020 seconds are taken for execution
#
#                       Results are VERY strange, but they are true:
#                           Minimum memory usage: load as list/dict, and after convert all of them into n0list/n0dict inside constructor
#                           Maximum speed: load as list/dict, and after convert just requiered nodes into n0dict
#                       *** BEFORE MAKING DECISION MAKE YOUR OWN PERFORMACE TESTING ***
#
#                       Same for XML:
#                           XML_struct = n0dict(XML_txt, recursively=True) => n0dict/n0list:
#                           XML_struct = n0dict(XML_txt, recursively=False) => n0dict/list
#                           XML_struct = n0dict(XML_txt, force_n0dict=True) =>
#                               force_n0dict is ignored -- the same like n0dict(XML_txt, recursively=False) => n0dict/list
# 0.39 = 2021-01-04
#                   fixed:
#                       n0dict. __init__(..): xmltodict.parse(args[0], dict_constuctor = n0dict),
# 0.40 = 2021-01-08
#                   enhanced:
#                       def n0pretty(item, indent_: int = 0, show_type:bool = True):
#                   added:
#                       n0dict. first(..)
#                       n0list. __getitem__(..)
#                       n0list. _get(..)
#                       n0list. get(..)
#                       n0list. first(..)
# 0.41 = 2021-01-09
#                   enhanced:
#                       Added predicate attrib[contains(text(),"TEXT")] or attrib[text()~~"TEXT"] or [attrib~~"TEXT"]
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/@value[contains(text(),"PRE")]/../@value'))
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/@value[text()~~"PRE"]/../@value'))
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/[@value~~"PRE"]/@value'))

from __future__ import annotations  # Python 3.7+: for using own class name inside body of class

import sys
import os
import inspect
import typing
from datetime import datetime, timedelta, date
import random
from collections import OrderedDict
import xmltodict
# from .xmltodict0121 import *
import json
# from .json2010 import *
import urllib
from typing import Union
import n0struct

# ********************************************************************
# ********************************************************************
__flag_compare_check_different_types = False


def set__flag_compare_check_different_types(value):
    """
    if __flag_compare_check_different_types == True, then
    validate type of attributes in .compare()/.direct_compare()
    and return result["difftypes"]
    """
    global __flag_compare_check_different_types
    __flag_compare_check_different_types = value
    return __flag_compare_check_different_types


def get__flag_compare_check_different_types():
    global __flag_compare_check_different_types
    return __flag_compare_check_different_types


# ********************************************************************
__flag_compare_return_difference_of_values = False


def set__flag_compare_return_difference_of_values(value):
    """
    if __flag_compare_return_difference_of_values == True, then
    if values of attributes are different and are int,float,
    return additional element in result["not_equal"] with difference
    """
    global __flag_compare_return_difference_of_values
    __flag_compare_return_difference_of_values = value
    return __flag_compare_return_difference_of_values


def get__flag_compare_return_difference_of_values():
    global __flag_compare_return_difference_of_values
    return __flag_compare_return_difference_of_values

# ********************************************************************
# ********************************************************************
def n0isnumeric(value: str):
    # return value.translate(str.maketrans("+-.", "000")).isnumeric() # Py3 dirty fix
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, str):
        return False
    value = value.strip()
    if value.startswith('+') or value.startswith('-'):
        value = value[1:].strip()
    if len(value) > 10:
        return False
    if value.count('.') == 1:
        value = value.replace('.','0')
    return value.isnumeric()
# ********************************************************************
# ********************************************************************
def n0eval(_str: str) -> Union(int,str):
    def my_split(_str: str, _separator: str) -> list:
        return [
                (_separator if _separator != '+' and i else "") + itm.strip()
                for i, itm in enumerate(_str.split(_separator))
                if itm.strip()
        ]

    if not isinstance(_str, str):
        return _str

    _str = _str.replace(" ","").lower()
    if not _str:
        return _str
        # raise ValueError("Could not convert empty/null string into index")

    first_split = my_split(_str, '+')
    second_split = []
    for item in first_split:
        items = my_split(item, '-')
        second_split.extend(items)

    result = 0
    for item in second_split:
        if item == "new()":
            return _str
        if item == "last()":
            item = -1
        else:
            try:
                item = int(item)
            except Exception:
                return _str
        result += item

    return result
# ********************************************************************
# ********************************************************************
def split_name_index(node_name: str) -> tuple:
    node_index = None
    if isinstance(node_name, str):
        if '[' in node_name and node_name.endswith(']'):
            node_name, node_index = node_name[:-1].split('[', 1)
            node_name = node_name.strip()
            node_index = node_index.strip()
            if isinstance(node_index, str):
                if node_index == "":
                    node_index = None
                
                if node_index.lower().startswith('contains') and node_index.endswith(')'):
                    node_index_part1, node_index_part2 = node_index[8:-1].strip().split('(',1)[1].split(',',1)
                    if node_index_part1.lower().startswith('text'):
                        node_index = "text()~~" + node_index_part2
                if '=' in node_index or '~' in node_index:
                    separators = ("==","!=","~~","!~","~","=")
                    for separator in separators:
                        if separator in node_index:
                            expected_node_name, expected_value = node_index.split(separator,1)
                            expected_node_name = expected_node_name.strip()
                            expected_value = expected_value.strip()
                            if separator == '=':
                                separator = '=='
                            if separator == '~':
                                separator = '~~'
                            break
                    else:
                        raise Exception("Never must be happend!")

                    if isinstance(expected_value, str):
                        if expected_value.lower() == "true()":
                            expected_value = True
                        elif expected_value.lower() == "false()":
                            expected_value = False
                        elif (expected_value.startswith('"') and expected_value.endswith('"')) or \
                                (expected_value.startswith("'") and expected_value.endswith("'")):
                            expected_value = expected_value[1:-1]
                            expected_value = urllib.parse.unquote(expected_value)

                    node_index = expected_node_name, separator, expected_value

    return node_name, node_index
# ********************************************************************
# ********************************************************************
def date_delta(now: date = None, day_delta: int = 0, month_delta: int = 0) -> date:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> date
    """
    date_delta_ = (now or datetime.today()) + timedelta(days=day_delta)
    month_quotient, month_remainder = divmod(date_delta_.month + month_delta - 1, 12)
    date_delta_ = datetime  (
                            date_delta_.year + month_quotient, month_remainder + 1, date_delta_.day,
                            date_delta_.hour, date_delta_.minute,  date_delta_.second,  date_delta_.microsecond
                            )
    return date_delta_

def date_now(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str 20 characters YYYYMMDDHHMMSSFFFFFF
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y%m%d%H%M%S%f")

def date_iso(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str ISO date format
    """
    return date_delta(now, day_delta, month_delta).isoformat(timespec='microseconds')

def date_yyyymmdd(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y-%m-%d")

def date_slash_ddmmyyyy(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD/MM/YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d/%m/%Y")

def date_ddmmyyyy(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD-MM-YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d-%m-%Y")

def date_yyyymmdd(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y-%m-%d")


def date_yymm(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMM
    """
    return date_delta(now, day_delta, month_delta).strftime("%y%m")


def date_mmyy(now: date = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str MMYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%m%y")


def from_ddmmmyy(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: DD-MMM-YY # 16-JUL-20
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%d-%b-%y").date()  # 16-JUL-20
    except (ValueError, TypeError):
        return date_str


def from_yyyymmdd(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: YYYY-MM-DD # 2020-07-16
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()  # 2020-07-16
    except (ValueError, TypeError):
        return date_str


def from_ddmmyyyy(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: DD-MM-YYYY # 16-07-2020
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()  # 16-07-2020
    except (ValueError, TypeError):
        return date_str


def to_date(date_str: str) -> typing.Union[date, str]:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()  # 2020-07-16
    except (ValueError, TypeError):
        try:
            return datetime.strptime(date_str, "%d-%b-%y").date()  # 16-JUL-20
        except (ValueError, TypeError):
            try:
                return datetime.strptime(date_str, "%d-%m-%Y").date()  # 16-07-2020
            except (ValueError, TypeError):
                try:
                    return datetime.strptime(date_str, "%d.%m.%Y").date()  # 16.07.2020
                except (ValueError, TypeError):
                    try:
                        return datetime.strptime(date_str, "%m/%d/%Y").date()  # 07/16/2020
                    except (ValueError, TypeError):
                        return date_str


# ********************************************************************
# ********************************************************************
def rnd(till_not_included: int) -> int:
    """
    :param till_not_included:
    :return: int [0..till_not_included)
    """
    return int(random.random() * till_not_included)


def random_from(from_list: list):
    """
    :param from_list:
    :return: from_list[rnd]
    """
    return from_list[rnd(len(from_list))]


def get_key_by_value(dict_: dict, value_):
    """
    :param dict_:
    :param value_:
    :return: last key which is associated with value_ in dict_
    """
    return {value: key for key, value in dict_.items()}[value_]


# ********************************************************************
# __debug_levels = {
# "ALLWAYS":  0,  # 0  = Show in any cases
# "FATAL":    1,  # 1  = Show if __debug_level >= 1
# "ERROR":    2,  # 2  = Show if __debug_level >= 2
# "WARN":     3,  # 3  = Show if __debug_level >= 3
# "WARN2":    4,  # 4  = Show if __debug_level >= 4
# "INFO":     5,  # 5  = Show if __debug_level >= 5
# "DEBUG":    6,  # 6  = Show if __debug_level >= 6
# "NOTE":     7,  # 7  = Show if __debug_level >= 7
# "TRACE":    8,  # 8  = Show if __debug_level >= 8
# "OTHER":    9,  # 9  = Show if __debug_level >= 9
# }
# __debug_level = __debug_levels["INFO"]
__debug_levels = (
    "ALLWAYS",  # 0  = Show in any cases
    "FATAL",  # 1  = Show if __debug_level >= 1
    "ERROR",  # 2  = Show if __debug_level >= 2
    "WARN",  # 3  = Show if __debug_level >= 3
    "WARN2",  # 4  = Show if __debug_level >= 4
    "INFO",  # 5  = Show if __debug_level >= 5
    "DEBUG",  # 6  = Show if __debug_level >= 6
    "NOTE",  # 7  = Show if __debug_level >= 7
    "TRACE",  # 8  = Show if __debug_level >= 8
    "OTHER",  # 9  = Show if __debug_level >= 9
)
__debug_level = 5  # __debug_levels.index("INFO")
__prev_end = "\n"


def set__debug_level(value: int):
    global __debug_level
    __debug_level = value
    return __debug_level

# ********************************************************************
__debug_output = sys.stderr.write
def set__debug_output(value: function):
    global __debug_output
    __debug_output = value
    return __debug_output
def n0print(
        text: str,
        level: int = 5,  # __debug_levels.index("INFO")
        internal_call: bool = False,
        end: str = "\n"
):
    """
    if {level} <= {__debug_level} then print {text}{end}

    :param text:
    :param level:
    :param end:
    :param internal_call:
    :return: None
    """
    global __prev_end
    if __prev_end == "\n":
        if internal_call == False:
            frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
        else:
            try:
                frameinfo = inspect.stack()[2]
            except:
                frameinfo = inspect.stack()[1]

        global __debug_level
        global __debug_levels
        if level <= __debug_level:
            __debug_output(
                "***%s %s %s:%d: " % (
                    (" [%s]" % __debug_levels[level]) if internal_call else " [ALWAYS]",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    os.path.split(frameinfo.filename)[1],
                    frameinfo.lineno
                )
                + (text if text else "") + end
            )
    else:
        __debug_output((text if text else "") + end)
    __prev_end = end


# ********************************************************************
def n0debug(var_name: str, level: int = 5):  # __debug_levels.index("INFO")
    """
    Print value of the variable with name {var_name},
    depends of value in global variable {__debug_level}.

    :param var_name:
    :param level:
    :return:
    """
    if not isinstance(var_name,str):
        frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
        sys.stdout.write(
            "*** %s:%d: incorrect call of n0debug(..): argument MUST BE string" % (
                os.path.split(frameinfo.filename)[1],
                frameinfo.lineno
            )
        )
        sys.exit(-1)
    # print(inspect.currentframe().f_back.f_locals)
    # print("~"*80)
    # print(var_name)
    # print(inspect.currentframe().f_back.f_locals.get(var_name))
    var_object = inspect.currentframe().f_back.f_locals[var_name]
    n0print(
        "(%s id=%s)%s = %s" % (
            type(var_object),
            id(var_object),
            var_name,
            n0pretty(var_object)
        ),
        level = level,
        internal_call = True,
    )

def n0debug_calc(var_value: str, var_name: str = "", level: int = 5):  # __debug_levels.index("INFO")
    """
    Print  calculated value (for example returned by function),
    depends of value in global variable __debug_level.

    :param var_value:
    :param var_name:
    :param level:
    :return:
    """
    n0print(
            "(%s id=%s)%s = %s" %
            (
                type(var_value),
                id(var_value),
                var_name,
                n0pretty(var_value)
            ),
            level = level,
            internal_call = True,
    )


def n0pretty(item, indent_: int = 0, show_type:bool = True):
    """
    :param item:
    :param indent_:
    :return:
    """
    def indent(indent__ = indent_):
        return "\n" + (" " * (indent__ + 1) * 4)  # __indent_size = 4

    if isinstance(item, (list, tuple, dict, set, frozenset)):
        brackets = "[]"
        if isinstance(item, (set, frozenset, dict)):
            brackets = "{}"
        elif isinstance(item, tuple):
            brackets = "()"
        result = ""
        for sub_item in item:
            if result:
                result += "," + indent()
            if isinstance(item, dict):
                result += "\"" + sub_item + "\": " + n0pretty(item[sub_item], indent_ + 1, show_type)  # json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes
            else:
                result += n0pretty(sub_item, indent_ + 1, show_type)
        if show_type:
            result_type = str(type(item)) + ("%s%d%s " % (brackets[0], len(item), brackets[1])) + brackets[0]
        else:
            result_type = brackets[0]
        if result and "\n" in result:
            result = result_type + indent() + result + indent(indent_ - 1)
        else:
            result = result_type + result
        result += brackets[1]
    elif isinstance(item, str):
        result = '"' + item.replace('"', '\\"') + '"'
    elif item is None:
        result = '"N0ne"'  # json.decoder.JSONDecodeError: Expecting value
    else:
        result = str(item)
    return result


def n0debug_object(object_name: str, level: int = 5):  # __debug_levels.index("INFO")
    class_object = inspect.currentframe().f_back.f_locals[object_name]
    class_attribs_methods = set(dir(class_object)) - set(dir(object))
    class_attribs = set()
    class_methods = set()
    to_print = "(%s id=%s)%s = \n" % (type(class_object), id(class_object), object_name)

    for attrib_name in class_attribs_methods:
        attrib = getattr(class_object, attrib_name)
        if callable(attrib):
            class_methods.add(attrib_name)
        else:
            class_attribs.add(attrib_name)

    for attrib_name in class_methods:
        to_print += "=*= function %s()\n" % attrib_name

    for attrib_name in class_attribs:
        attrib = getattr(class_object, attrib_name)
        to_print += "=== (%s id=%s)%s = %s\n" % (type(attrib), id(attrib), attrib_name, n0pretty(attrib))
    n0print(to_print, level = level, internal_call = True)

# ******************************************************************************
strip_ns = lambda key: key.split(':',1)[1] if ':' in key else key
# # Sample
# currency_converter = {"682": "SAR"}
# keys_for_currency_convertion = {
    # "currency":         lambda value: currency_converter[value] if value in currency_converter else value,
    # "source_currency":  lambda value: currency_converter[value] if value in currency_converter else value,
# }
# def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = keys_for_currency_convertion):
def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = None):
    if key is not None:
        if exception is not None:
            if key in exception:
                return value
        if key in transform_depends_of_key:
            return transform_depends_of_key[key](value)
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 10 and value[2] == '/' and value[5] == '/':
            return datetime.strptime(value, "%d/%m/%Y")  # EUROPEAN!!!
        if len(value) == 10 and value[4] == '-' and value[7] == '-':
            return datetime.strptime(value, "%Y-%m-%d")
        if len(value) == 19 and value[4] == '-' and value[7] == '-' and value[10] == ' ' and value[13] == ':' and value[16] == ':':
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        # if value.translate(str.maketrans("+-.", "000")).isnumeric():
        if n0isnumeric(value):
            # if '.' in value:
            #     return abs(float(value))
            # else:
            #     return abs(int(value))
            return abs(float(value))
        else:
            return value.upper()
    else:
        return value
# ******************************************************************************
def transform_structure(in_structure, transform_key = strip_ns, transform_value = convert_to_native_format):
    # n0debug("in_structure")
    if isinstance(in_structure, (dict, OrderedDict, n0dict)):
        # in_list = (in_structure,)
        in_list = [in_structure]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
    else:
        in_list = in_structure
    # n0debug("in_list")
    if isinstance(in_list, (list, tuple, n0list)):
        out_list = n0list()
        for in_dict in in_list:
            # n0debug("in_dict")
            if not isinstance(in_dict, (dict, OrderedDict, n0dict)):
                raise Exception("transform_structure(): expected to get dict/OrderedDict/n0dict as second level item")
            out_list.append(n0dict())
            for key_in in in_dict:
                key_out = transform_key(key_in)
                out_list[-1].update({key_out: transform_value(in_dict[key_in], key_out) if transform_value else in_dict[key_in]})
    else:
        raise Exception("transform_structure(): expected to get dict/OrderedDict/n0dict or list/tuple/n0list as argument")
    if isinstance(in_structure, (dict, OrderedDict, n0dict)):
        return out_list[0]
    else:
        return out_list
# ******************************************************************************
# notemptyitems(item):
#   Check item or recursively subitems of item.
#   Return count of notempty item/subitems.
# ******************************************************************************
def notemptyitems(item):
    not_empty_items_count = 0
    if isinstance(item, (dict, OrderedDict, n0dict)):
        for key in item:
            not_empty_items_count += notemptyitems(item[key])
    elif isinstance(item, (tuple, list, n0list)):
        for itm in item:
            not_empty_items_count += notemptyitems(itm)
    else:
        if item:
            not_empty_items_count += 1
    return not_empty_items_count


# ******************************************************************************
# xpath_match(xpath: str, xpath_list):
#   Check that real xpath (or xpath like) is equal any of xpath_list[0..n].
#   Returns i+1
# ******************************************************************************
def xpath_match(xpath: str, xpath_list):
    """

    :param xpath:
        xpath: str
    :param xpath_list:
        xpath_list: str or list|tuple
    :return:
         0 not matched any of xpath_list
        >0 matched
    """
    if isinstance(xpath_list, str):
        # xpath_list = (xpath_list,)
        xpath_list = [xpath_list]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
    if not xpath_list:
        return None
    if not isinstance(xpath_list, (tuple, list)):
        raise Exception("xpath_match(..): unknown type of xpath_list = %s" % type(xpath_list))

    xpath_parts = xpath.split("/")
    for i, xpath_itm in enumerate(xpath_list):
        xpath_itm_parts = xpath_itm.split("/")
        for j, part in enumerate(reversed(xpath_itm_parts)):
            if not part:  # //
                # n0print("MATCH: matched relative")
                return i + 1
            # n0debug("part")
            if j >= len(xpath_parts):
                # n0print("not matched: too short")
                break
            if part != "*" and part.lower() != xpath_parts[-1 - j].lower():  # /*/
                # n0print("not matched: not equal")
                break
        else:
            # n0print("MATCH: matched full")
            return i + 1
        # n0print("Let's try new loop")
    # n0print("not matched: not matched with all from list")
    return 0


def generate_composite_keys(input_list: n0list, elemets_for_composite_key: tuple, prefix: str = None, transform: tuple = None) -> list:
    """
    serialization all or {elemets_for_composite_key} elements of {input_list[]}
        :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
    :return:
        [[<composite_key>,[<index of entry>],...}
    """
    if isinstance(elemets_for_composite_key, str):
        # elemets_for_composite_key = (elemets_for_composite_key,)
        elemets_for_composite_key = [elemets_for_composite_key]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A

    composite_keys_for_all_lines = []
    # n0debug("transform")
    if transform:
        attributes_to_transform = [itm[0] for itm in transform]
    else:
        attributes_to_transform = None

    for line_i, line in enumerate(input_list):
        if isinstance(line, (dict, OrderedDict, n0dict)):
            created_composite_key = ""
            if elemets_for_composite_key:
                for key in elemets_for_composite_key:
                    if key in line:
                        if created_composite_key:
                            created_composite_key += ";"
                        fullxpath = "%s/%s" % (prefix, key)
                        transform_i = xpath_match(fullxpath, attributes_to_transform)
                        if transform_i:
                            transform_i -= 1
                            tranformed = transform[transform_i][1](line[key])
                        else:
                            tranformed = str(line[key])
                        created_composite_key += key + "=" + tranformed
            if not created_composite_key:
                for key in line:
                    if created_composite_key:
                        created_composite_key += ";"
                    fullxpath = "%s/%s" % (prefix, key)
                    transform_i = xpath_match(fullxpath, attributes_to_transform)
                    if transform_i:
                        transform_i -= 1
                        tranformed = transform[transform_i][1](line[key])
                    else:
                        tranformed = str(line[key])
                    created_composite_key += key + "=" + tranformed
        else:
            raise Exception("generate_composite_keys(..): expected element dict inside list, but got %s" % type(line))
        # if created_composite_key in composite_keys_for_all_lines:
            # composite_keys_for_all_lines[created_composite_key].append(line_i])
        # else:
            # composite_keys_for_all_lines.update({created_composite_key:[line_i]})
        composite_keys_for_all_lines.append((created_composite_key, line_i))
    return composite_keys_for_all_lines


class n0list(list):
    """
    Class extended builtins.list(builtins.object) with additional methods:
    . direct_compare()  = compare element self[i] with other[i] with the same indexes
    . compare()         = compare element self[i] with any other[?] WITHOUT using sorting
    """
    def __init__(self, *args, **kw):
        """
        args == tuple, kw == mapping(dictionary)

        * == convert from tuple into list of arguments
        ** == convert from mapping into list of named arguments

        :param args:
        :param kw:
            recursively = None/False/0 => don't convert subnodes into n0list/n0dict
        """
        len__args = len(args)
        if not len__args:
            return super(n0list, self).__init__(*args, **kw)
        elif isinstance(args, tuple):
            if len__args == 1:
                from_tuple = args[0]
            else:
                from_tuple = args
            _recursively = kw.get("recursively") or False
            for value in from_tuple:
                if _recursively:
                    if isinstance(value, (dict, OrderedDict)):
                        value = n0dict(value, recursively = _recursively)
                    elif isinstance(value, (list, tuple)):
                        value = n0list(value, recursively = _recursively)
                self.append(value)
# TypeError: __init__() should return None, not 'n0list'
            # return super(n0list, self).__init__(self)
            return None
        # n0debug("args")
        # n0debug("kw")
        raise TypeError("n0list.__init__(..) takes exactly one notnamed argument (list/tuple/n0list)")
    # ******************************************************************************
    # n0list. _find() 
    # ******************************************************************************
    def _find(self, xpath_list: list, parent_node, return_lists, xpath_found_str: str = "/") -> list:
        """
        [0] = parent node: n0dict/n0list
        [1] = node_name_index: str (or key or index)
        [2] = cur_value = None if not_found_xpath_list not is None
        [3] = found_xpath_str: str = "" if nothing found
        [4] = not_found_xpath_list: list = None if initial xpath_list is found
        """
        if isinstance(xpath_list, str):
            xpath_list = [itm.strip() for itm in xpath_list.replace("][","]/[").split('/') if itm]
        if not isinstance(xpath_list, (list, tuple)):
            raise IndexError("xpath (%s)'%s' must be list or string" % (type(xpath_list), str(xpath_list)))
        if not xpath_list:
            if xpath_found_str == '/':
                #================================
                # FOUND: root
                #================================
                return parent_node, None, parent_node, xpath_found_str, None
            else:
                return self._find(xpath_found_str, self, return_lists)
        node_name, node_index = split_name_index(xpath_list[0])
        if node_name:
            #--------------------------------
            # NOT FOUND: Node name in list
            #--------------------------------
            return parent_node, None, None, xpath_found_str, xpath_list
        # ##########################################################################################
        # Index in n0list (node_index is not None)
        # ##########################################################################################
        else:
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            if node_index == "*":
                cur_values = n0list()
                fst_parent_node = fst_node_name_index = fst_value = fst_found_xpath_str = None
                # n0debug("parent_node")
                for i,next_parent_node in enumerate(parent_node):
                    # n0debug("i")
                    # n0debug("next_parent_node")
                    # n0debug_calc(["[%d]" % i] + xpath_list[1:])
                    # n0debug("return_lists")
                    # n0debug("xpath_found_str")
                
                    if isinstance(next_parent_node, n0dict):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists)
                            # cur_not_found_xpath_list = n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists, "%s[%s]" % (xpath_found_str, node_index))
                    elif isinstance(next_parent_node, n0list):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = self._find(xpath_list[1:], next_parent_node, return_lists)
                            # cur_not_found_xpath_list = self._find(xpath_list[1:], next_parent_node, return_lists, "%s[%s]" % (xpath_found_str, node_index))
                    else:
                        raise Exception("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))
                        
                    # cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                        # cur_not_found_xpath_list = self._find(["[%d]" % i] + xpath_list[1:], parent_node, return_lists, xpath_found_str)
                        
                    if not cur_not_found_xpath_list:
                        cur_values.append(cur_value)
                        if not fst_found_xpath_str:
                            fst_parent_node, fst_node_name_index, fst_value, fst_found_xpath_str = \
                                cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str
                if not return_lists and len(cur_values) == 1:
                    cur_values = cur_values[0]
                if fst_found_xpath_str:
                    return fst_parent_node, fst_node_name_index, cur_values, fst_found_xpath_str,   None
                else:
                    return parent_node,     None,               None,       xpath_found_str,        xpath_list
            else:
                try:
                    node_index = n0eval(node_index)
                except:
                    raise IndexError("Unknown index '%s[%s]'" % (xpath_found_str, node_index))

                if isinstance(parent_node, (list, tuple, n0list)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index >= len__parent_node or node_index < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, "[%s]" % node_index, None, xpath_found_str, xpath_list
                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, "[%s]" % node_index, parent_node[node_index], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    next_parent_node =  parent_node[node_index]
                    if isinstance(next_parent_node, n0dict):
                        return n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists, "%s[%s]" % (xpath_found_str, node_index))
                    if isinstance(next_parent_node, n0list):
                        return self._find(xpath_list[1:], next_parent_node, return_lists, "%s[%s]" % (xpath_found_str, node_index))
                    else:
                        raise Exception("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))
    # ******************************************************************************
    # n0list. _get() 
    # ******************************************************************************
    def _get(self, xpath: str, raise_exception = True, if_not_found = None, return_lists = True):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if not xpath:
            return if_not_found
        if xpath.startswith('?'):
            xpath = xpath[1:]
            raise_exception = False
            if_not_found = ''
        if any(char in xpath for char in "/["):
            parent_node, node_name_index, cur_value, found_xpath_str, not_found_xpath_list = self._find(xpath, self, return_lists)
            if not not_found_xpath_list:
                return cur_value
            else:
                if raise_exception:
                    raise IndexError("not found '%s' in '%s'" % ('/'.join(not_found_xpath_list), found_xpath_str))
                else:
                    return if_not_found
        else:
            try:
                return super(n0list, self).__getitem__(n0eval(xpath))
            except IndexError as ex:
                if raise_exception:
                    raise ex
                else:
                    return if_not_found
    # ******************************************************************************
    # n0list. get() 
    # ******************************************************************************
    def get(self, xpath: str, if_not_found = None):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # ******************************************************************************
    # n0list. first() 
    # ******************************************************************************
    def first(self, xpath: str, if_not_found = None):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        If self[where1/where2/.../whereN] is list, thet the first element will be returned
        """
        result = self._get(xpath, raise_exception = False, if_not_found = if_not_found, return_lists = False)
        if isinstance(result, (list, tuple, n0list)) and len(result) == 1:
            result = result[0]
        return result
    # ******************************************************************************
    # ******************************************************************************
    def __getitem__(self, xpath):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if isinstance(xpath, str):
            return self._get(xpath, raise_exception = True)
        else:
            return super(n0list, self).__getitem__(xpath)
    # ******************************************************************************
    # * n0list. direct_compare(..): only n0dict. direct_compare/compare have one_of_list_compare
    # ******************************************************************************
    def direct_compare(
            self,
            other: n0list,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",
            continuity_check: str = "continuity_check",  # After this argument, other MUST be defined ONLY with names
            composite_key: tuple = (),
            compare_only: tuple = (),
            exclude: tuple = (),
            transform: tuple = (),
    ) -> n0dict:
        """
        Recursively compare self[i] with other[i]
        strictly according to the order of elements.
        If self[i] (other[i] must be the same) is n0list/n0dict, then goes deeper
        with n0list.direct_compare/n0dict.direct_compare(..)

        :param self: etalon list for compare.
        :param other: list to compare with etalon
        :param self_name: <default = "self"> dict/list name, used in result["messages"]
        :param other_name: <default = "other"> dict/list name, used in result["messages"]
        :param prefix: <default = ""> xpath prefix, used for full xpath generation
        :param continuity_check: used for checking that below arguments are defined only with names
        :param composite_key:  For compatibility with compare(..)
        :param compare_only: For compatibility with compare(..)
        :param exclude: ()|None|empty mean nothing to exclude
        :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "not_equal"      : [], # generated if elements with the same xpath and type are not equal
                    "self_unique"   : [], # generated if elements from self list don't exist in other list
                    "other_unique"  : [], # generated if elements from other list don't exist in self list
                    "difftypes"     : [], # generated if elements with the same xpath have different types
                })
                if not returned["messages"]: self and other are totally equal.
        """
        if continuity_check != "continuity_check":
            raise Exception("Incorrect order of arguments")
        if not isinstance(other, n0list):
            raise Exception("n0list.direct_compare(): other (%s) must be n0list" % str(other))

        result = n0dict({
            "messages": [],
            "not_equal": [],
            "self_unique": [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        # FIX ME: index in [] is not supported -- only node.
        if xpath_match(prefix, exclude):
            return result

        for i, itm in enumerate(self):
            if i >= len(other):
                # other list is SHORTER that self
                result["messages"].append(
                    "List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                    (
                        self_name, other_name,
                        self_name, i, str(self[i]),
                        other_name
                    )
                )
                result["self_unique"].append(("%s[%i]" % (prefix, i), self[i]))
                continue
            # ######### if i >= len(other):
            # --- TRANSFORM: START -------------------------------------
            # Transform self and other linked values with function transform[]()
            self_value = self[i]
            other_value = other[i]
            transform_i = xpath_match(prefix, [itm[0] for itm in transform])
            if transform_i:
                transform_i -= 1
                transform_self = transform[transform_i][1]
                if len(transform[transform_i]) > 2:
                    transform_other = transform[transform_i][2]
                else:
                    transform_other = transform_self
                self_value = transform_self(self_value)
                other_value = transform_other(other_value)
            # --- TRANSFORM: END ---------------------------------------
            if type(self_value) == type(other_value):
                if isinstance(self_value, (str, int, float, date)):
                    if self_value != other_value:
                        # VERY IMPORTANT TO SHOW ORIGINAL VALUES, NOT TRANSFORMED
                        result["not_equal"].append(
                            (
                                "%s[%i]" % (prefix, i),
                                [
                                    self[i],
                                    other[i]
                                ]
                            )
                        )
                        if get__flag_compare_return_difference_of_values():
                            try:
                                difference = round(float(other_value) - float(self_value), 7)
                            except ValueError:  # self_value or other_value could not be converted to float
                                difference = None
                            result["not_equal"][-1][1].append(difference)
                        result["messages"].append(
                            "Values are different: %s[%d]='%s' != %s[\"%s\"]='%s' " %
                            (
                                self_name, i, str(self[i]),
                                other_name, i, str(other[i])
                            )
                        )
                elif isinstance(self[i], (list, tuple)):
                    result.update_extend(
                        self[i].direct_compare(
                            other[i],
                            "%s[%i]" % (self_name, i),
                            "%s[%i]" % (other_name, i),
                            "%s[%i]" % (prefix, i),
                            # Not used in real, just for compatibility with compare(..)
                            composite_key=composite_key, compare_only=compare_only,
                            exclude=exclude, transform=transform,
                        )
                    )
                elif isinstance(self[i], (n0dict, dict, OrderedDict)):
                    result.update_extend(
                        n0dict(self[i]).direct_compare(
                            n0dict(other[i]),
                            "%s[%i]" % (self_name, i),
                            "%s[%i]" % (other_name, i),
                            "%s[%i]" % (prefix, i),
                            one_of_list_compare=self.direct_compare,
                            composite_key=composite_key, compare_only=compare_only,
                            # Not used in real, just for compatibility
                            exclude=exclude, transform=transform,
                        )
                    )
                elif self[i] is None:
                    # type(self[i]) == type(other[i]) and self[i] is None
                    # So both are None
                    pass
                else:
                    raise Exception(
                        "Not expected type %s in %s[%d]/%s[%d]" %
                        (
                            type(self[i]),
                            self_name, i,
                            other_name, i
                        )
                    )
            # ######### if type(self[i]) == type(other[i]):
            else:
                if get__flag_compare_check_different_types():
                    result["difftypes"].append(
                        (
                            "%s[%i]" % (prefix, i),
                            (
                                type(self[i]),
                                self[i],
                                type(other[i]),
                                other[i]
                            )
                        )
                    )
                    result["messages"].append(
                        "!!Types are different: %s[%d]=(%s)%s != %s[%d]=(%s)%s" %
                        (
                            self_name, i, type(self[i]), str(self[i]),
                            other_name, i, type(other[i]), str(other[i]),
                        )
                    )
                else:
                    result["not_equal"].append(
                        (
                            "%s[%i]" % (prefix, i),
                            (
                                self[i],
                                other[i]
                            )
                        )
                    )
                    result["messages"].append(
                        "Values are different: %s[%d]='%s' != %s[\"%s\"]='%s' " %
                        (
                            self_name, i, str(self[i]),
                            other_name, i, str(other[i])
                        )
                    )

        # ######### for i in enumerate(self)[0]:
        if len(other) > len(self):
            # self list is SHORTER that other
            for i, itm in enumerate(other[len(self):]):
                i += len(self)
                result["messages"].append(
                    "List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, self_name,
                        other_name, i, str(other[i]),
                        self_name
                    )
                )
                result["other_unique"].append(("%s[%i]" % (prefix, i), other[i]))
        return result

    # ******************************************************************************
    # ******************************************************************************

    # ******************************************************************************
    # * n0list. compare(..)
    # ******************************************************************************
    def compare(
            self,
            other: n0list,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",

            continuity_check: str = "continuity_check",  # After this argument, other MUST be defined only with names
            # Strictly recommended to define composite_key+compare_only or composite_key
            # else in case of just only one attribute of element will be different
            # both elements will be marked as not found (unique) inside the opposite list
            composite_key: tuple = (),  # ()|None|empty mean all
            compare_only: tuple = (),  # ()|None|empty mean all
            exclude: tuple = (),  # ()|None|empty mean nothing to exclude
            transform: tuple = (),  # ()|None|empty mean nothing to transform
    ) -> n0dict:
        """
        Recursively compare self[i] with other[?] WITHOUT using order of elements.
        If self[i] (other[?] must be the same) is n0list/n0dict,
        then goes deeper with n0list. compare(..)/n0dict.direct_compare(..)

        :param other:
        :param self_name:
        :param other_name:
        :param prefix:
        :param continuity_check:
        :param composite_key:
        :param compare_only:
        :param exclude:
        :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "not_equal"      : [], # generated if elements with the same xpath and type are not equal
                    "self_unique" : [], # generated if elements from self list don't exist in other list
                    "other_unique"  : [], # generated if elements from other list don't exist in self list
                    "difftypes"     : [], # generated if elements with the same xpath have different types
                })
                if not returned["messages"]: self and other are totally equal.
        """
        if continuity_check != "continuity_check":
            raise Exception("n0list. compare(..): incorrect order of arguments")
        if not isinstance(other, n0list):
            raise Exception("n0list. compare(..): other (%s) must be n0list" % str(other))
        result = n0dict({
            "messages": [],
            "not_equal": [],
            "self_unique": [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        # FIX ME: index in [] is not supported -- only node.
        if xpath_match(prefix, exclude):
            return result

        self_not_exist_in_other = generate_composite_keys(self, composite_key, prefix, transform)
        other_not_exist_in_self = generate_composite_keys(other, composite_key, prefix, transform)

        notmutable__self_not_exist_in_other = self_not_exist_in_other.copy()
        # notmutable__other_not_exist_in_self = other_not_exist_in_self.copy()
        # for self_i, composite_key in enumerate(notmutable__self_not_exist_in_other):
        for composite_key, self_i  in notmutable__self_not_exist_in_other:
            # other_composite_keys = [itm[0] for itm in other_not_exist_in_self]
            # other_i = other_not_exist_in_self[other_composite_keys.index(composite_key)][1]
            try:
                other_i = other_not_exist_in_self[[itm[0] for itm in other_not_exist_in_self].index(composite_key)][1]
            except ValueError:
                other_i = None
            # if composite_key in other_composite_keys:
            if not other_i is None:
                # other_i = notmutable__other_not_exist_in_self.index(composite_key)
                # other_i = other_not_exist_in_self[other_composite_keys.index(composite_key)][1]
                # --- TRANSFORM: START -------------------------------------
                # Transform self and other linked values with function transform[]()
                self_value = self[self_i]
                other_value = other[other_i]
                transform_i = xpath_match(prefix, [itm[0] for itm in transform])
                if transform_i:
                    transform_i -= 1
                    transform_self = transform[transform_i][1]
                    if len(transform[transform_i]) > 2:
                        transform_other = transform[transform_i][2]
                    else:
                        transform_other = transform_self
                    self_value = transform_self(self_value)
                    other_value = transform_other(other_value)
                # --- TRANSFORM: END ---------------------------------------
                if type(self_value) == type(other_value):
                    if isinstance(self_value, (str, int, float, date)):
                        if self_value != other_value:
                            if self_i == other_i:
                                # VERY IMPORTANT TO SHOW ORIGINAL VALUES, NOT TRANSFORMED
                                result["not_equal"].append(
                                    (
                                        "%s[%d]" % (prefix, self_i),
                                        [
                                            self[self_i],
                                            other[other_i]
                                        ]
                                    )
                                )
                            else:
                                # VERY IMPORTANT TO SHOW ORIGINAL VALUES, NOT TRANSFORMED
                                result["not_equal"].append(
                                    (
                                        "%s[%d]<>[%d]" % (prefix, self_i, other_i),
                                        [
                                            self[self_i],
                                            other[other_i]
                                        ]
                                    )
                                )
                            if get__flag_compare_return_difference_of_values():
                                try:
                                    difference = round(float(other_value) - float(self_value), 7)
                                except ValueError:  # self_value or other_value could not be converted to float
                                    difference = None
                                result["not_equal"][-1][1].append(difference)
                            result["messages"].append(
                                "Values are different: %s[%d]='%s' != %s[%d]='%s' " %
                                (
                                    self_name, self_i, str(self[self_i]),
                                    other_name, other_i, str(other[other_i])
                                )
                            )
                    elif isinstance(self[self_i], (list, tuple)):
                        result.update_extend(
                            n0list(self[self_i]).compare(
                                n0list(other[other_i]),
                                "%s[%d]" % (self_name, self_i),
                                "%s[%d]" % (other_name, other_i),
                                "%s[%d]%s" % (
                                    prefix,
                                    other_i,
                                    ("<>[%d]" % other_i) if self_i != other_i else ""
                                ),
                                composite_key=composite_key, compare_only=compare_only,
                                exclude=exclude, transform=transform,
                            )
                        )
# 0.18 = Splitted logic, to avoid convertation of dict, OrderedDict into n0dict
                    elif isinstance(self[self_i], (n0dict,)):
                        result.update_extend(
                            n0dict(self[self_i]).compare(
                                # n0dict(other[other_i]),  # 0.18
                                other[other_i],
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + (
                                    "<>[" + str(other_i) + "]" if self_i != other_i else ""),
                                one_of_list_compare=self.compare,
                                composite_key=composite_key, compare_only=compare_only,
                                exclude=exclude, transform=transform,
                            )
                        )
# 0.18 = Splitted logic, to avoid convertation of dict, OrderedDict into n0dict
                    elif isinstance(self[self_i], (dict, OrderedDict)):  # Very important isinstance suppose that n0dict is the same like OrderedDict, because of it's parent class
                        raise Exception("self[self_i] is %s, expected n0dict" % type(self[self_i]))
                    elif self[self_i] is None:
                        # type(self[self_i]) == type(other[other_i]) and self[self_i] is None
                        # So both are None
                        pass
                    else:
                        raise Exception(
                            "Not expected type %s in %s[%d]/%s[%d]" %
                            (
                                type(self[self_i]),
                                self_name, self_i,
                                other_name, other_i
                            )
                        )
                # ######### if type(self[i]) == type(other[i]):
                else:
                    if get__flag_compare_check_different_types():
                        result["difftypes"].append(
                            (
                                prefix + "[" + str(self_i) + "]",
                                (
                                    type(self[self_i]), self[self_i],
                                    type(other[other_i]), other[other_i]
                                )
                            )
                        )
                        result["messages"].append("++Types are different: %s[%d]=(%s)%s != %s[%d]=(%s)%s" %
                                                  (
                                                      self_name, self_i, type(self[self_i]), str(self[self_i]),
                                                      other_name, other_i, type(other[other_i]), str(other[other_i]),
                                                  )
                                                  )
                    else:
                        if self_i == other_i:
                            result["not_equal"].append(
                                (
                                    "%s[%d]" % (prefix, self_i),
                                    (
                                        self[self_i],
                                        other[other_i]
                                    )
                                )
                            )
                        else:
                            result["not_equal"].append(
                                (
                                    "%s[%d]<>[%d]" % (prefix, self_i, other_i),
                                    (
                                        self[self_i],
                                        other[other_i]
                                    )
                                )
                            )
                        result["messages"].append(
                            "Values are different: %s[%d]='%s' != %s[\"%s\"]='%s' " %
                            (
                                self_name, self_i, str(self[self_i]),
                                other_name, other_i, str(other[other_i])
                            )
                        )
                # ######### if type(self[i]) == type(other[i]):
                # self_not_exist_in_other.remove(composite_key)
                # other_not_exist_in_self.remove(composite_key)
                del self_not_exist_in_other[[itm[0] for itm in self_not_exist_in_other].index(composite_key)]
                del other_not_exist_in_self[[itm[0] for itm in other_not_exist_in_self].index(composite_key)]
            # ######### if key in other_not_exist_in_self:
        # ######### for key in notmutable__self_not_exist_in_other:

        if self_not_exist_in_other:
            # for composite_key in self_not_exist_in_other:
                # self_i = notmutable__self_not_exist_in_other.index(composite_key)
            for composite_key, self_i in self_not_exist_in_other:
                result["messages"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        self_name, self_i, str(self[self_i]),
                        other_name
                    )
                )
                result["self_unique"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
        if other_not_exist_in_self:
            # for composite_key in other_not_exist_in_self:
                # other_i = notmutable__other_not_exist_in_self.index(composite_key)
            for composite_key, other_i in other_not_exist_in_self:
                result["messages"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, other_i, str(other[other_i]),
                        self_name
                    )
                )
                result["other_unique"].append(("%s[%d]" % (prefix, other_i), other[other_i]))
        return result
    # ******************************************************************************
    # ******************************************************************************
    # def append(self, sigle_item):
    # if isinstance(sigle_item, (list,n0list)):
    # raise (TypeError, '(%s)%s must be scalar' % (type(sigle_item), sigle_item))
    # super(n0list, self).append(sigle_item)  #append the item to itself (the list)
    # return self
    # ******************************************************************************
    # ******************************************************************************
    # def extend(self, other_list):
    # if not isinstance(other_list, (list,n0list)):
    # raise (TypeError, '(%s)%s must be list' % (type(sigle_item), sigle_item))
    # super(n0list, self).extend(other_list)
    # return self
    # ******************************************************************************
    # ******************************************************************************
    def _in(self, other_list, in_is_expected: bool):
        if not isinstance(other_list, (list,tuple,n0list)):
            other_list = [other_list]
        for itm in self:
            if (itm in other_list) == in_is_expected:
                return True
        else:
            return False
    # ******************************************************************************
    def any_in(self, other_list):
        return self._in(other_list, True)
    # ******************************************************************************
    def any_not_in(self, other_list):
        return not self._in(other_list, True)
    # ******************************************************************************
    def all_in(self, other_list):
        return not self._in(other_list, False)
    # ******************************************************************************
    def all_not_in(self, other_list):
        return self._in(other_list, False)
    # ******************************************************************************
    # ******************************************************************************
    def _consists_of(self, other_list, in_is_expected: bool):
        if not isinstance(other_list, (list,tuple,n0list)):
            other_list = [other_list]
        for itm in other_list:
            if super(n0list, self).__contains__(itm) == in_is_expected:
                return True
        else:
            return False
    # ******************************************************************************
    def consists_of_any(self, other_list):
        return self._consists_of(other_list, True)
    # ******************************************************************************
    def consists_of_all(self, other_list):
        return not self._consists_of(other_list, False)
    # ******************************************************************************
    def __contains__(self, other_list):  # otherlist in n0list([a])
        return self.consists_of_all(other_list)
    # ******************************************************************************
    def not_consists_of_any(self, other_list):
        return not self._consists_of(other_list, True)
# ******************************************************************************
# class n0dict(OrderedDict):
class n0dict(dict):
    """
    https://github.com/martinblech/xmltodict/issues/252
    For Python >= 3.6, dictionary are Sorted by insertion order, so avoid the use of OrderedDict for those python versions.
    """
    # ******************************************************************************
    # ******************************************************************************
    def __init__(self, *args, **kw):
        """
        args == tuple, kw == mapping(dictionary)

        * == convert from tuple into list of arguments
        ** == convert from mapping into list of named arguments

        :param args:
        :param kw:
            recursively = None/False/0 => don't convert subnodes into n0list/n0dict
        """
        _object_pairs_hook = n0dict if kw.pop("force_n0dict", None) else None
        len__args = len(args)
        if not len__args:
            return super(n0dict, self).__init__(*args, **kw)
        if len__args == 1:
            # Not kw.pop()! Because of "recursively" will be provided deeper into _constructor(..)
            _recursively = kw.get("recursively", False) or False
            if isinstance(args[0], str):
                if _recursively:
                    _constructor = self.__init__
                else:
                    _constructor = super(n0dict, self).__init__

                if args[0].strip()[0] == "<":
                    # https://github.com/martinblech/xmltodict/issues/252
                    # The main function parse has a force_n0dict keyword argument useful for this purpose.
                    return _constructor(
                        xmltodict.parse(args[0], dict_constructor = n0dict),
                        **kw
                    )
                elif args[0].strip()[0] == "{":
                    return _constructor(
                        json.loads(args[0], object_pairs_hook = _object_pairs_hook),
                        **kw
                    )
            elif isinstance(args[0], (dict, OrderedDict, n0dict)):
                for key in args[0]:
                    value = args[0][key]
                    if _recursively:
                        if isinstance(value, (dict, OrderedDict, n0dict)):
                            value = n0dict(value, recursively = _recursively)
                        elif isinstance(value, (list, tuple, n0list)):
                            value = n0list(value, recursively = _recursively)
                    self.update({key: value})
                return None
            elif isinstance(args[0], zip):
                for key, value in args[0]:
                    self.update({key: value})
                return None
            elif isinstance(args[0], (list, tuple)):
                # [key1, value1, key2, value2, ..., keyN, valueN]
                if (len(args[0]) % 2) == 0 and all(isinstance(itm, str) for itm in args[0][0::2]):
                    for key, value in zip(args[0][0::2],args[0][1::2]):
                        self.update({key: value})
                    return None
                # [(key1, value1), (key2, value2), ..., (keyN, valueN)]
                if all(isinstance(itm, tuple) and len(itm) == 2 and isinstance(itm[0], str) for itm in args[0]):
                    for pair in args[0]:
                        self.update({pair[0]: pair[1]})
                    return None
        raise TypeError("n0dict.__init__(..) takes exactly one notnamed argument (string (XML or JSON) or dict/OrderedDict/n0dict/zip or paired tuple/list)")
    # ******************************************************************************
    def update_extend(self, other):
        if other is None:
            return self
        elif isinstance(other, (n0dict, OrderedDict, dict)):
            for key in other:
                if key not in self:
                    self.update({key: other[key]})
                else:
                    if not isinstance(self[key], list):
                        self[key] = list(self[key])
                    if isinstance(other[key], (list, tuple)):
                        self[key].extend(other[key])
                    else:
                        self[key].append(other[key])
        elif isinstance(other, (str, int, float)):
            key = list(self.items())[0][0]  # [0]= first item, [0] = key
            self[key].append(other)
        elif isinstance(other, (list, n0list, tuple)):
            key = list(self.items())[0][0]  # [0]= first item, [0] = key
            for itm in other:
                if isinstance(itm, (list, tuple)):
                    self[key].extend(itm)
                else:
                    self[key].append(itm)
        else:
            raise Exception("Unexpected type of other: " + str(type(other)))
        return self

    # ******************************************************************************
    # * n0dict. compare(..)
    # ******************************************************************************
    def compare(
            self,
            other: n0dict,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",

            continuity_check="continuity_check",  # After this argument, other MUST be defined only with names
            one_of_list_compare=n0list.compare,
            # ONLY FOR COMPLEX COMPARE
            # Strictly recommended to init lists
            # else in case of just only one attribute of element will be different
            # both elements will be marked as not found (unique) inside the opposite list
            composite_key: tuple = (),  # ()|None|empty mean all
            compare_only: tuple = (),  # ()|None|empty mean all
            exclude: tuple = (),  # ()|None|empty mean nothing to exclude
            transform: tuple = (),  # ()|None|empty mean nothing to transform
    ) -> n0dict:
        if continuity_check != "continuity_check":
            raise Exception("n0dict. compare(..): incorrect order of arguments")
        if not isinstance(other, n0dict):
            raise Exception("n0dict. compare(..): other (%s) must be n0dict" % str(other))
        result = n0dict({
            "messages": [],
            "not_equal": [],
            "self_unique": [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        self_keys = list(self.keys())
        self_not_exist_in_other = list(self.keys())
        other_not_exist_in_self = list(other.keys())

        # #############################################################
        # NEVER fetch data from the mutable list in the loop !!!
        # #############################################################
        for key in self_keys:
            if key in other:
                # fullxpath = prefix + "/" + key
                fullxpath = "%s/%s" % (prefix, key)
                # n0debug("fullxpath")
                if not xpath_match(fullxpath, exclude):
                    # --- TRANSFORM: START -------------------------------------
                    # Transform self and other linked values with function transform[]()
                    self_value = self[key]
                    other_value = other[key]
                    # n0debug("transform")
                    transform_i = xpath_match(fullxpath, [itm[0] for itm in transform])
                    # n0debug("transform_i")
                    if transform_i:
                        transform_i -= 1
                        transform_self = transform[transform_i][1]
                        if len(transform[transform_i]) > 2:
                            transform_other = transform[transform_i][2]
                        else:
                            transform_other = transform_self
                        self_value = transform_self(self_value)
                        other_value = transform_other(other_value)
                    # --- TRANSFORM: END ---------------------------------------
                    if type(self_value) == type(other_value):
                        if isinstance(self_value, (str, int, float, date)):
                            # if self_value != other_value:
                            if self_value != other_value \
                                and (not compare_only or xpath_match(fullxpath, compare_only)):
                                # VERY IMPORTANT TO SHOW ORIGINAL VALUES, NOT TRANSFORMED
                                result["not_equal"].append(
                                    (
                                        "%s/%s" % (prefix, key),
                                        [
                                            self[key],
                                            other[key]
                                        ]
                                    )
                                )
                                if get__flag_compare_return_difference_of_values():
                                    try:
                                        difference = round(float(other_value) - float(self_value), 7)
                                    except ValueError:  # self_value or other_value could not be converted to float
                                        difference = None
                                    result["not_equal"][-1][1].append(difference)
                                result["messages"].append(
                                    "Values are different: %s[\"%s\"]=%s != %s[\"%s\"]=%s " %
                                    (
                                        self_name, key, self[key],
                                        other_name, key, other[key]
                                    )
                                )
                        elif isinstance(self[key], (list, tuple)):
                            result.update_extend(
                                one_of_list_compare(
                                    n0list(self[key]),
                                    n0list(other[key]),
                                    '%s["%s"]' % (self_name, key),
                                    '%s["%s"]' % (other_name, key),
                                    "%s/%s" % (prefix, key),
                                    composite_key=composite_key, compare_only=compare_only,
                                    exclude=exclude, transform=transform,
                                )
                            )
                        elif isinstance(self[key], (dict, OrderedDict)):
                            result.update_extend(
                                n0dict(self[key]).compare(
                                    n0dict(other[key]),
                                    '%s["%s"]' % (self_name, key),
                                    '%s["%s"]' % (other_name, key),
                                    "%s/%s" % (prefix, key),
                                    one_of_list_compare=one_of_list_compare,  # Only for n0dict. compare()
                                    composite_key=composite_key, compare_only=compare_only,
                                    exclude=exclude, transform=transform,
                                )
                            )
                        elif self[key] is None:
                            # type(self[key]) == type(other[key]) and self[key] is None
                            # So both are None
                            pass
                        else:
                            raise Exception("Not expected type %s in %s[\"%s\"]" % (type(self[key]), key, self_name))
                    else:
                        if not compare_only or xpath_match(fullxpath, compare_only):
                            if get__flag_compare_check_different_types():
                                result["difftypes"].append(
                                    (
                                        prefix + "/" + str(key),
                                        (
                                            type(self[key]), self[key],
                                            type(other[key]), other[key]
                                        )
                                    )
                                )
                                result["messages"].append(
                                    "*Types are different: %s[\"%s\"]=(%s)%s != %s[\"%s\"]=(%s)%s" %
                                    (
                                        self_name, key, type(self[key]), str(self[key]),
                                        other_name, key, type(other[key]), str(other[key]),
                                    )
                                )
                            else:
                                result["not_equal"].append((prefix + "/" + key, (self[key], other[key])))
                                result["messages"].append(
                                    "Values are different: %s[\"%s\"]=%s != %s[\"%s\"]=%s " %
                                    (
                                        self_name, key, self[key],
                                        other_name, key, other[key]
                                    )
                                )
                self_not_exist_in_other.remove(key)
                other_not_exist_in_self.remove(key)

        if self_not_exist_in_other:
            for key in self_not_exist_in_other:
                fullxpath = "%s/%s" % (prefix, key)
                if not xpath_match(fullxpath, exclude) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    result["messages"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            self_name,
                            key,
                            str(self[key]),
                            other_name
                        )
                    )
                    result["self_unique"].append((fullxpath, self[key]))
        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                fullxpath = "%s/%s" % (prefix, key)
                if not xpath_match(fullxpath, exclude) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    result["messages"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            other_name,
                            key,
                            str(other[key]),
                            self_name
                        )
                    )
                    result["other_unique"].append((fullxpath, other[key]))
        return result

    # ******************************************************************************
    # * n0dict. direct_compare(..)
    # ******************************************************************************
    def direct_compare(
            self,
            other: n0dict,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",

            continuity_check="continuity_check",
            # After this argument, other MUST be defined only with names
            one_of_list_compare=n0list.direct_compare,
            # ONLY FOR COMPLEX COMPARE
            # Strictly recommended to init lists
            # else in case of just only one attribute of element will be different
            # both elements will be marked as not found (unique) inside the opposite list
            composite_key: tuple = (),  # None/empty means all
            compare_only: tuple = (),  # None/empty means all
            exclude: tuple = (),  # ()|None|empty mean nothing to exclude
            transform: tuple = (),  # ()|None|empty mean nothing to transform
    ) -> n0dict:
        if continuity_check != "continuity_check":
            raise Exception("n0dict. direct_compare(..): incorrect order of arguments")
        return self.compare(
            other,
            self_name, other_name, prefix,
            one_of_list_compare=one_of_list_compare,  # Only for n0dict. compare()
            composite_key=composite_key, compare_only=compare_only,
            exclude=exclude, transform=transform,
        )
    # ******************************************************************************
    # XPATH
    # ******************************************************************************
    def __xpath(self, value, path: str = None, mode: int = None) -> list:
        """
        Private function: recursively collect elements xpath starts from parent
        """
        result = []
        if isinstance(value, (list, tuple, n0list)):
            for i, subitm in enumerate(value):
                result += self.__xpath(subitm, "%s[%d]" % (path, i), mode)
        elif isinstance(value, (dict, OrderedDict, n0dict)):
            for key, value in value.items():
                result += self.__xpath(value, "%s/%s" % (path, key), mode)
        elif isinstance(value, (str, int, float)) or value is None:
            result.append((path, value))
        else:
            raise Exception("Not expected type (%s) %s/%s == %s" % (type(value), path, key, str(value)))
        return result

    def xpath(self, mode: int = None) -> list:  # list[(xpath, value)]
        """
        Public function: collect elements xpath starts from root
        """
        return self.__xpath(self, "/", mode)

    def to_xpath(self, mode: int = None) -> str:
        """
        Public function: collect elements xpath starts from root and print with indents
        """
        result = ""
        xpath_list = self.xpath(mode)
        xpath_maxlen = max(len(itm[0]) for itm in xpath_list) + 2  # plus 2 chars '"]'
        for itm in xpath_list:
            result += ("['%-" + str(xpath_maxlen) + "s = %s\n") % \
                        (
                            itm[0] + "']",  # Don't move to the main
                            ('"' + str(itm[1]) + '"') if itm[1] else "None"
                        )
        return result

    # ******************************************************************************
    # XML
    # ******************************************************************************
    def __xml(self, parent: n0dict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export OrderedDict into xml result string
        """
        result = ""
        if not parent is None:
            # type_parent = type(parent)
            # type_parent_str = str(type_parent)
            if isinstance(parent, (dict, OrderedDict, n0dict)):
                if not len(parent.items()):
                    # return None
                    return ""
                for key, value in parent.items():
                    if result:
                        result += "\n"
                    if isinstance(value, (list, tuple, n0list)):
                        for i, subitm in enumerate(value):
                            if i:
                                result += "\n"
                            sub_result = self.__xml(subitm, indent + inc_indent, inc_indent)
                            if not sub_result:
                                if isinstance(sub_result, str):
                                    result += " " * indent + "<%s></%s>" % (key,key)
                                else:
                                    result += " " * indent + "<%s/>" % key
                            else:
                                if '>' in sub_result:
                                    result += (" " * indent + "<%s>\n%s\n" + " " * indent + "</%s>") % (key, sub_result, key)
                                else:
                                    result += (" " * indent + "<%s>%s</%s>") % (key, sub_result, key)
                    elif isinstance(value, (str, int, float)):
                        result += " " * indent + ("<%s>%s</%s>" % (key, str(value), key))
                    elif isinstance(value, (dict, OrderedDict, n0dict)):
                        sub_result = self.__xml(value, indent + inc_indent, inc_indent)
                        # if "\n" in sub_result: sub_result = "\n" + sub_result
                        if sub_result:
                            sub_result = "\n" + sub_result
                        if sub_result:
                            result += (" " * indent + "<%s>%s\n" + " " * indent + "</%s>") % (key, sub_result, key)
                        else:
                            result += " " * indent + "<%s/>" % key
                    elif value is None:
                        result += " " * indent + "<%s/>" % key
                    else:
                        raise Exception("__xml(..): Unknown type (%s) %s ==  %s" % (type(value), key, str(value)))
            elif isinstance(parent, (list, tuple, n0list)):
                if not len(parent):
                    return None
                for i, itm in enumerate(parent):
                    if i:
                        result += "\n"
                    result += self.__xml(itm, indent + inc_indent, inc_indent)
            elif isinstance(parent, (str, int, float)):
                result += str(parent)
            else:
                print("Exception")
                raise Exception("__xml(..): Unknown type (%s) ==  %s" % (type(parent), str(parent)))

            return result
        else:
            # return None
            return ""

    def to_xml(self, indent: int = 4, encoding: str = "utf-8") -> str:
        """
        Public function: export self into xml result string
        """
        result = ""
        if encoding:
            result = "<?xml version=\"1.0\" encoding=\"%s\"?>\n" % encoding

        for key in self:
            value = self[key]
            if isinstance(value, (list, tuple, n0list)):
                if len(value):
                    for i, subitm in enumerate(value):
                        result += "<%s>" % key
                        sub_result = self.__xml(subitm, indent, indent)
                        if '<' in sub_result:
                            sub_result = '\n' + sub_result + '\n'
                        result += sub_result + "</%s>\n" % key
                else:
                    result += "<%s/>\n" % key
            else:
                if value is None:
                    result += "</%s>" % key
                else:
                    result += "<%s>" % key
                    if isinstance(value, (str, int, float)):
                        # buffer += "<%s>%s</%s>\n" % (key, str(value), key)
                        result += "%s" % str(value)
                    else:
                        result += "\n" + self.__xml(value, indent, indent) + "\n"
                    result += "</%s>\n" % key
        return result

    # ******************************************************************************
    # JSON
    # ******************************************************************************
    def __json(self, parent: OrderedDict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export OrderedDict into json result string
        """
        result = ""
        for key, value in parent.items():
            if result:
                result += ",\n"
            if isinstance(value, list):
                sub_result = ""
                for i, subitm in enumerate(value):
                    if sub_result:
                        sub_result += ",\n"
                    sub_sub_result = self.__json(subitm, indent + inc_indent * 2, inc_indent)
                    if sub_sub_result:
                        if isinstance(subitm, (dict, OrderedDict, n0dict)):
                            sub_result += (" " * (indent + inc_indent) + "{\n%s\n" + " " * (
                                    indent + inc_indent) + "}") % sub_sub_result
                        elif isinstance(subitm, (list, tuple, n0list)):
                            sub_result += (" " * (indent + inc_indent) + "[\n%s\n" + " " * (
                                    indent + inc_indent) + "]") % sub_sub_result
                if sub_result:
                    result += (" " * indent + "\"%s\": [\n%s\n" + " " * indent + "]") % (key, sub_result)
                else:
                    result += " " * indent + "\"%s\": null" % key
            elif isinstance(value, str):
                result += " " * indent + ("\"%s\": \"%s\"" % (key, value))
            elif isinstance(value, (n0dict, dict, OrderedDict)):
                sub_result = self.__json(value, indent + inc_indent, inc_indent)
                if sub_result:
                    result += (" " * indent + "\"%s\": {\n%s\n" + " " * indent + "}") % (key, sub_result)
                else:
                    result += " " * indent + "\"%s\": null" % key
            elif value is None:
                result += " " * indent + "\"%s\": null" % key
            else:
                raise Exception("Unknown type (%s) %s ==  %s" % (type(value), key, str(value)))
        return result

    def to_json(self, indent: int = 4) -> str:
        """
        Public function: export self into json result string
        """
        return n0pretty(self, show_type=False)

    # ******************************************************************************
    # ******************************************************************************
    def isExist(self, xpath) -> n0dict:
        """
        Public function: return empty lists in dict, if self[xpath] exists
        """
        validation_results = n0dict({
            "messages": [],
            "not_equal": [],
            "self_unique": [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            validation_results.update({"difftypes": []})

        # TO DO: redo with 'in'
        try:
            if self[xpath]:
                return validation_results
        except:
            pass
        validation_results["messages"].append("[%s] doesn't exist" % xpath)
        validation_results["other_unique"].append((xpath, None))
        return validation_results
    # ******************************************************************************
    def is_exist(self, xpath) -> bool:
        """
        Public function: return True, if self[xpath] exists
        """
        # TO DO: redo with 'in'
        try:
            if self[xpath]:
                return True
        except:
            return False
    # ******************************************************************************
    # ******************************************************************************
    def has_all(self,tupple_of_keys):
        for key in tupple_of_keys:
            if key not in self:
                return False
            else:
                if self[key] is None:
                    return False
                if isinstance(self[key],(str,tuple,list,set,frozenset,dict,OrderedDict,n0dict)) and len(self[key]) == 0:
                    return False
        return True
    # ******************************************************************************
    # ******************************************************************************
    def has_any_of(self,tupple_of_keys):
        for key in tupple_of_keys:
            if key in self:
                return True
        return True
    # ******************************************************************************
    # ******************************************************************************
    # ******************************************************************************
    # ******************************************************************************
    def isEqual(self, xpath, value):
        """
        Public function: return empty lists in dict, if self[xpath] == value
        """
        validation_results = self.isExist(xpath)
        if notemptyitems(validation_results):
            return validation_results
        try:
            if self[xpath] == value:
                return []
        except:
            pass
        validation_results["messages"].append("[%s]=='%s' != '%s'" % (xpath, self[xpath], value))
        validation_results["not_equal"].append((xpath, (self[xpath], value)))
        return validation_results

    # ******************************************************************************
    # ******************************************************************************
    def isTheSame(self, xpath, other_n0dict, other_xpath=None, transformation=lambda x: x):
        """
        Public function: return empty lists in dict, if transformation(self[xpath]) == transformation(other_n0dict[other_xpath])
        """
        if not other_xpath:
            other_xpath = xpath
        validation_results = self.isExist(xpath).update_extend(other_n0dict.isExist(other_xpath))
        if notemptyitems(validation_results):
            return validation_results
        try:
            if transformation(self[xpath]) == transformation(other_n0dict[other_xpath]):
                return validation_results
        except:
            # n0print("EXCEPTION in 'if transformation(self[xpath]) == transformation(other_n0dict[other_xpath]):'")
            pass
        validation_results["messages"].append("[%s]=='%s' != [%s]=='%s'" % (
            xpath, transformation(self[xpath]),
            other_xpath, transformation(other_n0dict[other_xpath])
        )
                                              )
        validation_results["not_equal"].append((xpath, (self[xpath], other_n0dict[other_xpath])))
        return validation_results
    # **********************************************************************************************
    # n0dict _find
    # **********************************************************************************************
    def _find(self, xpath_list: list, parent_node, return_lists, xpath_found_str: str = "/") -> list:
        """
        [0] = parent node: n0dict/n0list
        [1] = node_name_index: str (or key or index)
        [2] = cur_value = None if not_found_xpath_list not is None
        [3] = found_xpath_str: str = "" if nothing found
        [4] = not_found_xpath_list: list = None if initial xpath_list is found
        """
        if isinstance(xpath_list, str):
            xpath_list = [itm.strip() for itm in xpath_list.replace("][","]/[").split('/') if itm]
        if not isinstance(xpath_list, (list, tuple)):
            raise IndexError("xpath (%s)'%s' must be list or string" % (type(xpath_list), str(xpath_list)))
        if not xpath_list:
            if xpath_found_str == '/':
                #================================
                # FOUND: root
                #================================
                return parent_node, None, parent_node, xpath_found_str, None
            else:
                return self._find(xpath_found_str, self, return_lists)
            # raise IndexError("too much '..' in xpath")
        # if parent_node is None:
            # parent_node = self

        node_name, node_index = split_name_index(xpath_list[0])
        # ##########################################################################################
        # Key in n0dict
        # ##########################################################################################
        if node_name:
            # ..................................................................
            # Surfacing if /..
            # ..................................................................
            if node_name == "..":
                cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                    cur_not_found_xpath_list = self._find(
                        # '..' is already not included into xpath_found_str, so just remove only last node
                        [itm for itm in xpath_found_str.split('/') if itm][:-1],
                        self,
                        return_lists
                    )
                if cur_node_name_index:
                    cur_node_name, cur_node_index = split_name_index(cur_node_name_index)
                    if cur_node_name:
                        nxt_parent_node = cur_parent_node[cur_node_name]
                    else:
                        # n0debug("cur_node_name_index")
                        # n0debug("cur_node_name")
                        # n0debug("cur_node_index")
                        # n0debug("cur_parent_node")
                        nxt_parent_node = cur_parent_node[n0eval(cur_node_index)]
                else:
                    nxt_parent_node = cur_parent_node

                if node_index or len(xpath_list) > 1:
                    if node_index:
                        return self._find(["[%s]" % node_index] + xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
                    else:
                        return self._find(                        xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
                else:
                    # ================================
                    # FOUND: the last is n0dict
                    # ================================
                    return cur_parent_node, cur_node_name_index, nxt_parent_node, xpath_found_str + '/' + cur_node_name_index, None
            # ..................................................................
            # Try to parse as list
            # ..................................................................
            if isinstance(parent_node, (list, tuple, n0list)):
                # *******************************
                # Indulge #1 for incorrect syntax -- [*] was skipped for list in xpath
                # *******************************
                return self._find(["[*]"] + xpath_list, parent_node, return_lists, xpath_found_str)
            if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                raise IndexError("If key '%s' is set then (%s)'%s' must be n0dict at '%s'" %
                    (node_name, type(parent_node), str(parent_node), xpath_found_str)
                )
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            if node_name == "*":
                # cur_values = n0list([])
                cur_values = n0list()
                fst_parent_node = fst_node_name_index = fst_value = fst_found_xpath_str = None
                for next_node_name in parent_node:
                    cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                        cur_not_found_xpath_list = self._find([next_node_name] + new_xpath_list, return_lists, parent_node, found_xpath_str)
                    if not cur_not_found_xpath_list:
                        cur_values.append(cur_value)
                        if not fst_found_xpath_str:
                            fst_parent_node, fst_node_name_index, fst_value, fst_found_xpath_str = \
                                cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str
                if not return_lists and len(cur_values) == 1:
                    cur_values = cur_values[0]
                if fst_found_xpath_str:
                    return fst_parent_node, fst_node_name_index, cur_values, fst_found_xpath_str,   None
                else:
                    # #--------------------------------
                    # # NOT FOUND in all [*] items
                    # #--------------------------------
                    return parent_node,     None,               None,       xpath_found_str,        xpath_list
            # ..................................................................
            # Check key in dictionary
            # ..................................................................
            if not node_name in parent_node:
                #--------------------------------
                # NOT FOUND: Node name in n0dict
                #--------------------------------
                # Expected not found [text()='']/../
                if isinstance(node_index, tuple) and \
                   node_index[0] == "text()" and node_index[1][1] in "=~" and node_index[2] == "" and \
                   len(xpath_list) >= 2 and xpath_list[1] == '..':
                    return self._find(xpath_list[2:], parent_node, return_lists, xpath_found_str)
                else:
                    return parent_node, None, None, xpath_found_str, xpath_list
            if len(xpath_list) == 1 and node_index is None:
                #================================
                # FOUND: the last is n0dict
                #================================
                return parent_node, node_name, parent_node[node_name], xpath_found_str + '/' + node_name, None
            #*******************************
            # Deeper
            #*******************************
            if node_index is None:
                return self._find(
                                    xpath_list[1:],
                                    parent_node[node_name],
                                    return_lists,
                                    xpath_found_str + '/' + node_name
                )
            else:
                return self._find(
                                    [
                                        "[%s%s'%s']" % (node_index[0], node_index[1], node_index[2]) \
                                        if isinstance(node_index,tuple) else \
                                        "[%s]" % node_index
                                    ] + xpath_list[1:],
                                    parent_node[node_name],
                                    return_lists,
                                    xpath_found_str + '/' + node_name
                )
        # ##########################################################################################
        # Index in n0list (node_index is not None)
        # ##########################################################################################
        else:
            #--------------------------------
            # NOT FOUND: new element in n0list
            #--------------------------------
            if node_index == "new()":
                parent_node, node_name_index, cur_value, found_xpath_str, \
                    not_found_xpath_list = self._find(xpath_found_str, self, return_lists)
                if not isinstance(parent_node[node_name_index], (list, tuple, n0list)):
                    parent_node[node_name_index] = n0list([parent_node[node_name_index]])
                return parent_node[node_name_index], None, None, xpath_found_str, ["[new()]"] + xpath_list[1:]
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            elif node_index == "*":
                if not isinstance(parent_node, (list, tuple, n0list)):
                    # Hidden list. Convert single item into list
                    parent_node = [parent_node]
                # cur_values = n0list([])
                cur_values = n0list()
                fst_parent_node = fst_node_name_index = fst_value = fst_found_xpath_str = None
                for i,cur_node in enumerate(parent_node):
                    cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                        cur_not_found_xpath_list = self._find(["[%d]" % i] + xpath_list[1:], parent_node, return_lists, xpath_found_str)
                    if not cur_not_found_xpath_list:
                        cur_values.append(cur_value)
                        if not fst_found_xpath_str:
                            fst_parent_node, fst_node_name_index, fst_value, fst_found_xpath_str = \
                                cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str
                if not return_lists and len(cur_values) == 1:
                    cur_values = cur_values[0]
                if fst_found_xpath_str:
                    return fst_parent_node, fst_node_name_index, cur_values, fst_found_xpath_str,   None
                else:
                    # #--------------------------------
                    # # NOT FOUND in all [*] items
                    # #--------------------------------
                    return parent_node,     None,               None,       xpath_found_str,        xpath_list


            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Conditions: parent is expected to be dictionary (or possible list)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # elif '=' in node_index:
            elif isinstance(node_index, tuple):
                if node_index[0] == 'text()':
                    if isinstance(parent_node, int):
                        node_index[2] = int(node_index[2])
                    elif isinstance(parent_node, float):
                        node_index[2] = float(node_index[2])
                        
                    if node_index[1][1] == '=':
                        comparing_result = parent_node == node_index[2]  # expected_value
                    elif node_index[1][1] == '~':
                        comparing_result = node_index[2] in parent_node  # expected_value
                    else:
                        raise Exception ("Unknown comparing command in %s" % node_index)
                        
                    if node_index[1][0] == '!':
                        comparing_result = not comparing_result
                    elif node_index[1][0] != '=' and node_index[1][0] != '~':
                        raise Exception ("Unknown comparing command in %s" % node_index)
                        
                    if comparing_result:
                        # *******************************
                        # Deeper
                        # *******************************
                        return self._find(xpath_list[1:], parent_node, return_lists, xpath_found_str)
                    else:
                        #--------------------------------
                        # NOT FOUND: value is not expected
                        #--------------------------------
                        return parent_node, None, None, xpath_found_str, xpath_list
                else:
                    if isinstance(parent_node, (list, tuple, n0list)) and len(parent_node):
                        # *******************************
                        # Not correct: indulge #2 in incorrect syntax -- [*] was skipped for list in xpath
                        # *******************************
                        return self._find(["[*]"] + xpath_list, parent_node, return_lists, xpath_found_str)

                    if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                        raise IndexError("If key '%s' is set then (%s)'%s' must be n0dict at '%s'" %
                            (node_index[0], type(parent_node), str(parent_node), xpath_found_str)
                        )
                    if not node_index[0] in parent_node:
                        return parent_node, None, None, xpath_found_str, xpath_list

                    return self._find(
                                        ["[text()%s%s]" % (node_index[1], node_index[2]), ".."] + xpath_list[1:],
                                        parent_node[node_index[0]],
                                        return_lists,
                                        xpath_found_str + '/' + node_index[0]
                    )
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Pure index
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            else:
                try:
                    node_index = n0eval(node_index)
                except:
                    raise IndexError("Unknown index '%s[%s]'" % (xpath_found_str, node_index))

                if isinstance(parent_node, (list, tuple, n0list)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index >= len__parent_node or node_index < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, "[%s]" % node_index, None, xpath_found_str, xpath_list
                    # raise IndexError("If we are looking for element of list '%s[%s]', then parent node (%s)'%s' must be list" % (xpath_found_str, node_index, type(parent_node), str(parent_node)))

                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, "[%s]" % node_index, parent_node[node_index], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    return self._find(xpath_list[1:], parent_node[node_index], return_lists, "%s[%s]" % (xpath_found_str, node_index))
    # **********************************************************************************************
    # **********************************************************************************************
    def _get(self, xpath: str, raise_exception = True, if_not_found = None, return_lists = True):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if xpath.startswith('?'):
            xpath = xpath[1:]
            raise_exception = False
            if_not_found = ''
        if any(char in xpath for char in "/["):
            parent_node, node_name_index, cur_value, found_xpath_str, not_found_xpath_list = self._find(xpath, self, return_lists)
            if not not_found_xpath_list:
                return cur_value
            else:
                if raise_exception:
                    raise IndexError("not found '%s' in '%s'" % ('/'.join(not_found_xpath_list), found_xpath_str))
                else:
                    return if_not_found
        else:
            try:
                return super(n0dict, self).__getitem__(xpath)
            # except IndexError as ex:
            except KeyError as ex:
                if raise_exception:
                    raise ex
                else:
                    return if_not_found
    # ******************************************************************************
    # ******************************************************************************
    def __getitem__(self, xpath):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        return self._get(xpath, raise_exception = True)
    # ******************************************************************************
    # ******************************************************************************
    def get(self, xpath: str, if_not_found = None):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # **********************************************************************************************
    # **********************************************************************************************
    def first(self, xpath: str, if_not_found = None):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        If self[where1/where2/.../whereN] is list, thet the first element will be returned
        """
        result = self._get(xpath, raise_exception = False, if_not_found = if_not_found, return_lists = False)
        if isinstance(result, (list, tuple, n0list)) and len(result) == 1:
            result = result[0]
        return result
    # **********************************************************************************************
    # **********************************************************************************************
    def _add(self, parent_node, node_name_index: str, xpath_list: list) -> str:
        if node_name_index:
            # or cur_node_name OR cur_node_index MUST have value, both could NOT have values
            cur_node_name, cur_node_index = split_name_index(node_name_index)
        else:
            # If BOTH are empty, just add new element into dictionary parent_node
            cur_node_name, cur_node_index = None, None

        next_node_name, next_node_index = split_name_index(xpath_list[0])  # possible both could be NOT empty

        # if not cur_node_index is None:
        if cur_node_index is None:
            ####################################################################
            # Parent is DICTIONARY
            ####################################################################
            if cur_node_name:
                if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                    raise IndexError("If we are looking for key '%s' then parent (%s)'%s' must be dictionary"
                                     % (cur_node_name, type(parent_node), str(parent_node)))
                parent_node = parent_node[cur_node_name]
            else:
                # It could happen, then just to add key into dictionary
                pass

            if next_node_name:
                if not next_node_name in parent_node:
                    # New node
                    if next_node_index:
                        if next_node_index != "new()":
                            raise Exception("Nonsence! Impossible to add %s[%s] to the list (%s)%s"
                                            % (cur_node_name, cur_node_index, type(parent_node), str(parent_node)))
                        # item[0] == None, will be reused at the next step with last()
                        parent_node.update({next_node_name: n0list([None])})
                        next_node = parent_node[next_node_name]
                        # next_node_name_index = "[%s]" % next_node_index
                        next_node_name_index = "[last()]"
                    else:
                        parent_node.update({next_node_name: n0dict({})})
                        next_node = parent_node
                        next_node_name_index = next_node_name
                else:
                    # Node is EXISTED
                    if next_node_index:
                        parent_node.update({next_node_name: [parent_node[next_node_name]]})
                        next_node = parent_node[next_node_name]
                        next_node_name_index = "[%s]" % next_node_index
                    else:
                        raise IndexError("Nonsense! How to create already existed node '%s'?" % next_node_name)
            else:
                if next_node_index != "new()":
                    raise IndexError("Expect new() for adding index, but got '%s'" % next_node_index)
                parent_node.append(None)
                next_node = parent_node
                next_node_name_index = "[last()]"
        else:
            ####################################################################
            # Parent is LIST or should be a list
            ####################################################################
            if cur_node_index == "new()":
                if not isinstance(parent_node[cur_node_name], (list, tuple, n0list)):
                    ####################################################################
                    # Convert not LIST into the list
                    ####################################################################
                    if len(parent_node[cur_node_name]):
                        parent_node.update({cur_node_name: n0list([parent_node[cur_node_name]])})
                    else:
                        # parent_node.update({cur_node_name: n0list([])})
                        parent_node.update({cur_node_name: n0list()})
                    parent_node = parent_node[cur_node_name]
                if next_node_name:
                    if not next_node_index:
                        # Next is pure dict
                        parent_node.append(n0dict({next_node_name: n0dict({})}))
                        next_node = parent_node[-1]
                        next_node_name_index = next_node_name
                    else:
                        # Next is list under dict
                        # parent_node.append(n0dict({next_node_name: n0list([])}))
                        parent_node.append(n0dict({next_node_name: n0list()}))
                        next_node = parent_node[-1][next_node_name]
                        # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                        next_node_name_index = "[%s]" % next_node_index
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = "[%s]" % next_node_index
                else:
                    raise Exception("Nonsence! Both next_node_name and next_node_index could NOT be empty")
            if cur_node_index == "last()":
                # Came from previous level: we create [None] and point to [last()] for exchange
                if not isinstance(parent_node, (list, tuple, n0list)):
                    raise Exception("Nonsence! if index '%s' is set then (%s)%s must be n0list"
                                    % (cur_node_index, type(parent_node), str(parent_node)))
                if next_node_name:
                    if not next_node_index:
                        # Next is pure dict
                        parent_node[-1] = n0dict({next_node_name: n0dict({})})
                        next_node = parent_node[-1]
                        next_node_name_index = next_node_name
                    else:
                        # Next is list under dict
                        # parent_node[-1] = n0dict({next_node_name: n0list([])})
                        parent_node[-1] = n0dict({next_node_name: n0list()})
                        next_node = parent_node[-1][next_node_name]
                        # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                        next_node_name_index = "[%s]" % next_node_index
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = "[%s]" % next_node_index
            else:
                raise Exception("Nonsence! Impossible to add %s[%s] to the list (%s)%s"
                                % (cur_node_name, cur_node_index, type(parent_node), str(parent_node)))

        if len(xpath_list) == 1:
            return next_node, next_node_name_index
        else:
            return self._add(next_node, next_node_name_index, xpath_list[1:])
    # **********************************************************************************************
    # **********************************************************************************************
    def __setitem__(self, xpath: str, new_value):
        """
        Private function:
        self[where1/where2/.../whereN] = value
            AKA
        self[where1][where2]...[whereN] = value

        if xpath will be started with ?, the nothing will be done if new_value is None or empty
        if xpath is exist, then the value will be overwritten
        if not exist, then the node will be created

        could be used predicates:
            [<item>=<value>]
            [<item>='<value>']
        or indexes
            [0]
            [1]
            [2]
            [-1]
            [-2]
            [-3]
        or functions
            [last()]
            [last()-1]
            [last()-2]
        or commands for creating (convertion into list) new node
            [new()]
        """
        if xpath.startswith('?'):
            if new_value is None or (isinstance(new_value, str) and new_value == ""):
                return None
            xpath = xpath[1:]

        if any(char in xpath for char in "/["):
            parent_node, node_name_index, cur_value, found_xpath_str, not_found_xpath_list = self._find(xpath, self, return_lists = True)
            if not_found_xpath_list:
                parent_node, node_name_index = self._add(parent_node, node_name_index, not_found_xpath_list)

            node_name, node_index = split_name_index(node_name_index)
            if isinstance(parent_node, (dict, OrderedDict, n0dict)):
                if node_index:
                    raise Exception("How is it possible: index '%s' for dictionary (%s)'%s'?"% (node_index, type(parent_node), parent_node))
                parent_node.update({node_name_index: new_value})
            elif isinstance(parent_node, (list, tuple, n0list)):
                if node_name:
                    raise Exception("How is it possible: key '%s' for list (%s)'%s'?" % (node_name, type(parent_node), parent_node))
                parent_node[n0eval(node_index)] = new_value
            else:
                raise Exception("How is it possible: unknown type of parent node (%s) of '%s'" % (type(parent_node), parent_node))
        else:
            super(n0dict, self).__setitem__(xpath, new_value)

        return new_value  # For speed
    # ******************************************************************************
    # ******************************************************************************
    def _valid(self, validate, valid_is_expected: bool):
        for itm in self:
            if validate(itm) == valid_is_expected:
                return True
        return False
    # ******************************************************************************
    def any_valid(self, validate):
        return self._consists_of(validate, True)
    # ******************************************************************************
    def any_not_valid(self, validate):
        return self._consists_of(validate, False)
    # ******************************************************************************
    def all_valid(self, validate):
        return not self._consists_of(validate, False)
    # ******************************************************************************
    def all_not_valid(self, validate):
        return not self._consists_of(validate, True)
    # ******************************************************************************
    def valid(self, node_xpath:str, validate, expected_result_for_error: bool = False, msg:str = None):
        """
        :param node_xpath:
            xpath to the node inside self
        :param validate:
            list/scalar/function = validation
        :param expected_result_for_error:
            By default expected that if result of validation is True, then self[node_xpath] is not valid (return False)
        :param msg:
            if None => return result as bool True(validation)/False
        :return:

        Examples:
            xml.valid('node/subnode', ["",None], True, "ERROR")
                If xml['node/subnode'] is equal "" or None (result of comparising is True), then return ERROR, else ""
            xml.valid('node/subnode', ["",None], True)
                If xml['node/subnode'] is equal "" or None (result of comparising is True), then return False (not valid), else True
            xml.valid('node/subnode', "", True)
                If xml['node/subnode'] is equal "" (result of comparising is True), then return False (not valid), else True
            xml.valid('node/subnode', [1,2], False, "ERROR")
                If xml['node/subnode'] is not equal 1 or 2 (result of comparising is False), then return ERROR, else ""
            xml.valid('node/subnode', [1,2], False)
                If xml['node/subnode'] is not equal 1 or 2 (result of comparising is False), then return False (not valid), else True
            xml.valid('node/subnode', [1,2])
                If xml['node/subnode'] is not equal 1 or 2 (result of comparising is False), then return False (not valid), else True
        """
        try:
            node_value = self.get(node_xpath)
            if callable(validate):
                validate_result = validate(node_value)
            elif isinstance(validate, (list, tuple, n0list)):
                validate_result = node_value in validate
            else:
                validate_result = node_value == validate
        except:
            validate_result = False

        if validate_result == expected_result_for_error:
            if msg is None:
                return False
            else:
                return msg.format(node_xpath, str(node_value))
        else:
            if msg is None:
                return True
            else:
                return ""
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
