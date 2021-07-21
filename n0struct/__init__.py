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
# 0.42 = 2021-01-22
#                   enhanced:
#                       n0debug(..)
#                       mypy optimization
# 0.43 = 2021-01-28
#                   enhanced:
#                       mypy optimization
#                       compare()["messages"] -> compare()["differences"]
#                       compare(exclude=) -> compare(exclude_xpaths=)
#                   added:
#                       def load_file(file_name: str) -> list:
#                       def save_file(file_name: str, lines: typing.Any):
#                       def load_serialized(...):
# 0.44 = 2021-02-08
#                   fixed:
#                       split_name_index(..)
# 0.45 = 2021-02-27
#                   enhanced:
#                       mypy optimization
#                       def init_logger(..)
#                   added:
#                       def timestamp() -> str:
#                       def date_yymmdd(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
#                       class OrderedSet(MutableSet):
#                       def unpack_references(initial_dict: dict, initial_key: str, recursive: bool = True) -> OrderedSet:
#                       class Git():
#                   fixed:
#                       n0list. _get(..)
# 0.45 = 2021-03-05
#                   added:
#                       n0dict. def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> n0dict:
#                       n0dict. def delete(self, xpath: str, recursively: bool = False) -> n0dict:
#                       n0dict. def pop(self, xpath: str, recursively: bool = False) -> typing.Any:
# 0.46 = 2021-07-21 optimized for debugging
from __future__ import annotations  # Python 3.7+: for using own class name inside body of class

import sys
import os
import inspect

# from typing import Any, Union, Dict, Tuple, List, Set, FrozenSet, NewType, Sequence
import typing
# from mypy_extensions import (Arg, DefaultArg, NamedArg, DefaultNamedArg, VarArg, KwArg)
from mypy_extensions import Arg

from datetime import datetime, timedelta, date
import random
from collections import OrderedDict
import xmltodict
import json
# import urllib # expected_value = urllib.parse.unquote(expected_value) # mypy: error: Module has no attribute "parse"
from urllib.parse import unquote as urllib__parse__unquote
import contextlib
from loguru import logger
from logging import StreamHandler
# ********************************************************************
# Used by class Git():
import subprocess
import signal
# ********************************************************************
__flag_compare_check_different_types = False
def set__flag_compare_check_different_types(value: bool):
    """
    if __flag_compare_check_different_types == True, then
    validate type of attributes in .compare()/.direct_compare()
    and return result["difftypes"]
    """
    global __flag_compare_check_different_types
    __flag_compare_check_different_types = value
    return __flag_compare_check_different_types
def get__flag_compare_check_different_types() -> bool:
    global __flag_compare_check_different_types
    return __flag_compare_check_different_types
# ********************************************************************
__flag_compare_return_difference_of_values = False
def set__flag_compare_return_difference_of_values(value: bool):
    """
    if __flag_compare_return_difference_of_values == True, then
    if values of attributes are different and are int,float,
    return additional element in result["not_equal"] with difference
    """
    global __flag_compare_return_difference_of_values
    __flag_compare_return_difference_of_values = value
def get__flag_compare_return_difference_of_values() -> bool:
    global __flag_compare_return_difference_of_values
    return __flag_compare_return_difference_of_values
# ********************************************************************
# ********************************************************************
def n0isnumeric(value: str) -> bool:
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
def n0eval(_str: str) -> typing.Union[int, float, typing.Any]:
    def my_split(_str: str, _separator: str) -> typing.List:
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
                if '.' in item:
                    item = float(item)
                else:
                    item = int(item)
            except Exception:
                return _str
        result += item

    return result
# ********************************************************************
# ********************************************************************
def split_name_index(node_name: str) -> typing.Tuple[
                                                        # typing.Any,
                                                        str,
                                                        typing.Union[
                                                            str,
                                                            typing.Tuple[str, str, typing.Union[str, bool]]
                                                        ]
                                                    ]:
    if not isinstance(node_name, str):
        raise Exception("node_name (%s)%s must be string" % (type(node_name), node_name))

    node_index_tuple = None
    if '[' in node_name and node_name.endswith(']'):
        node_name, node_index_str = node_name[:-1].split('[', 1)
        node_name = node_name.strip()
        node_index_str = node_index_str.strip()
        if isinstance(node_index_str, str):
            if node_index_str != "":
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
                        raise Exception("Never must be happend!")

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
                        # expected_value = urllib.parse.unquote(expected_value) # mypy: error: Module has no attribute "parse"
                        expected_value = urllib__parse__unquote(expected_value)
                    node_index_tuple = (expected_node_name, separator, expected_value or expected_value_bool)
    else:
        node_index_str = None
    return node_name, (node_index_tuple if not node_index_tuple is None else node_index_str)
# ********************************************************************
# ********************************************************************
def date_delta(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> datetime:
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
# ********************************************************************
def date_now(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str 20 characters YYYYMMDDHHMMSSFFFFFF
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y%m%d%H%M%S%f")
# ********************************************************************
def timestamp() -> str:
    """
    :return: now -> str 13 characters YYMMDD_HHMMSS
    """
    return (timestamp := date_now())[2:8] + "_" + timestamp[8:14]
# ********************************************************************
def date_iso(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str ISO date format
    """
    return date_delta(now, day_delta, month_delta).isoformat(timespec='microseconds')
# ********************************************************************
def date_yymmdd(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMMDD
    """
    return date_delta(now, day_delta, month_delta).strftime("%y%m%d")
# ********************************************************************
def date_yyyymmdd(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y-%m-%d")
# ********************************************************************
def date_slash_ddmmyyyy(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD/MM/YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d/%m/%Y")
# ********************************************************************
def date_ddmmyyyy(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD-MM-YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d-%m-%Y")
# ********************************************************************
def date_yymm(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMM
    """
    return date_delta(now, day_delta, month_delta).strftime("%y%m")
# ********************************************************************
def date_mmyy(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str MMYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%m%y")
# ********************************************************************
def from_ddmmmyy(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: DD-MMM-YY # 16-JUL-20
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%d-%b-%y").date()  # 16-JUL-20
    except (ValueError, TypeError):
        return date_str
# ********************************************************************
def from_yyyymmdd(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: YYYY-MM-DD # 2020-07-16
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()  # 2020-07-16
    except (ValueError, TypeError):
        return date_str
# ********************************************************************
def from_ddmmyyyy(date_str: str) -> typing.Union[date, str, None]:
    """
    :param date_str: DD-MM-YYYY # 16-07-2020
    :return: str -> date
    """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()  # 16-07-2020
    except (ValueError, TypeError):
        return date_str
# ********************************************************************
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
def load_file(file_name: str) -> list:
    with open(file_name, 'rt') as inFile:
        return [line.strip() for line in inFile.read().split("\n") if line.strip()]
# ********************************************************************
def save_file(file_name: str, lines: typing.Any):
    if isinstance(lines, (list, tuple)):
        buffer = "\n".join(lines)
    elif isinstance(lines, (str)):
        buffer = lines
    else:
        buffer = str(lines)
    with open(file_name, 'wt') as outFile:
        outFile.write(buffer)
# ********************************************************************
def load_serialized(file_name: str,
                    # /,  # When everybody migrates to py3.8, then we will make it much beautiful
                    equal_tag: str = "=",
                    separator_tag: str = ";",
                    comment_tags: typing.Union[tuple, list] = ("#", "//"),
                    remove_startswith: str = "",
                    remove_endswith: str = ""
                    ) -> n0list:

    result = n0list()

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
            result.append(n0dict())
            # result["root"].append(n0dict())
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
# ********************************************************************
# ********************************************************************
def rnd(till_not_included: int) -> int:
    """
    :param till_not_included:
    :return: int [0..till_not_included)
    """
    return int(random.random() * till_not_included)
# ********************************************************************
def random_from(from_list: list) -> typing.Any:
    """
    :param from_list:
    :return: from_list[rnd]
    """
    return from_list[rnd(len(from_list))]
# ********************************************************************
def get_key_by_value(dict_: dict, value_: typing.Any):
    """
    :param dict_:
    :param value_:
    :return: last key which is associated with value_ in dict_
    """
    return {value: key for key, value in dict_.items()}[value_]
# ********************************************************************
# __prev_end = "\n"
__debug_showobjecttype = True
__debug_showobjectid = True
__main_log_filename = None
def init_logger(
        debug_level: str = "TRACE",
        debug_output = sys.stderr,
        debug_timeformat: str = "YYYY-MM-DD HH:mm:ss.SSS",
        debug_showobjectid = True,
        debug_logtofile = True,
        log_file_name: str = None,
    ):
    logger.level("DEBUG", color="<white>")

    global __main_log_filename
    if debug_logtofile:
        if log_file_name:
            __main_log_filename = log_file_name
        else:
            if not __main_log_filename:
                __main_log_filename = os.path.splitext(os.path.split(inspect.stack()[-1].filename)[1])[0]
            if __main_log_filename == "<string>":
                __main_log_filename = "debuglog"
            __main_log_filename += "_" + timestamp() + ".log"

    global __debug_showobjectid
    __debug_showobjectid = debug_showobjectid

    format = ""
    if debug_timeformat:
        format += "<green>{time:" + debug_timeformat + "}</green>|"
    format += "<level>{level: <8}</level>|<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|<level>{message}</level>"

    handlers = [
        dict(sink = debug_output, level = debug_level, format = format),
    ]
    if debug_logtofile:
        handlers.append(
            dict(sink = __main_log_filename, enqueue = True, level = debug_level, format = format),
        )
    logger.configure(handlers = handlers)
# ********************************************************************
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
    
    '''
    if internal_call:  # Called from n0debug|n0debug_calc|n0debug_object
        try:
            frameinfo = inspect.stack()[3]
        except:
            try:
                frameinfo = inspect.stack()[2]
            except:
                try:
                    frameinfo = inspect.stack()[1]
                except:
                    try:
                        frameinfo = inspect.stack()[0]
                    except:
                        frameinfo = None
    else:
        frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
    '''
    
    logger.opt(depth=1+internal_call).log(level,
        (text if text else "")
    )
# ********************************************************************
def n0pretty(item: typing.Any, indent_: int = 0, show_type:bool = None, __indent_size: int = 4, __quotes:str = '"'):
    """
    :param item:
    :param indent_:
    :return:
    """
    def indent(indent__ = indent_):
        return "\n" + (" " * (indent__ + 1) * __indent_size) if __indent_size else ""

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
                result += __quotes + sub_item + __quotes + ":" + (" " if __indent_size else "")
                sub_item_value = n0pretty(item[sub_item], indent_ + 1, show_type, __indent_size, __quotes)  
                # to mitigate json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes, __quotes == "\""
                if isinstance(sub_item_value, str):
                    sub_item_value = __quotes + sub_item_value + __quotes
                result += sub_item_value
            else:
                result += n0pretty(sub_item, indent_ + 1, show_type, __indent_size, __quotes)
        if show_type or __debug_showobjecttype:
            result_type = str(type(item)) + ("%s%d%s " % (brackets[0], len(item), brackets[1])) + brackets[0]
        else:
            result_type = brackets[0]
        if result and "\n" in result:
            result = result_type + indent() + result + indent(indent_ - 1)
        else:
            result = result_type + result
        result += brackets[1]
    elif isinstance(item, str) and not indent_:
        result = "'" + item.replace("'", "\\'") + "'"
    elif item is None:
        result = 'N0ne'  # json.decoder.JSONDecodeError: Expecting value
    else:
        result = str(item)
    return result
# ******************************************************************************
def n0debug_calc(var_object, var_name: str = "", level: str = "DEBUG", internal_call: int = 0):
    """
    Print  calculated value (for example returned by function),
    depends of value in global variable __debug_level.

    :param var_object:
    :param var_name:
    :param level:
    :return:
    """
    prefix = str(type(var_object)) if __debug_showobjecttype else "" + \
             " id=%s" % id(var_object) if __debug_showobjectid else ""
    if prefix:
        prefix = "(" + prefix + ")"
    
    n0print(
        "%s%s == %s" % (
            prefix,
            var_name,
            n0pretty(var_object)
        ),
        level = level,
        internal_call = internal_call + 1,
    )
# ********************************************************************
def n0debug(var_name: str, level: str = "DEBUG"):
    """
    Print value of the variable with name {var_name},
    depends of value in global variable {__debug_level}.

    :param var_name:
    :param level:
    :return:
    """
    if not isinstance(var_name,str):
        raise Exception("incorrect call of n0debug(..): argument MUST BE string")

    __f_locals = inspect.currentframe().f_back.f_locals
    if not var_name in __f_locals:
        raise Exception("impossible to find object '%s'" % var_name)
    var_object = __f_locals.get(var_name)
    n0debug_calc(var_object, var_name, level = level, internal_call = 1)
# ********************************************************************
def n0debug_object(object_name: str, level: str = "DEBUG"):
    class_object = inspect.currentframe().f_back.f_locals[object_name]
    class_attribs_methods = set(dir(class_object)) - set(dir(object))
    class_attribs = set()
    class_methods = set()
    
    prefix = str(type(class_object)) if __debug_showobjecttype else "" + \
             " id=%s" % id(class_object) if __debug_showobjectid else ""
    if prefix:
        prefix = "(" + prefix + ")"
    to_print = "%s%s = \n" % (prefix, object_name)
    
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
        prefix = str(type(attrib)) if __debug_showobjecttype else "" + \
                 " id=%s" % id(attrib) if __debug_showobjectid else ""
        if prefix:
            prefix = "(" + prefix + ")"
        to_print += "=== %s%s = %s\n" % (prefix, attrib_name, n0pretty(attrib))
        
    n0print(to_print, level = level, internal_call = True)
# ******************************************************************************
strip_ns = lambda key: key.split(':',1)[1] if ':' in key else key
'''
# Sample
currency_converter = {"682": "SAR"}
keys_for_currency_convertion = {
    "currency":         lambda value: currency_converter[value] if value in currency_converter else value,
    "source_currency":  lambda value: currency_converter[value] if value in currency_converter else value,
}
def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = keys_for_currency_convertion):
'''
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
        if n0isnumeric(value):
            return abs(float(value))
        else:
            return value.upper()
    else:
        return value
# ******************************************************************************
def transform_structure(in_structure, transform_key = strip_ns, transform_value = convert_to_native_format):
    if isinstance(in_structure, (dict, OrderedDict, n0dict)):
        in_list = [in_structure]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
    else:
        in_list = in_structure
    if isinstance(in_list, (list, tuple, n0list)):
        out_list = n0list()
        for in_dict in in_list:
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
def xpath_match(xpath: str, xpath_list: typing.Union[str, list, tuple]) -> int:
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
# ******************************************************************************
def generate_composite_keys(
                            input_list: n0list,
                            elements_for_composite_key: tuple,
                            prefix: str = None,
                            transform: typing.List[typing.Tuple[str, typing.Callable[[str], str]]] = []
                            ) -> list:
    """
    serialization all or {elements_for_composite_key} elements of {input_list[]}
    :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
    :return:
        [[<composite_key>,[<index of entry>],...}
    """
    if isinstance(elements_for_composite_key, str):
        elements_for_composite_key = [elements_for_composite_key]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A

    composite_keys_for_all_lines = []
    if transform:
        attributes_to_transform = [itm[0] for itm in transform]
    else:
        attributes_to_transform = []

    for line_i, line in enumerate(input_list):
        if isinstance(line, (dict, OrderedDict, n0dict)):
            created_composite_key = ""
            if elements_for_composite_key:
                for key in elements_for_composite_key:
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
        else:
            raise Exception("generate_composite_keys(..): expected element dict inside list, but got (%s)%s" % (type(line), line))
        composite_keys_for_all_lines.append((created_composite_key, line_i))
    return composite_keys_for_all_lines
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
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
            return None
        raise TypeError("n0list.__init__(..) takes exactly one notnamed argument (list/tuple/n0list)")
    # **************************************************************************
    # n0list. _find()
    # **************************************************************************
    def _find(self,
            xpath_list: typing.Union[str, list],
            parent_node,
            return_lists,
            xpath_found_str: str = "/") \
        ->  typing.Tuple[
                typing.Union[n0dict, n0list, None],
                typing.Union[str, int, None],
                typing.Union[typing.Any, None],
                str,
                typing.Union[list, None]
            ]:
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
            if isinstance(node_index, str):
                node_index_str = node_index
            else:
                raise Exception("Impossible to have complex index for lists")

            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            if node_index_str == "*":
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
                    elif isinstance(next_parent_node, n0list):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = self._find(xpath_list[1:], next_parent_node, return_lists)
                    else:
                        raise Exception("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))

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
                    return parent_node,     None,                None,       xpath_found_str,        xpath_list
            else:
                try:
                    node_index_int = n0eval(node_index_str)
                except:
                    raise IndexError("Unknown index '%s[%s]'" % (xpath_found_str, node_index_str))

                if isinstance(parent_node, (list, tuple, n0list)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index_int >= len__parent_node or node_index_int < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, "[%s]" % str(node_index_int), None, xpath_found_str, xpath_list
                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, "[%s]" % str(node_index_int), parent_node[node_index_int], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    next_parent_node =  parent_node[node_index_int]
                    if isinstance(next_parent_node, n0dict):
                        return n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists, "%s[%d]" % (xpath_found_str, node_index_int))
                    if isinstance(next_parent_node, n0list):
                        return self._find(xpath_list[1:], next_parent_node, return_lists, "%s[%d]" % (xpath_found_str, node_index_int))
                    else:
                        raise Exception("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))
    # **************************************************************************
    # n0list. _get()
    # **************************************************************************
    def _get(self, xpath: typing.Union[str, int], raise_exception = True, if_not_found = None, return_lists = True):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if isinstance(xpath, int):
            if (xpath < 0 and -xpath <= len(self)) or (xpath >= 0 and xpath < len(self)):
                return self[xpath]
            else:
                return if_not_found
        elif not isinstance(xpath, str) or not xpath:
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
    # **************************************************************************
    # n0list. get()
    # **************************************************************************
    def get(self, xpath: typing.Union[str, int], if_not_found = None):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # **************************************************************************
    # n0list. first()
    # **************************************************************************
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
    # **************************************************************************
    def __getitem__(self, xpath):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if isinstance(xpath, str):
            return self._get(xpath, raise_exception = True)
        else:
            return super(n0list, self).__getitem__(xpath)
    # **************************************************************************
    # * n0list. direct_compare(..): only n0dict. direct_compare/compare have one_of_list_compare
    # **************************************************************************
    def direct_compare(
            self,
            other: n0list,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",
            continuity_check: str = "continuity_check",  # After this argument, other MUST be defined ONLY with names
            composite_key: tuple = (),
            compare_only: tuple = (),
            exclude_xpaths: tuple = (),
            transform: tuple = (),
    ) -> n0dict:
        """
        Recursively compare self[i] with other[i]
        strictly according to the order of elements.
        If self[i] (other[i] must be the same) is n0list/n0dict, then goes deeper
        with n0list.direct_compare/n0dict.direct_compare(..)

        :param self: etalon list for compare.
        :param other: list to compare with etalon
        :param self_name: <default = "self"> dict/list name, used in result["differences"]
        :param other_name: <default = "other"> dict/list name, used in result["differences"]
        :param prefix: <default = ""> xpath prefix, used for full xpath generation
        :param continuity_check: used for checking that below arguments are defined only with names
        :param composite_key:  For compatibility with compare(..)
        :param compare_only: For compatibility with compare(..)
        :param exclude_xpaths: ()|None|empty mean nothing to exclude
        :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
        :return:
                n0dict({
                    "differences":  [], # generated for each case of not equality
                    "not_equal":    [], # generated if elements with the same xpath and type are not equal
                    "self_unique":  [], # generated if elements from self list don't exist in other list
                    "other_unique": [], # generated if elements from other list don't exist in self list
                    "difftypes":    [], # generated if elements with the same xpath have different types
                })
                if not returned["differences"]: self and other are totally equal.
        """
        if continuity_check != "continuity_check":
            raise Exception("Incorrect order of arguments")
        if not isinstance(other, n0list):
            raise Exception("n0list.direct_compare(): other (%s) must be n0list" % str(other))

        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        # FIX ME: index in [] is not supported -- only node.
        if xpath_match(prefix, exclude_xpaths):
            return result

        for i, itm in enumerate(self):
            if i >= len(other):
                # other list is SHORTER that self
                result["differences"].append(
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
                if isinstance(self_value, (str, int, float)):
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
                            difference = None
                            with contextlib.suppress(ValueError):  # self_value or other_value could not be converted to float
                                if isinstance(self_value, (date, datetime)):
                                    difference = datetime.fromtimestamp(float(other_value.timestamp()) - float(self_value.timestamp()))
                                else:
                                    difference = round(float(other_value) - float(self_value), 7)
                            result["not_equal"][-1][1].append(difference)
                        result["differences"].append(
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
                            exclude_xpaths=exclude_xpaths, transform=transform,
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
                            exclude_xpaths=exclude_xpaths, transform=transform,
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
                    result["differences"].append(
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
                    result["differences"].append(
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
                result["differences"].append(
                    "List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, self_name,
                        other_name, i, str(other[i]),
                        self_name
                    )
                )
                result["other_unique"].append(("%s[%i]" % (prefix, i), other[i]))
        return result
    # **************************************************************************
    # * n0list. compare(..)
    # **************************************************************************
    def compare(
            self,
            other: n0list,
            self_name: str = "self",
            other_name: str = "other",
            prefix: str = "",
            # /,  # When everybody migrates to py3.8, then we will make it much beautiful
            continuity_check: str = "continuity_check",  # After this argument, other MUST be defined only with names
            # Strictly recommended to define composite_key+compare_only or composite_key
            # else in case of just only one attribute of element will be different
            # both elements will be marked as not found (unique) inside the opposite list
            composite_key: tuple = (),  # ()|None|empty mean all
            compare_only: tuple = (),  # ()|None|empty mean all
            exclude_xpaths: tuple = (),  # ()|None|empty mean nothing to exclude
            transform: tuple = (),  # ()|None|empty mean nothing to transform
    ) -> n0dict:
        """
        Recursively compare self[i] with other[?] WITHOUT using order of elements.
        If self[i] is n0list/n0dict (and if other[?] is found with the same type),
        then goes deeper with n0list. compare(..)/n0dict.direct_compare(..)

        :param other:
        :param self_name:
        :param other_name:
        :param prefix:
        :param continuity_check:
        :param composite_key:
        :param compare_only:
        :param exclude_xpaths:
        :param transform: ()|None|empty mean nothing to transform, else [[<xpath to elem>,<lambda for transformatio>],..]
        :return:
                n0dict({
                    "differences":  [], # generated for each case of not equality
                    "not_equal":    [], # generated if elements with the same xpath and type are not equal
                    "self_unique":  [], # generated if elements from self list don't exist in other list
                    "other_unique": [], # generated if elements from other list don't exist in self list
                    "difftypes":    [], # generated if elements with the same xpath have different types
                })
                if not returned["differences"]: self and other are totally equal.
        """
        if continuity_check != "continuity_check":
            raise Exception("n0list. compare(..): incorrect order of arguments")
        if not isinstance(other, n0list):
            raise Exception("n0list. compare(..): other (%s) must be n0list" % str(other))
        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        # FIX ME: index in [] is not supported -- only node.
        if xpath_match(prefix, exclude_xpaths):
            return result

        self_not_exist_in_other = generate_composite_keys(self, composite_key, prefix, transform)
        other_not_exist_in_self = generate_composite_keys(other, composite_key, prefix, transform)

        notmutable__self_not_exist_in_other = self_not_exist_in_other.copy()
        for composite_key, self_i  in notmutable__self_not_exist_in_other:
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
                            result["differences"].append(
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
                                exclude_xpaths=exclude_xpaths, transform=transform,
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
                                exclude_xpaths=exclude_xpaths, transform=transform,
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
                        result["differences"].append("++Types are different: %s[%d]=(%s)%s != %s[%d]=(%s)%s" %
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
                        result["differences"].append(
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
            for composite_key, self_i in self_not_exist_in_other:
                result["differences"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        self_name, self_i, str(self[self_i]),
                        other_name
                    )
                )
                result["self_unique"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
        if other_not_exist_in_self:
            for composite_key, other_i in other_not_exist_in_self:
                result["differences"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, other_i, str(other[other_i]),
                        self_name
                    )
                )
                result["other_unique"].append(("%s[%d]" % (prefix, other_i), other[other_i]))
        return result
    # **************************************************************************
    # def append(self, sigle_item):
    # if isinstance(sigle_item, (list,n0list)):
    # raise (TypeError, '(%s)%s must be scalar' % (type(sigle_item), sigle_item))
    # super(n0list, self).append(sigle_item)  #append the item to itself (the list)
    # return self
    # **************************************************************************
    # def extend(self, other_list):
    # if not isinstance(other_list, (list,n0list)):
    # raise (TypeError, '(%s)%s must be list' % (type(sigle_item), sigle_item))
    # super(n0list, self).extend(other_list)
    # return self
    # **************************************************************************
    def _in(self, other_list, in_is_expected: bool):
        if not isinstance(other_list, (list,tuple,n0list)):
            other_list = [other_list]
        for itm in self:
            if (itm in other_list) == in_is_expected:
                return True
        else:
            return False
    # **************************************************************************
    def any_in(self, other_list):
        return self._in(other_list, True)
    # **************************************************************************
    def any_not_in(self, other_list):
        return not self._in(other_list, True)
    # **************************************************************************
    def all_in(self, other_list):
        return not self._in(other_list, False)
    # **************************************************************************
    def all_not_in(self, other_list):
        return self._in(other_list, False)
    # **************************************************************************
    def _consists_of(self, other_list, in_is_expected: bool):
        if not isinstance(other_list, (list,tuple,n0list)):
            other_list = [other_list]
        for itm in other_list:
            if super(n0list, self).__contains__(itm) == in_is_expected:
                return True
        else:
            return False
    # **************************************************************************
    def consists_of_any(self, other_list):
        return self._consists_of(other_list, True)
    # **************************************************************************
    def consists_of_all(self, other_list):
        return not self._consists_of(other_list, False)
    # **************************************************************************
    def __contains__(self, other_list):  # otherlist in n0list([a])
        return self.consists_of_all(other_list)
    # **************************************************************************
    def not_consists_of_any(self, other_list):
        return not self._consists_of(other_list, True)
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
# class n0dict(OrderedDict):
class n0dict(dict):
    """
    https://github.com/martinblech/xmltodict/issues/252
    For Python >= 3.6, dictionary are Sorted by insertion order, so avoid the use of OrderedDict for those python versions.
    """
    # **************************************************************************
    # **************************************************************************
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
    # **************************************************************************
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
    # **************************************************************************
    # * n0dict. compare(..)
    # **************************************************************************
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
            exclude_xpaths: tuple = (),  # ()|None|empty mean nothing to exclude
            # transform: tuple = (),  # ()|None|empty mean nothing to transform
            transform:  typing.Tuple[
                                typing.Tuple[
                                    str,
                                    typing.Callable,
                                    typing.Callable
                                ]
                        ] = (),
    ) -> n0dict:
        if continuity_check != "continuity_check":
            raise Exception("n0dict. compare(..): incorrect order of arguments")
        if not isinstance(other, n0dict):
            raise Exception("n0dict. compare(..): other ((%s)%s) must be n0dict" % (type(other), str(other)))
        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
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
                if not xpath_match(fullxpath, exclude_xpaths):
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
                                result["differences"].append(
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
                                    exclude_xpaths=exclude_xpaths, transform=transform,
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
                                    exclude_xpaths=exclude_xpaths, transform=transform,
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
                                result["differences"].append(
                                    "*Types are different: %s[\"%s\"]=(%s)%s != %s[\"%s\"]=(%s)%s" %
                                    (
                                        self_name, key, type(self[key]), str(self[key]),
                                        other_name, key, type(other[key]), str(other[key]),
                                    )
                                )
                            else:
                                result["not_equal"].append((prefix + "/" + key, (self[key], other[key])))
                                result["differences"].append(
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
                if not xpath_match(fullxpath, exclude_xpaths) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    result["differences"].append(
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
                if not xpath_match(fullxpath, exclude_xpaths) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    result["differences"].append(
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
    # **************************************************************************
    # * n0dict. direct_compare(..)
    # **************************************************************************
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
            exclude_xpaths: tuple = (),  # ()|None|empty mean nothing to exclude
            transform: tuple = (),  # ()|None|empty mean nothing to transform
    ) -> n0dict:
        if continuity_check != "continuity_check":
            raise Exception("n0dict. direct_compare(..): incorrect order of arguments")
        return self.compare(
            other,
            self_name, other_name, prefix,
            one_of_list_compare=one_of_list_compare,  # Only for n0dict. compare()
            composite_key=composite_key, compare_only=compare_only,
            exclude_xpaths=exclude_xpaths, transform=transform,
        )
    # **************************************************************************
    # XPATH
    # **************************************************************************
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
    # **************************************************************************
    def xpath(self, mode: int = None) -> list:  # list[(xpath, value)]
        """
        Public function: collect elements xpath starts from root
        """
        return self.__xpath(self, "/", mode)
    # **************************************************************************
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
    # **************************************************************************
    # XML
    # **************************************************************************
    def __xml(self, parent: n0dict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export OrderedDict into xml result string
        """
        result = ""
        if not parent is None:
            if isinstance(parent, (dict, OrderedDict, n0dict)):
                if not len(parent.items()):
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
                        if not key.startswith("@"):
                            result += " " * indent + ("<%s>%s</%s>" % (key, str(value), key))
                    elif isinstance(value, (dict, OrderedDict, n0dict)):
                        sub_result = self.__xml(value, indent + inc_indent, inc_indent)

                        attribs = ""
                        attribs_of_current_key = [(__key[1:], __value) for __key,__value in value.items() if __key.startswith("@")]
                        if len(attribs_of_current_key):
                            for __key, __value in attribs_of_current_key:
                                attribs += " %s=\"%s\"" % (__key, __value)
                        if sub_result:
                            result += (" " * indent + "<%s%s>\n%s\n" + " " * indent + "</%s>") % (key, attribs, sub_result, key)
                        else:
                            result += " " * indent + "<%s%s/>" % (key, attribs)
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
    # **************************************************************************
    def to_xml(self, indent: int = 4, encoding: str = "utf-8") -> str:
        """
        Public function: export self into xml result string
        """
        result = ""
        if encoding:
            result = "<?xml version=\"1.0\" encoding=\"%s\"?>\n" % encoding
        return result + self.__xml(self, 0, indent)
    # **************************************************************************
    # JSON
    # **************************************************************************
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
                    result += (" " * indent + '"%s": [\n%s\n' + " " * indent + "]") % (key, sub_result)
                else:
                    result += " " * indent + '"%s": null' % key
            elif isinstance(value, str):
                result += " " * indent + ('"%s": "%s"' % (key, value))
            elif isinstance(value, (n0dict, dict, OrderedDict)):
                sub_result = self.__json(value, indent + inc_indent, inc_indent)
                if sub_result:
                    result += (" " * indent + '"%s": {\n%s\n' + " " * indent + "}") % (key, sub_result)
                else:
                    result +=  " " * indent + '"%s": null' % key
            elif value is None:
                result += " " * indent + '"%s": null' % key
            else:
                raise Exception("Unknown type (%s) %s ==  %s" % (type(value), key, str(value)))
        return result

    def to_json(self, indent: int = 4) -> str:
        """
        Public function: export self into json result string
        """
        return n0pretty(self, show_type=False, __indent_size = indent)
    # **************************************************************************
    # **************************************************************************
    def isExist(self, xpath) -> n0dict:
        """
        Public function: return empty lists in dict, if self[xpath] exists
        """
        validation_results = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
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
        validation_results["differences"].append("[%s] doesn't exist" % xpath)
        validation_results["other_unique"].append((xpath, None))
        return validation_results
    # **************************************************************************
    # **************************************************************************
    def is_exist(self, xpath: str) -> bool:
        """
        Public function: return True, if self[xpath] exists
        """
        # TO DO: redo with 'in'
        '''
        try:
            if self[xpath]:
                return True
        except:
            pass
        return False
        '''
        with contextlib.suppress(Exception):
            if self[xpath]:
                return True
        return False
    # **************************************************************************
    # **************************************************************************
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
    # **************************************************************************
    # **************************************************************************
    def has_any_of(self,tupple_of_keys):
        for key in tupple_of_keys:
            if key in self:
                return True
        return True
    # **************************************************************************
    # **************************************************************************
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
        validation_results["differences"].append("[%s]=='%s' != '%s'" % (xpath, self[xpath], value))
        validation_results["not_equal"].append((xpath, (self[xpath], value)))
        return validation_results
    # **************************************************************************
    # **************************************************************************
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
        validation_results["differences"].append("[%s]=='%s' != [%s]=='%s'" % (
            xpath, transformation(self[xpath]),
            other_xpath, transformation(other_n0dict[other_xpath])
        )
                                              )
        validation_results["not_equal"].append((xpath, (self[xpath], other_n0dict[other_xpath])))
        return validation_results
    # **************************************************************************
    # n0dict _find
    # **************************************************************************
    # def _find(self, xpath_list: list, parent_node, return_lists, xpath_found_str: str = "/") -> list:
    def _find(self,
            xpath_list: typing.Union[str, list],
            parent_node,
            return_lists,
            xpath_found_str: str = "/") \
        ->  typing.Tuple[
                typing.Union[n0dict, n0list, None],
                typing.Union[str, int, None],
                typing.Union[typing.Any, None],
                str,
                typing.Union[list, None]
            ]:
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
        if not node_name and not node_index:
            n0debug("xpath_list")
            raise Exception("Empty node_name and node_index")
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
                        if isinstance(cur_node_index, str):
                            nxt_parent_node = cur_parent_node[n0eval(cur_node_index)]
                        else:
                            raise Exception("If index is in '%s', then (%s)'%s' must be str" %
                                                (
                                                    cur_node_name_index,
                                                    type(cur_node_index),
                                                    cur_node_index
                                                )
                                            )
                else:
                    nxt_parent_node = cur_parent_node

                if node_index or len(xpath_list) > 1:
                    if node_index:
                        return self._find(["[%s]" % str(node_index)] + xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
                    else:
                        return self._find(                             xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
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
                        cur_not_found_xpath_list = self._find(
                                                        # [next_node_name] + new_xpath_list, # mypy: error: Name 'new_xpath_list' is not defined
                                                        [next_node_name] + xpath_list,
                                                        return_lists,
                                                        parent_node,
                                                        found_xpath_str
                                                   )
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
                                        if isinstance(node_index, tuple) else \
                                        "[%s]" % str(node_index) # Because of mypy: error: Not all arguments converted during string formatting
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
                        raise Exception ("Unknown comparing command in %s" % str(node_index))

                    if node_index[1][0] == '!':
                        comparing_result = not comparing_result
                    elif node_index[1][0] != '=' and node_index[1][0] != '~':
                        raise Exception ("Unknown comparing command in %s" % str(node_index))

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
                    node_index_int = n0eval(node_index)
                except:
                    raise IndexError("Unknown index '%s[%s]'" % (xpath_found_str, node_index))

                if isinstance(parent_node, (list, tuple, n0list)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index_int >= len__parent_node or node_index_int < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, "[%d]" % node_index_int, None, xpath_found_str, xpath_list
                    # raise IndexError("If we are looking for element of list '%s[%s]', then parent node (%s)'%s' must be list" % (xpath_found_str, node_index, type(parent_node), str(parent_node)))

                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, "[%d]" % node_index_int, parent_node[node_index_int], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    return self._find(xpath_list[1:], parent_node[node_index_int], return_lists, "%s[%d]" % (xpath_found_str, node_index_int))
    # **************************************************************************
    # **************************************************************************
    def _get(self, xpath: str, raise_exception = True, if_not_found = None, return_lists = True):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        if not xpath:
            raise Exception("xpath '%s' is not valid" % str(xpath))
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
            except KeyError as ex:
                if raise_exception:
                    raise ex
                else:
                    return if_not_found
    # ******************************************************************************
    # ******************************************************************************
    def __getitem__(self, xpath):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        return self._get(xpath, raise_exception = True)
    # **************************************************************************
    # **************************************************************************
    def get(self, xpath: str, if_not_found = None):
        """
        Public function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # **************************************************************************
    # **************************************************************************
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
    # **************************************************************************
    # **************************************************************************
    def _add(self, parent_node, node_name_index: typing.Union[str, tuple], xpath_list: list) -> typing.Tuple[str, str]:
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
                        next_node_name_index = "[%s]" % str(next_node_index)
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = "[%s]" % str(next_node_index)
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
                        next_node_name_index = "[%s]" % str(next_node_index)
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = "[%s]" % str(next_node_index)
            else:
                raise Exception("Nonsence! Impossible to add %s[%s] to the list (%s)%s"
                                % (cur_node_name, cur_node_index, type(parent_node), str(parent_node)))

        if len(xpath_list) == 1:
            return next_node, next_node_name_index
        else:
            return self._add(next_node, next_node_name_index, xpath_list[1:])
    # **************************************************************************
    # **************************************************************************
    def __setitem__(self, xpath: str, new_value):
        """
        Public function:
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
    # **************************************************************************
    def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> n0dict:
        # **********************************************************************
        def multi_define(xpath, new_value):
            if isinstance(new_value, (dict, OrderedDict, n0dict)):
                self[xpath] = n0dict(new_value, recursively=True)
            elif isinstance(new_value, (list, tuple, n0list)):
                self[xpath] = n0list(new_value, recursively=True)
            else:
                self[xpath] = new_value
        # **********************************************************************
        if isinstance(xpath, dict) and new_value is None:
            for item_key in xpath:
                multi_define(item_key, xpath[item_key])
        elif isinstance(xpath, str) and not new_value is None:
            multi_define(xpath, new_value)
        else:
            raise Exception("Received (%s,%s) as argument, but expected (key,value) or (dict)." % (type(xpath), type(new_value)))
        return self
    # **************************************************************************
    def delete(self, xpath: str, recursively: bool = False) -> n0dict:
        xpath_list = xpath.split('/')
        for i,last_xpath_index in enumerate(range(len(xpath_list), 0, -1)):
            parent_node, node_name_index, cur_value, found_xpath_str, not_found_xpath_list = \
                self._find(xpath_list[0:last_xpath_index], self, return_lists=True)
            if i == 0 or (
                recursively and
                isinstance(cur_value, n0dict) and not len(cur_value)
            ):
                del parent_node[node_name_index]
        return self
    # **************************************************************************
    def pop(self, xpath: str, recursively: bool = False) -> typing.Any:
        result = self[xpath]
        self.delete(xpath, recursively)
        return result
    # **************************************************************************
    # **************************************************************************
    def _valid(self, validate, valid_is_expected: bool):
        for itm in self:
            if validate(itm) == valid_is_expected:
                return True
        return False
    # **************************************************************************
    def any_valid(self, validate):
        return self._consists_of(validate, True)
    # **************************************************************************
    def any_not_valid(self, validate):
        return self._consists_of(validate, False)
    # **************************************************************************
    def all_valid(self, validate):
        return not self._consists_of(validate, False)
    # **************************************************************************
    def all_not_valid(self, validate):
        return not self._consists_of(validate, True)
    # **************************************************************************
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
# https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
# https://code.activestate.com/recipes/576694/
from collections.abc import MutableSet
class OrderedSet(MutableSet):
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
# ******************************************************************************
# 2 levels dict:
# initial_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - key1
#       - item3
#       - item4
# Unpack references recursive: bool = True
# unpacked_dict = {key : list(unpack_references(initial_dict, key)) for key in initial_dict}
# unpacked_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - item1
#       - item2
#       - item3
#       - item4
# Remove references recursive: bool = False
# unpacked_dict = {key : list(unpack_references(initial_dict, key), False) for key in initial_dict}
# unpacked_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - item3
#       - item4
def unpack_references(initial_dict: dict, initial_key: str, recursive: bool = True) -> OrderedSet:
    collected_set = OrderedSet() # Not allow to save order with ordinary set
    node = initial_dict[initial_key]
    if isinstance(node, str):
        node = [node]
    if not isinstance(node, list):
        raise Exception(f"node under {initial_key} must be str or list")

    for item in node:
        if item in initial_dict:    # item == reference (key)
            if recursive:
                collected_set |= unpack_references(initial_dict, item)
        else:                       # item == component dir
            collected_set.add(item)
    return collected_set
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
class Git():
    _repository_name = None
    _repository_path = None
    # ##############################################################################################
    def __init__(self, repo_root_dir: str, repository_url: str, rsa_key_path: str = ""):
        if not repository_url.startswith("ssh://") or not repository_url.endswith(".git"):
            raise Exception("repository_url must be 'ssh://...git'")

        outs = errs = None
        self._repository_path = os.path.abspath(repo_root_dir)
        if not os.path.exists(os.path.join(self._repository_path, ".git")):
            outs, errs = self.run(
                                ["clone", repository_url] +
                                ["--config", "core.sshCommand=ssh -i " + rsa_key_path + " -F /dev/null"] if rsa_key_path else []
            )
            self._repository_name = repository_url.split("/")[-1].split(".git")[0]
            self._repository_path = os.path.join(self._repository_path, self._repository_name)
        else:
            self._repository_name = os.path.split(self._repository_path)[1]
            n0print("Other repository '%s' is already existed" % self._repository_name)

        if errs and "already exists and is not an empty directory." in errs:
            outs, errs = self.run("pull")
            if outs != "Already up to date.\n":
                n0debug_calc(outs.strip(), "outs")
                n0debug_calc(errs.strip(), "errs")
                # raise Exception(outs + "\n" if outs else "" + errs)
    # ##############################################################################################
    def run(self, git_arguments: typing.Union[str, list], show_result = True) -> tuple:
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")
        n0print("*** git %s" % " ".join(git_arguments))
        p = subprocess.Popen(   (command_line:=["git",] + git_arguments),
                                cwd = self._repository_path,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True,
                                encoding = "utf-8",
        )
        try:
            outs, errs = p.communicate(timeout=(timeout_sec:=600))
        except subprocess.TimeoutExpired:
            raise Exception("Timeout %d seconds were happened during execution:\n%s>%s" % (timeout_sec, self._repository_path, " ".join(command_line)))
            os.kill(p.pid, signal.CTRL_BREAK_EVENT)
            outs, errs = p.communicate()

        if show_result:
            n0debug_calc(outs.strip(), "outs")
            n0debug_calc(errs.strip(), "errs")
        return outs, errs
    # ##############################################################################################
    def checkout(self, branch_name: str):
        outs, errs = self.run(["checkout", branch_name])
        return outs, errs
    # ##############################################################################################
    def log(self, git_arguments: typing.Union[str, list]):
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")

        outs, errs = self.run(["log",  "--date=format:%y%m%d_%H%M%S", "--pretty=format:%H=%ad=%cn=%s"] + git_arguments)
        return outs, errs
    # ##############################################################################################
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
