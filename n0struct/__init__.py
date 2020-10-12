# 0.01 = 2020-07-25 = Initial version
# 0.02 = 2020-07-26 = Enhancements
# 0.03 = 2020-08-02 = Huge enhancements
# 0.04 = 2020-08-05 = Prepared for upload to pypi.org
# 0.05 = 2020-08-11 = Huge enhancements: unification of .*compare() .toJson(), .toXml(), n0dict(JSON/XML string)
# 0.06
# 0.07 = 2020-09-02 = transform added
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
from __future__ import annotations  # Python 3.7+: for using own class name inside body of class

import sys
import os
import inspect
import typing
from datetime import datetime, timedelta, date
import random
from collections import OrderedDict
import xmltodict
import json
import urllib

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
    return additional element in result["notequal"] with difference
    """
    global __flag_compare_return_difference_of_values
    __flag_compare_return_difference_of_values = value
    return __flag_compare_return_difference_of_values


def get__flag_compare_return_difference_of_values():
    global __flag_compare_return_difference_of_values
    return __flag_compare_return_difference_of_values


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
    return date_delta(now, day_delta, month_delta).strftime("%Y%m%d%m%d%H%M%S%f")
    
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
        if internal_call:
            frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
        else:
            frameinfo = inspect.stack()[2]

        global __debug_level
        global __debug_levels
        if level <= __debug_level:
            sys.stdout.write(
                "***%s %s %s:%d: " % (
                    (" [%s]" % __debug_levels[level]) if internal_call else "",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    os.path.split(frameinfo.filename)[1],
                    frameinfo.lineno
                )
                + (text if text else "") + end
            )
    else:
        sys.stdout.write((text if text else "") + end)
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
        level=level
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
            level=-level
    )


def n0pretty(item, indent_: int = 0):
    """
    :param item:
    :param indent_:
    :return:
    """

    def indent():
        return "\n" + (" " * (indent_ + 1) * 4)  # __indent_size = 4

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
                result += "'" + sub_item + "': " + n0pretty(item[sub_item], indent_ + 1)
            else:
                result += n0pretty(sub_item, indent_ + 1)
        if result and "\n" in result:
            result = brackets[0] + indent() + result + indent()
        else:
            result = brackets[0] + result
        result += brackets[1]
    elif isinstance(item, str):
        result = '"' + item + '"'
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
    n0print(to_print, level=level)


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
    if isinstance(xpath_list, str):
        xpath_list = (xpath_list,)
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


def get_composite_keys(input_list: n0list, elemets_for_composite_key: tuple) -> list:
    """
    serialization all or {elemets_for_composite_key} elements of {input_list[]}
    """
    if isinstance(elemets_for_composite_key, str):
        elemets_for_composite_key = (elemets_for_composite_key,)

    composite_keys_for_all_lines = []
    for line in input_list:
        if isinstance(line, (dict, n0dict)):
            created_composite_key = ""
            if elemets_for_composite_key:
                for key in elemets_for_composite_key:
                    if key in line:
                        if created_composite_key:
                            created_composite_key += ";"
                        created_composite_key += key + "=" + str(line[key])
            if not created_composite_key:
                for key in line:
                    if created_composite_key:
                        created_composite_key += ";"
                    created_composite_key += key + "=" + str(line[key])
        else:
            raise Exception("get_composite_keys(..): expected dict, but got unexpected type"
                            " of element in input_list: %s" % type(line))
        composite_keys_for_all_lines.append(created_composite_key)
    return composite_keys_for_all_lines


class n0list(list):
    """
    Class extended builtins.list(builtins.object) with additional methods:
    . direct_compare()  = compare [i] <=> [i]
    . compare()         = compare [i] <=> [?] WITHOUT using order
    """

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
        :param transform: ()|None|empty mean nothing to transform
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "notequal"      : [], # generated if elements with the same xpath and type are not equal
                    "selfnotfound"  : [], # generated if elements from other list don't exist in self list
                    "othernotfound" : [], # generated if elements from self list don't exist in other list
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
            "notequal": [],
            "selfnotfound": [],
            "othernotfound": [],
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
                result["othernotfound"].append(("%s[%i]" % (prefix, i), self[i]))
                continue
            # ######### if i >= len(other):
            # --- TRANSFORM: START -------------------------------------
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
                        result["notequal"].append(
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
                            result["notequal"][-1][1].append(difference)
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
                    result["notequal"].append(
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
                result["selfnotfound"].append(("%s[%i]" % (prefix, i), other[i]))
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
        :param transform:
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "notequal"      : [], # generated if elements with the same xpath and type are not equal
                    "selfnotfound"  : [], # generated if elements from other list don't exist in self list
                    "othernotfound" : [], # generated if elements from self list don't exist in other list
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
            "notequal": [],
            "selfnotfound": [],
            "othernotfound": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        # FIX ME: index in [] is not supported -- only node.
        if xpath_match(prefix, exclude):
            return result

        self_not_exist_in_other = get_composite_keys(self, composite_key)
        other_not_exist_in_self = get_composite_keys(other, composite_key)

        notmutable__self_not_exist_in_other = self_not_exist_in_other.copy()
        notmutable__other_not_exist_in_self = other_not_exist_in_self.copy()
        for self_i, composite_key in enumerate(notmutable__self_not_exist_in_other):
            if composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)
                # --- TRANSFORM: START -------------------------------------
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
                                result["notequal"].append(
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
                                result["notequal"].append(
                                    (
                                        "%s[%d]<=>[%d]" % (prefix, self_i, other_i),
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
                                result["notequal"][-1][1].append(difference)
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
                                    ("<=>[%d]" % other_i) if self_i != other_i else ""
                                ),
                                composite_key=composite_key, compare_only=compare_only,
                                exclude=exclude, transform=transform,
                            )
                        )
                    elif isinstance(self[self_i], (n0dict, dict, OrderedDict)):
                        result.update_extend(
                            n0dict(self[self_i]).compare(
                                n0dict(other[other_i]),
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + (
                                    "<=>[" + str(other_i) + "]" if self_i != other_i else ""),
                                one_of_list_compare=self.compare,
                                composite_key=composite_key, compare_only=compare_only,
                                exclude=exclude, transform=transform,
                            )
                        )
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
                            result["notequal"].append(
                                (
                                    "%s[%d]" % (prefix, self_i),
                                    (
                                        self[self_i],
                                        other[other_i]
                                    )
                                )
                            )
                        else:
                            result["notequal"].append(
                                (
                                    "%s[%d]<=>[%d]" % (prefix, self_i, other_i),
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
                self_not_exist_in_other.remove(composite_key)
                other_not_exist_in_self.remove(composite_key)
            # ######### if key in other_not_exist_in_self:
        # ######### for key in notmutable__self_not_exist_in_other:

        if self_not_exist_in_other:
            for composite_key in self_not_exist_in_other:
                self_i = notmutable__self_not_exist_in_other.index(composite_key)
                result["messages"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        self_name, self_i, str(self[self_i]),
                        other_name
                    )
                )
                result["othernotfound"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
        if other_not_exist_in_self:
            for composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)
                result["messages"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, other_i, str(other[other_i]),
                        self_name
                    )
                )
                result["selfnotfound"].append(("%s[~%d]" % (prefix, other_i), other[other_i]))
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
class n0dict(OrderedDict):
    # ******************************************************************************
    # def lxml2dict(self, element):
    # return element.tag, \
    # OrderedDict(map(self.lxml2dict, element)) or element.text
    # ******************************************************************************
    def __init__(self, *args, **kw):
        """
        args == tuple, kw == mapping(dictionary)

        * == convert from tuple into list of arguments
        ** == convert from mapping into list of named arguments

        :param args:
        :param kw:
        """
        if len(args):
            if isinstance(args[0], str):
                if args[0].strip()[0] == "<":
                    return super(n0dict, self).__init__(xmltodict.parse(args[0]))
                elif args[0].strip()[0] == "{":
                    return super(n0dict, self).__init__(json.loads(args[0]))
                raise Exception("n0dict(..): if you provide string, it should be XML or JSON")
        # raise Exception("n0dict(..): Init as OrderedDict")
        # n0debug_calc(len(args),"len(args)")
        # n0debug_calc(args,"args")
        return super(n0dict, self).__init__(*args, **kw)
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
            "notequal": [],
            "selfnotfound": [],
            "othernotfound": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})

        self_not_exist_in_other = list(self.keys())
        other_not_exist_in_self = list(other.keys())

        # #############################################################
        # NEVER fetch data from the mutable list in the loop !!!
        # #############################################################
        for key in self:
            if key in other:
                fullxpath = prefix + "/" + key
                if not xpath_match(fullxpath, exclude):
                    # --- TRANSFORM: START -------------------------------------
                    self_value = self[key]
                    other_value = other[key]
                    transform_i = xpath_match(fullxpath, [itm[0] for itm in transform])
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
                                result["notequal"].append(
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
                                    result["notequal"][-1][1].append(difference)
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
                            result["notequal"].append((prefix + "/" + key, (self[key], other[key])))
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
                if not xpath_match(fullxpath, exclude):
                    result["messages"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            self_name,
                            key,
                            str(self[key]),
                            other_name
                        )
                    )
                    result["othernotfound"].append((fullxpath, self[key]))
        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                fullxpath = "%s/%s" % (prefix, key)
                if not xpath_match(fullxpath, exclude):
                    result["messages"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            other_name,
                            key,
                            str(other[key]),
                            self_name
                        )
                    )
                    result["selfnotfound"].append((fullxpath, other[key]))
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
    # * n0dict. __FindElem(..)
    # ******************************************************************************
    def __FindElem(self, parent: n0dict, where_parts: list, value: str = None, xpath: str = "", root = None) -> tuple:
        """
        Private function: 
            if path is found, returns 
                [0] = element/node by path where_parts:list
                [1] = None
                [2] = xpath of found element/node
            if path is NOT found, returns 
                [0] = last found element/node
                [1] = not found sub-elements
                [2] = xpath of last found element/node
        """
        if parent is None:
            raise Exception("Why parent is None?")
        if root is None:
            root = parent
            
        child_name = where_parts[0]
        child_index = None
        if "[" in child_name and child_name.endswith("]"):
            child_name, child_index = child_name.split("[", 2)
            child_index = child_index[:-1].strip().lower()

        # n0print("#"*80)
        # n0debug("where_parts")
        # n0debug("child_name")
        # n0debug("child_index")
        # n0debug("parent")
        # print("parent=")
        # print(parent)
        if isinstance(parent, (n0dict, OrderedDict, dict)):
            # n0print("+1"*20)
            if child_name not in parent:
                # n0print("-"*50)
                # return parent, where_parts  # Return what was found, and what was not found
                return parent, where_parts, xpath  # Return what was found, and what was not found
            else:
                # n0print("*"*50)
                child = parent.get(child_name)  # [] or None are possible results
                # n0debug("child")
        elif isinstance(parent, (n0list, tuple, list)):
            # n0print("+2"*20)
            for i,one_of_parent in enumerate(parent):
                # n0print("##### Lets try: %s[%d]"%(xpath,i))
                found, not_found, found_xpath = self.__FindElem(
                                                            one_of_parent, 
                                                            where_parts, 
                                                            value, 
                                                            "%s[%d]"%(xpath,i),
                                                            root
                                                            )  
                if not not_found:
                    return found, not_found, found_xpath
            else:
                return parent, where_parts, xpath  # Return what was found, and what was not found
        else:
            if child_name == "..":
                # n0print("Upper and upper")
                parent_xpath = "/".join(xpath.split('/')[:-1])
                # n0debug("parent_xpath")
                # n0print("-------------8<----------------- #1")
                parent = root[parent_xpath]
                # n0print("------------->8----------------- #1")
                # n0debug("parent")
                # n0debug_calc("/".join(where_parts[1:]),"more_xpath")
                return self.__FindElem(parent, where_parts[1:], value, parent_xpath, root)  # Upper and upper
            # n0print("+3"*20)
            # n0print("~"*50)
            # n0print("Unknown type of parent %s" % type(parent))
            # n0print("~"*50)
            # n0debug("parent")
            # n0debug("where_parts")
            # sys.exit(-1)
            

        if child_index:
            # n0print("+4"*20)
            if isinstance(child, (list, tuple, n0list)):
                # n0print("+5"*20)
                if not child_index.translate(str.maketrans("+-.", "000")).isnumeric():
                    if child_index.startswith("last()"):
                        child_index = child_index[6:]
                        if not child_index or child_index.translate(str.maketrans("+-.", "000")).isnumeric():  # Py3 dirty fix
                            child_index = int(eval("-1" + child_index))  # FIX ME: Very dark and dirty :-(
                        else:
                            raise IndexError(
                                "'Something strange with index 'last()%s' in '%s'" % (child_index, where_parts[0]))
                    else:
                        print("'%s' in '%s' is not an index" % (child_index, where_parts[0]))
                        raise IndexError("'%s' in '%s' is not an index" % (child_index, where_parts[0]))
                else:
                    child_index = int(eval(child_index))  # FIX ME: Very dark and dirty :-(
                if child_index >= len(child):
                    raise IndexError(
                        "index of '%s' (%d) is beyond the length (%d) of %s" % (
                            where_parts[0], child_index, len(child), child
                        )
                    )
                if child_index < -len(child):
                    raise IndexError(
                        "index of '%s' (%d) is below the length (%d) of %s" % (
                            where_parts[0], child_index, len(child), child
                        )
                    )
                # n0print("+7"*20)
                child = child[child_index]
                # n0debug("child")
                # n0debug("where_parts")
            else:
                # n0print("+6"*20)
                if child_index.startswith("text()"):
                    child_text_compare = child_index[6:]
                    if child_text_compare.startswith("=="):
                        child_index_value = child_text_compare[2:].strip()
                        child_text_compare = True
                    elif child_text_compare.startswith("!="):
                        child_index_value = child_text_compare[2:].strip()
                        child_text_compare = False
                    elif child_text_compare.startswith("="):
                        child_index_value = child_text_compare[1:].strip()
                        child_text_compare = True
                    else:
                        raise IndexError("Strange compare command in '%s' of (%s)'%s'==%s" % (child_index, type(child), xpath, child))
                        
                    if child_index_value[0] == child_index_value[-1] and child_index_value[0] in ("'",'"'):
                        child_index_value = child_index_value[1:-1]
                        
                    child_value = urllib.parse.unquote(child).lower()
                    child_index_value = urllib.parse.unquote(child_index_value)
                    
                    if (child_value == child_index_value) != child_text_compare:
                        # n0print("Expected: %s %s %s" % (child_value, "==" if child_text_compare else "!=", child_index_value)) 
                        return parent, where_parts, xpath
                    # else:
                        # n0print("+"*80) 
                        # n0print("+"*80) 
                        # n0print("As expected: %s %s %s" % (child_value, "==" if child_text_compare else "!=", child_index_value)) 
                        # n0print("+"*80) 
                        # n0print("+"*80) 
                        
                else:
                    raise IndexError("Strange index '%s' of (%s)'%s'==%s" % (child_index, type(child), xpath, child))
                # if child_index == "last()":
                    # child = child
                # else:
                    # raise IndexError("'%s' is not list but %s" % (child, type(child)))

        # n0print("+8"*20)
        if len(where_parts) > 1:
            # n0print("Deeper and deeper")
            # n0debug_calc(where_parts[1:])
            # n0debug_calc(xpath+"/"+where_parts[0])
            return self.__FindElem(child, where_parts[1:], value, xpath+"/"+where_parts[0], root)  # Deeper and deeper
        elif len(where_parts) == 1:
            # if value and value != "change to n0dict()":
            if value:
                parent.update({child_name: value})
            # n0print("Returning...")
            # n0debug("child_name")
            # n0print(parent.get(child_name))
            # n0print(xpath)
            # return parent.get(child_name), None, xpath  # Parent element, nothing is left
            return child, None, xpath  # Parent element, nothing is left
        else:
            raise Exception("FATAL: Unexpected behavior with empty path")

    # ******************************************************************************
    # ******************************************************************************
    def __AddElem(self, parent: OrderedDict, where_parts: list, default_value: str = "change to n0dict()") -> tuple:
        """
        Private function: create element by path where_parts:list and define it as default_value.
        If any of elements exists, then such element will be converted into array,
        and subpath will be continued from last element of such array
        """
        if default_value == "change to n0dict()":
            default_value = n0dict()

        if not where_parts or not len(where_parts):
            return parent  # Created element

        if len(where_parts) == 1:
            current_value = default_value
            if not default_value:
                # current_value = n0dict()
                pass
        else:
            current_value = n0dict()

        if isinstance(parent, list):
            parent = parent[-1]  # If list, then put to the last node
        # NOT PREDICTED: What to do if will be requested to extend already existed element into node?
        # print("--> " +  str(where_parts))
        child = parent.get(where_parts[0])
        if child:
            # The element with the same name exists
            if not isinstance(child, list):
                child = [child]
            child.append(current_value)
            # parent[where_parts[0]] = child # Return back updated value
            super(n0dict, parent).__setitem__(where_parts[0], child)

            if len(where_parts) == 1:
                return child, []

            child = parent[where_parts[0]][-1]
        else:
            parent.update({where_parts[0]: current_value})
            child = parent.get(where_parts[0])
            if len(where_parts) == 1:
                return child
            if current_value is None:
                return child

        # print("==> " +  str(where_parts))
        return self.__AddElem(child, where_parts[1:], default_value)  # Create next element

    # ******************************************************************************
    # ******************************************************************************
    def AddElem(self, where: str, what: str = None, value: str = None):
        """
        Public function:
        Convert path where:str into list, remove all empty separators ("//" or leading/trailing "/"),
        find element with path where:str, from the root (super(n0dict, self)),
        unpack tuple with "*" into list of arguments,
        create sub-nodes' name[s] if they[/it] do[es]n't exist ONLY.

        If optional argument 'what' is provided, add sub-nodes. If sub-nodes exist, CONVERT THEM INTO LIST AND ADD NEW ITEM.
        If optional argument 'value' is provided, put into destination path where+what.
        """
        return \
            self.__AddElem(  # This pass will convert single elements into lists IN CASE OF DUPLICATION NAMES
                self.__AddElem(  # This pass will create sub-nodes' name[s] if they[/it] do[es]n't exist ONLY.
                    *  # unpack tuple with "*" into list of arguments,
                    self.__FindElem(  # find element with path where:str, from the root (super(n0dict, self)),
                        self,
                        [itm for itm in where.split("/") if itm]  # Convert path where:str into list,
                        # remove all empty separators ("//" or leading/trailing "/"),
                    )[0:1] # leave only 2 returned elements: where to inject and what to inject
                ),
                [itm for itm in what.split("/") if itm],  # Convert path what:str into list,
                # remove all empty separators ("//" or leading/trailing "/"),
                value  # If optional argument 'value' is provided, put into destination path where+what.
            )

    # ******************************************************************************
    # ******************************************************************************
    def nvl(self, where: str, if_not_found = None):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        if not where:
            return default
        found, not_found, found_xpath = self.__FindElem(self,
                                           [itm for itm in where.split("/") if itm]  # Convert path where:str into list,
                                           # remove all empty separators
                                           # ("//" or leading/trailing "/")
                                           )
        if not_found:
            return if_not_found
        # #####################################################################
        # #####################################################################
        # NEVER RECONVERT OBJECTS!!!
        # For example: return n0list(found) => dict["list"].append(newitem) => append will be applyed to NEW object!!!
        # #####################################################################
        # #####################################################################
        return found
    # ******************************************************************************
    # ******************************************************************************
    def __getitem__(self, where: str):
        """
        Private function:
        return self[where1/where2/.../whereN]
            AKA
        return self[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        # found, not_found = self.__FindElem(super(n0dict, self)
        found, not_found, found_xpath = self.__FindElem(self,
                                           [itm for itm in where.split("/") if itm]  # Convert path where:str into list,
                                           # remove all empty separators
                                           # ("//" or leading/trailing "/")
                                           )
        if not_found:
            # raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), where))
            raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), found_xpath))
        # #####################################################################
        # #####################################################################
        # NEVER RECONVERT OBJECTS!!!
        # For example: return n0list(found) => dict["list"].append(newitem) => append will be applyed to NEW object!!!
        # #####################################################################
        # #####################################################################
        return found

    # ******************************************************************************
    # ******************************************************************************
    def __setitem__(self, where: str, value: str):
        """
        Private function:
        self[=?where1/where2/.../whereN] = value
            AKA
        self[where1][where2]...[whereN] = value

        if 'where' starts with '=', then
            the value will be rewritten
            If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        else
            the path will be created. if last element exists, then the element will be reconfigured into array
            if any whereN starts with '+', then the element will be reconfigured into array

        """
        flag_overwrite_attribute_value = False
        if where.startswith("="):
            flag_overwrite_attribute_value = True
            where = where[1:]
        where_parts = [itm for itm in where.split("/") if itm]

        if len(where_parts) == 1:
            return super(n0dict, self).__setitem__(where, value)
        else:
            if flag_overwrite_attribute_value:
                found, not_found, found_xpath = self.__FindElem(super(n0dict, self), where_parts, value)
                if not_found:
                    # raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), where))
                    raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), found_xpath))
                return found
            else:
                # By default just the last element could be item in the array,
                # but   if where_parts[i] will be ended with '[next()]',
                #       then from this part it will be part of array
                for i, where_part in enumerate(where_parts):
                    tag = "[next()]"
                    if where_part.lower().replace(" ", "").endswith(tag):
                        where_part = where_part[:-len(tag)]
                        where_parts[i] = where_part
                        break
                else:
                    i -= len(where_parts)
                where1 = "/".join(where_parts[:i])
                where2 = "/".join(where_parts[i:])
                return self.AddElem(where1, where2, value)

    # ******************************************************************************
    # XPATH
    # ******************************************************************************
    def __xpath(self, parent: OrderedDict, path: str = None, mode: int = None) -> list:
        """
        Private function: recursively collect elements xpath starts from parent
        """
        result = []
        for key, value in parent.items():
            if isinstance(value, list):
                for i, subitm in enumerate(value):
                    result += self.__xpath(subitm, "%s/%s[%d]" % (path, key, i), mode)
            elif isinstance(value, str):
                result.append(("%s/%s" % (path, key), value))
            elif isinstance(value, (n0dict, dict, OrderedDict)):
                result += self.__xpath(value, "%s/%s" % (path, key), mode)
            elif value is None:
                result.append(("%s/%s" % (path, key), None))
            else:
                raise Exception("%s/%s ==  %s" % (path, key, value))
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
                            ('"' + itm[1] + '"') if itm[1] else "None"
                        )
        return result

    # ******************************************************************************
    # XML
    # ******************************************************************************
    def __xml(self, parent: OrderedDict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export OrderedDict into xml result string
        """
        result = ""
        for key, value in parent.items():
            if result:
                result += "\n"
            if isinstance(value, list):
                for i, subitm in enumerate(value):
                    if i:
                        result += "\n"
                    sub_result = self.__xml(subitm, indent + inc_indent, inc_indent)
                    if sub_result:
                        result += (" " * indent + "<%s>\n%s\n" + " " * indent + "</%s>") % (key, sub_result, key)
                    else:
                        result += " " * indent + "<%s/>" % key
            elif isinstance(value, str):
                result += " " * indent + ("<%s>%s</%s>" % (key, value, key))
            elif isinstance(value, (n0dict, dict, OrderedDict)):
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
        return result

    def to_xml(self, indent: int = 4, encoding: str = "utf-8") -> str:
        """
        Public function: export self into xml result string
        """
        buffer = ""
        if encoding:
            buffer = "<?xml version=\"1.0\" encoding=\"%s\"?>\n" % encoding

        if len(self.keys()):
            own_tagname = list(self.keys())[0]
            buffer += "<%s>" % own_tagname

            own_value = list(self.values())[0]
            if len(self.values()) == 1 and isinstance(own_value, (str, int, float)):
                buffer += str(own_value)
            else:
                for item in self.values():
                    buffer += "\n" + self.__xml(item, indent, indent) + "\n"
            buffer += "</%s>\n" % own_tagname

        return buffer

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
                        elif isinstance(subitm, (list, n0list)):
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
                # if "\n" in sub_result: sub_result = "\n" + sub_result
                # if sub_result: sub_result = "\n" + sub_result
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
        buffer = "{\n"

        own_tagname = list(self.keys())[0]
        buffer += " " * indent + "\"%s\":" % own_tagname

        own_value = list(self.values())[0]
        if len(self.values()) == 1 and isinstance(own_value, (str, int, float)):
            buffer += " \"%s\"" % str(own_value)
        elif isinstance(own_value, (list, tuple, n0list, dict, OrderedDict, n0dict)):
            result = ""
            for item in self.values():
                result += self.__json(item, indent * 2, indent)
            if isinstance(own_value, (dict, OrderedDict, n0dict)):
                buffer += (" {\n%s\n" + " " * indent + "}") % result
            else:
                buffer += (" [\n%s\n" + " " * indent + "]") % result
        else:
            raise Exception("Unknown type (%s) %s ==  %s" % (type(own_value), own_tagname, str(own_value)))

        buffer += "\n}"

        return buffer

    # ******************************************************************************
    # ******************************************************************************
    def isExist(self, xpath):
        """
        Public function: return empty lists in dict, if self[xpath] exists
        """
        validation_results = n0dict({
            "messages": [],
            "notequal": [],
            "selfnotfound": [],
            "othernotfound": [],
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
        validation_results["selfnotfound"].append((xpath, None))
        return validation_results
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
        validation_results["notequal"].append((xpath, (self[xpath], value)))
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
        validation_results["notequal"].append((xpath, (self[xpath], other_n0dict[other_xpath])))
        return validation_results
    # ******************************************************************************
    # ******************************************************************************
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
