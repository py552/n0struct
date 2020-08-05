# 0.01 = 2020-07-25 = Initial version
# 0.02 = 2020-07-26 = Enhancements
# 0.03 = 2020-08-02 = Huge enhancements
# 0.04 = 2020-08-05 = Prepared for upload to pypi.org
from __future__ import annotations  # Python 3.7+: for using own class name inside body of class
from collections import OrderedDict
import random
import inspect
import os
import sys
from datetime import datetime, timedelta
from pprint import pprint
# ******************************************************************************
# rnd(_till_not_included_random): generate random integer value [0.._till_not_included_random-1]
# ******************************************************************************
rnd = lambda _till_not_included_random: int(random.random()*int(_till_not_included_random))
# ******************************************************************************
# random_from(_from_list): provide random item from the _from_list[..]
# ******************************************************************************
random_from = lambda _from_list: _from_list[rnd(len(_from_list))]
# ******************************************************************************
# get_key_by_value(_dict, _value): provide (last) key which is assosiated with _value in _dict
# ******************************************************************************
get_key_by_value = lambda _dict, _value: {value:key for key, value in _dict.items()}[_value]
# ******************************************************************************
debug_levels={
    "ALL":      10, # 10 = ALL->...->FATAL
    "TRACE":    9,  #  9 = TRACE->DEBUG->INFO->WARN->ERROR->FATAL
    "DEBUG":    7,  #  7 = DEBUG->INFO->WARN->ERROR->FATAL
    "INFO":     5,  #  5 = INFO->WARN->ERROR->FATAL
    "WARN":     3,  #  3 = WARN->ERROR->FATAL
    "ERROR":    2,  #  2 = ERROR->FATAL
    "FATAL":    1,  #  1 = FATAL only
    "OFF":      0,  #  0 = OFF
}
debug_level = debug_levels["INFO"]
# ******************************************************************************
# n0print(text, level = -debug_levels["INFO"]):
#   Print messages,
#   depends of value in global variable debug_level.
#   If n0print is called directly, value in level must be negative.
#   n0print is called thru n0debug/n0debug_calc, value in level must be possitive.
# ******************************************************************************
def n0print(text, level = -debug_levels["INFO"]):
    if level < 0:
        level = -level
        frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
    else:
        frameinfo = inspect.stack()[2]
    if debug_level >= level:
        sys.stdout.write(
            "*** [%s] %s %s:%d: " % (
                get_key_by_value(debug_levels, level),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                os.path.split(frameinfo.filename)[1], 
                frameinfo.lineno
                )
            + (text if text else "") + "\n"
        ) 
# ******************************************************************************
# n0debug(var_name, level = debug_levels["INFO"]):
#   Print value of var with name var_name,
#   depends of value in global variable debug_level.
# ******************************************************************************
n0debug = lambda var_name, level = debug_levels["INFO"]: n0print(
    "(%s id=%s)%s = '%s'" % (
        type(inspect.currentframe().f_back.f_locals[var_name]),
        id(inspect.currentframe().f_back.f_locals[var_name]),
        var_name,
        str(inspect.currentframe().f_back.f_locals[var_name])
    ) if var_name in inspect.currentframe().f_back.f_locals
    else "%s is NOT FOUND" % var_name
    , level = level
)
# ******************************************************************************
# n0debug_calc(var_value, var_name = "", level = debug_levels["INFO"]):
#   Print  calculated value (for example returned by function), 
#   depends of value in global variable debug_level.
# ******************************************************************************
n0debug_calc = lambda var_value, var_name = "", level = debug_levels["INFO"]: n0print(
    "(%s id=%s)%s = '%s'" % (type(var_value), id(var_value), var_name, str(var_value))
    , level = level
)
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
# ******************************************************************************
# ******************************************************************************
class n0list(list):
    """
    Class extended builtins.list(builtins.object) with additional methods:
    .direct_compare_list()  = compare [i] <=> [i]
    .compare_list()         = compare [i] <=> [?] WITHOUT using order
    """
    def direct_compare_list(
        self,
        other: n0list,
        self_name: str = "self",
        other_name: str = "other",
        prefix: str = "",
        dummy1 = None, # For compatibility with the list of input attributes of compare_list(..)
        dummy2 = None, # For compatibility with the list of input attributes of compare_list(..)
    ) -> n0dict:
        """
        Recursively compare self[i] with other[i] strictly according to the order of elements.
        If self[i] (other[i] must be the same) is n0list/n0dict, then goes deeper 
        with n0list.direct_compare_list/n0dict.direct_compare_dict(..)

        :param n0list self: etalon list for compare.
        :param n0list other: list to compare with etalon
        :param str self_name: <optional, default = "self"> dict/list format name before self
        :param str other_name: <optional, default = "other"> dict/list format name before other
        :param str prefix: <optional, default = ""> xpath format name before self/other
        :param NoneType dummy1: For compatibility with the list of input attributes of compare_list(..)
        :param NoneType dummy2: For compatibility with the list of input attributes of compare_list(..)
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "notequal"      : [], # generated if elements with the same xpath and type are not equal
                    "difftypes"     : [], # generated if elements with the same xpath have different types
                    "selfnotfound"  : [], # generated if elements from other list don't exist in self list
                    "othernotfound" : [], # generated if elements from self list don't exist in other list
                })
                if not returned["messages"]: self and other are totally equal.
        :rtype n0dict:
        """
        if not isinstance(other, n0list):
            raise Exception("n0list.direct_compare_list(): other (%s) must be n0list" % str(other))
        result = n0dict({
            "messages"      : [],
            "notequal"      : [],
            "difftypes"     : [],
            "selfnotfound"  : [],
            "othernotfound" : [],
        })

        for i,itm in enumerate(self):
            if i >= len(other):
                # other list is SHORTER that self
                result["messages"].append("List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                                            (
                                                self_name, other_name,
                                                self_name, i, str(self[i]),
                                                other_name
                                            )
                )
                result["othernotfound"].append((prefix + "[" + str(i) + "]", self[i]))
                continue
            # ######### if i >= len(other):
            if type(self[i]) == type(other[i]):
                if isinstance(self[i], (str, int)):
                    if self[i] != other[i]:
                        result["notequal"].append((prefix + "[" + str(i) + "]", (self[i], other[i])))
                        result["messages"].append("Values are different: %s[%d]='%s' != %s[\"%s\"]='%s' " %
                                                  (
                                                      self_name, i, str(self[i]),
                                                      other_name, i, str(other[i])
                                                  )
                        )
                elif isinstance(self[i], (list, tuple)):
                    result.update_extend(
                        self[i].direct_compare_list(
                            other[i],
                            self_name + "[" + str(i) + "]",
                            other_name + "[" + str(i) + "]",
                            prefix + "[" + str(i) + "]"
                        )
                    )
                elif isinstance(self[i], (n0dict, dict, OrderedDict)):
                    result.update_extend(
                        n0dict(self[i]).direct_compare_dict(
                            n0dict(other[i]),
                            self_name + "[" + str(i) + "]",
                            other_name + "[" + str(i) + "]",
                            prefix + "[" + str(i) + "]",
                            self.direct_compare_list
                        )
                    )
                else:
                    result["difftypes"].append(
                        (
                            prefix + "[" + str(i) + "]",
                            (
                                type(self[i]), self[i],
                                type(other[i]), other[i]
                            )
                        )
                    )
                    result["messages"].append("Not expected type %s in %s[%d]/%s[%d]" %
                                              (
                                                  type(self[i]),
                                                  self_name, i,
                                                  other_name, i
                                              )
                    )
            # ######### if type(self[i]) == type(other[i]):
            else:
                result["difftypes"].append(
                    (
                        prefix + "[" + str(i) + "]",
                        (
                            type(self[i]), self[i],
                            type(other[i]), other[i]
                        )
                    )
                )
                result["messages"].append("Types are different: %s[%d]=(%s)%s != %s[%d]=(%s)%s" %
                                          (
                                              self_name, i, type(self[i]), str(self[i]),
                                              other_name, i, type(other[i]), str(other[i]),
                                          )
                )
        # ######### for i in enumerate(self)[0]:
        if len(other) > len(self):
            # self list is SHORTER that other
            for i,itm in enumerate(other[len(self):]):
                i += len(self)
                result["messages"].append("List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                                          (
                                              other_name, self_name,
                                              other_name, i, str(other[i]),
                                              self_name
                                          )
                )
                result["selfnotfound"].append((prefix + "[" + str(i) + "]", other[i]))
        return result
    # ******************************************************************************
    # ******************************************************************************
    def compare_list(
        self,
        other: n0list,
        self_name: str = "self",
        other_name: str = "other",
        prefix: str = "",
        # Strictly recommended to define list_elements_for_*
        # else in case of just only one attribute of element will be different
        # both elements will be marked as not found (unique) inside the opposite list
        elements_for_composite_key: tuple = (),  # ()|None|empty mean all
        elements_for_compare: tuple = (),  # ()|None|empty mean all
    ) -> n0dict:
        """
        Recursively compare self[i] with other[?] WITHOUT using order of elements.
        If self[i] (other[?] must be the same) is n0list/n0dict,
        then goes deeper with n0list.compare_list(..)/n0dict.direct_compare_dict(..)

        :param n0list self: etalon list for compare.
        :param n0list other: list to compare with etalon
        :param str self_name: optional: dict/list format name before self
        :param str other_name: dict/list format name before other
        :param str prefix: xpath before self/other
        :param tuple elements_for_composite_key: ()|None|empty mean all
        :param tuple elements_for_compare: ()|None|empty mean all
        :return:
                n0dict({
                    "messages"      : [], # generated for each case of not equality
                    "notequal"      : [], # generated if elements with the same xpath and type are not equal
                    "difftypes"     : [], # generated if elements with the same xpath have different types
                    "selfnotfound"  : [], # generated if elements from other list don't exist in self list
                    "othernotfound" : [], # generated if elements from self list don't exist in other list
                })
                if not returned["messages"]: self and other are totally equal.
        :rtype n0dict:
        """
        if not isinstance(other, n0list):
            raise Exception("n0list.compare_list(): other (%s) must be n0list" % str(other))
        result = n0dict({
            "messages"      : [],
            "notequal"      : [],
            "difftypes"     : [],
            "selfnotfound"  : [],
            "othernotfound" : [],
        })

        def get_composite_keys(input_list: n0list, elements_for_composite_key: tuple) -> list:
            composite_keys = []
            for i, itm in enumerate(input_list):
                composite_key = ""
                for path_to_element in elements_for_composite_key if elements_for_composite_key else input_list[i]:
                    composite_key += path_to_element + "=" + str(input_list[i][path_to_element]) + ";"
                composite_keys.append(composite_key)
            return composite_keys
            

        self_not_exist_in_other = get_composite_keys(self, elements_for_composite_key)
        other_not_exist_in_self = get_composite_keys(other, elements_for_composite_key)

        notmutable__self_not_exist_in_other = self_not_exist_in_other.copy()
        notmutable__other_not_exist_in_self = other_not_exist_in_self.copy()
        for self_i,composite_key in enumerate(notmutable__self_not_exist_in_other):
            if composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)

                if type(self[self_i]) == type(other[other_i]):
                    if isinstance(self[self_i], (str, int)):
                        if self[self_i] != other[other_i]:
                            if self_i == other_i:
                                result["notequal"].append((prefix + "[" + str(self_i) + "]", (self[self_i], other[other_i])))
                            else:
                                result["notequal"].append((prefix + "[" + str(self_i) + "]<=>[" + str(other_i) + "]", (self[self_i], other[other_i])))
                            result["messages"].append("Values are different: %s[%d]='%s' != %s[\"%s\"]='%s' " %
                                                      (
                                                          self_name, self_i, str(self[self_i]),
                                                          other_name, other_i, str(other[other_i])
                                                      )
                            )
                    elif isinstance(self[self_i], (list, tuple)):
                        result.update_extend(
                            self.direct_compare_list(
                                self[self_i], other[other_i],
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + ("<=>[" + str(other_i) + "]" if self_i != other_i else "")
                            )
                        )
                    elif isinstance(self[self_i], (n0dict, dict, OrderedDict)):
                        result.update_extend(
                            n0dict(self[self_i]).direct_compare_dict(
                                n0dict(other[other_i]),
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + ("<=>[" + str(other_i) + "]" if self_i != other_i else ""),
                                self.compare_list
                            )
                        )
                    else:
                        result["difftypes"].append(
                            (
                                prefix + "[" + str(self_i) + "]<=>[" + str(other_i) + "]",
                                (
                                    type(self[self_i]), self[self_i],
                                    type(other[other_i]), other[other_i]
                                )
                            )
                        )
                        result["messages"].append("Not expected type %s in %s[%d]/%s[%d]" %
                                                  (
                                                      type(self[self_i]),
                                                      self_name, self_i,
                                                      other_name, other_i
                                                  )
                        )
                # ######### if type(self[i]) == type(other[i]):
                else:
                    result["difftypes"].append(
                        (
                            prefix + "[" + str(self_i) + "]",
                            (
                                type(self[self_i]), self[self_i],
                                type(other[other_i]), other[other_i]
                            )
                        )
                    )
                    result["messages"].append("Types are different: %s[%d]=(%s)%s != %s[%d]=(%s)%s" %
                                              (
                                                  self_name, self_i, type(self[self_i]), str(self[self_i]),
                                                  other_name, other_i, type(other[other_i]), str(other[other_i]),
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
                result["messages"].append("Element %s[%d]='%s' doesn't exist in %s" %
                                            (
                                                self_name, self_i, str(self[self_i]),
                                                other_name
                                            )
                )
                result["othernotfound"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
        if other_not_exist_in_self:
            for composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)
                result["messages"].append("Element %s[%d]='%s' doesn't exist in %s" %
                                          (
                                              other_name, other_i, str(other[other_i]),
                                              self_name
                                          )
                )
                result["selfnotfound"].append((prefix + "[" + str(self_i) + "]", other[other_i]))
                
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
    def update_extend(self, other):
        if other is None:
            return self
        elif isinstance(other, (n0dict, OrderedDict, dict)):
            for key in other:
                if not key in self:
                    self.update({key:other[key]})
                else:
                    if not isinstance(self[key],list):
                        self[key] = list(self[key])
                    if isinstance(other[key], (list, tuple)):
                        self[key].extend(other[key])
                    else:
                        self[key].append(other[key])
        elif isinstance(other, (str,int,float)):
            key = list(self.items())[0][0] # [0]= first item, [0] = key
            self[key].append(other)
        elif isinstance(other, (list,n0list,tuple)):
            key = list(self.items())[0][0] # [0]= first item, [0] = key
            for itm in other:
                if isinstance(itm, (list,tuple)):
                    self[key].extend(itm)
                else:
                    self[key].append(itm)
        else:
            raise Exception("Unexpected type of other: " + str(type(other)))
        return self
    ################################################################################
    ################################################################################
    ################################################################################
    def direct_compare_dict(self,
                            other: n0dict,
                            self_name: str = "self",
                            other_name: str = "other",
                            prefix: str = "",
                            one_of_list_compare = n0list.direct_compare_list,
                            # ONLY FOR COMPLEX COMPARE
                            # Strictly recommended to init lists
                            # else in case of just only one attribute of element will be different
                            # both elements will be marked as not found (unique) inside the opposite list
                            elements_for_composite_key: tuple = (),  # ()|None|empty mean all
                            elements_for_compare: tuple = (), # ()|None|empty mean all
    ) -> n0dict:
        if not isinstance(other, n0dict):
            raise Exception("n0dict.direct_compare_dict(): other (%s) must be n0dict" % str(other))
        result = n0dict({
            "messages"      : [],
            "notequal"      : [],
            "difftypes"     : [],
            "selfnotfound"  : [],
            "othernotfound" : [],
        })

        self_not_exist_in_other = list(self.keys())
        other_not_exist_in_self = list(other.keys())

        # #############################################################
        # NEVER fetch data from the mutable list in the loop !!!
        # #############################################################
        for key in self:
            if key in other:
                if type(self[key]) == type(other[key]):
                    if isinstance(self[key], (str, int)):
                        if self[key] != other[key]:
                            result["notequal"].append((prefix + "/" + key, (self[key], other[key])))
                            result["messages"].append("Values are different: %s[\"%s\"]=%s != %s[\"%s\"]=%s " % (
                                                                                self_name, key, self[key],
                                                                                other_name, key, other[key]
                                                                                )
                            )
                    elif isinstance(self[key], (list, tuple)):
                        result.update_extend(
                                                one_of_list_compare (
                                                    n0list(self[key]),
                                                    n0list(other[key]),
                                                    self_name + "[\"" + key + "\"]",
                                                    other_name + "[\"" + key + "\"]",
                                                    prefix + "/" + str(key),
                                                    elements_for_composite_key,
                                                    elements_for_compare
                                                )
                        )
                    elif isinstance(self[key], (dict, OrderedDict)):
                        result.update_extend(
                                                n0dict(self[key]).direct_compare_dict(
                                                    n0dict(other[key]),
                                                    self_name+"[\""+key+"\"]",
                                                    other_name+"[\""+key+"\"]",
                                                    prefix+"/"+str(key),
                                                    one_of_list_compare
                                                )
                        )
                    else:
                        result["difftypes"].append(
                            (
                                prefix + "/" + str(key),
                                (
                                    type(self[key]), self[key],
                                    type(other[key]), other[key]
                                )
                            )
                        )
                        result["messages"].append("Not expected type %s in %s[\"%s\"]" % (type(self[key]), key, self_name))
                else:
                    result["difftypes"].append(
                        (
                            prefix + "/" + str(key),
                            (
                                type(self[key]), self[key],
                                type(other[key]), other[key]
                            )
                        )
                    )
                    result["messages"].append("Types are different: %s[\"%s\"]=(%s)%s != %s[\"%s\"]=(%s)%s" %
                                                            (
                                                            self_name, key, type(self[key]), str(self[key]),
                                                            other_name, key, type(other[key]), str(other[key]),
                                                            )
                    )
                self_not_exist_in_other.remove(key)
                other_not_exist_in_self.remove(key)

        if self_not_exist_in_other:
            for key in self_not_exist_in_other:
                result["messages"].append("Element %s[\"%s\"]='%s' doesn't exist in %s" %
                                                                    (
                                                                        self_name,
                                                                        key,
                                                                        str(self[key]),
                                                                        other_name
                                                                    )
                )
                result["othernotfound"].append((prefix + "/" + str(key), self[key]))
        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                result["messages"].append("Element %s[\"%s\"]='%s' doesn't exist in %s" %
                                  (
                                      other_name,
                                      key,
                                      str(other[key]),
                                      self_name
                                  )
                )
                result["selfnotfound"].append((prefix + "/" + str(key), other[key]))
        return result
    # ******************************************************************************
    # ******************************************************************************
    def compare_dict(self,
                                other: n0dict,
                                self_name: str = "self",
                                other_name: str = "other",
                                prefix: str = "",
                                # ONLY FOR COMPLEX COMPARE
                                # Strictly recommended to init lists
                                # else in case of just only one attribute of element will be different
                                # both elements will be marked as not found (unique) inside the opposite list
                                elements_for_composite_key: tuple = (),  # None/empty means all
                                elements_for_compare: tuple = (),  # None/empty means all
    ) -> n0dict:
        return self.direct_compare_dict(
                    other,
                    self_name, other_name, prefix,
                    n0list.compare_list, elements_for_composite_key, elements_for_compare
        )
    # ******************************************************************************
    # ******************************************************************************
    def __FindElem(self, parent: n0dict, where_parts: list, value: str = None) -> tuple:
        """
        Private function: returns element/node by path where_parts:list in [0]
        if path is not found, returns last found element/node in [0], and not found sub-elements in [1]
        """
        child_name = where_parts[0]
        child_index = None
        if "[" in child_name and child_name.endswith("]"):
            child_name, child_index = child_name.split("[",2)
            child_index = child_index[:-1].strip().lower()
        
        if not child_name in parent:
            return (parent, where_parts) # Return what was found, and what was not found
        else:
            child = parent.get(child_name) # [] or None are possible results

        if child_index:
            if not isinstance(child, (list, tuple)): 
                raise IndexError("'%s' is not list but %s" % (child, type(child)))
            if not child_index.translate(str.maketrans("+-","00")).isnumeric():
                if child_index.startswith("last()"):
                    child_index = child_index[6:]
                    if not child_index or child_index.translate(str.maketrans("+-","00")).isnumeric(): # Py3 dirty fix
                        child_index = int(eval("-1"+child_index)) # FIXME: Very dark and dirty :-(
                    else:
                        raise IndexError("'Something strange with index 'last()%s' in '%s'" % (child_index, where_parts[0]))
                else:
                    raise IndexError("'%s' in '%s' is not an index" % (child_index, where_parts[0]))
            else:
                child_index = int(eval(child_index)) # FIXME: Very dark and dirty :-(
            if child_index >= len(child):
                raise IndexError("index of '%s' (%d) is beyond the length (%d) of %s" % (where_parts[0], child_index, len(child), child))
            if child_index < -len(child):
                raise IndexError("index of '%s' (%d) is below the length (%d) of %s" % (where_parts[0], child_index, len(child), child))
            child = child[child_index]
            
        if len(where_parts) > 1:
            return self.__FindElem(child, where_parts[1:], value) # Deeper and deeper
        elif len(where_parts) == 1:
            if value:
                parent.update({child_name: value})
            return (parent.get(child_name), None) # Parent element, nothing is left
        else:
            raise Exception("FATAL: Unexpected behavior with empty path")
    # ******************************************************************************
    # ******************************************************************************
    def __AddElem(self, parent: OrderedDict, where_parts: list, default_value: str = None) -> tuple:
        """
        Private function: create element by path where_parts:list and define it as default_value.
        If any of elements exists, then such element will be converted into array,
        and subpath will be continued from last element of such array
        """
        if not where_parts or not len(where_parts):
            return parent  # Created element

        if default_value and len(where_parts) == 1:
            current_value = default_value
        else:
            current_value = n0dict()

        if isinstance(parent, list): parent = parent[-1]  # If list put to the last node
        # NOT PREDICTED: What to do if will be requested to extend already existed element into node?
        child = parent.get(where_parts[0])
        if child:
            # The element with the same name exists
            if not isinstance(child, list):
                child = [child]
            child.append(current_value)
            # parent[where_parts[0]] = child # Return back updated value
            super(n0dict, parent).__setitem__(where_parts[0], child)

            if len(where_parts) == 1:
                return (child, [])

            child = parent[where_parts[0]][-1]
        else:
            parent.update({where_parts[0]: current_value})
            child = parent.get(where_parts[0])

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
                    )
                ),
                [itm for itm in what.split("/") if itm],  # Convert path what:str into list,
                                                          # remove all empty separators ("//" or leading/trailing "/"),
                value  # If optional argument 'value' is provided, put into destination path where+what.
            )
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
        found, not_found = self.__FindElem(self,
                                           [itm for itm in where.split("/") if itm] # Convert path where:str into list,
                                                                                    # remove all empty separators
                                                                                    # ("//" or leading/trailing "/")
        )
        if not_found:
            raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), where))
        ## NEVER RECONVERT OBJECTS!!!
        ## For example: return n0list(found) => dict["list"].append(newitem) => append will be applyed to NEW object!!!
        return found
    # ******************************************************************************
    # ******************************************************************************
    def __setitem__(self, where: str, value: str):
        """
        Private function:
        self[where1/where2/.../whereN] = value
            AKA
        self[where1][where2]...[whereN] = value
        
        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        flagSet = False
        if where.startswith("="):
            flagSet = True
            where = where[1:]
        where_parts = [itm for itm in where.split("/") if itm]

        if len(where_parts) == 1:
            return super(n0dict, self).__setitem__(where, value)
        else:
            if flagSet:
                found, not_found = self.__FindElem(super(n0dict, self), where_parts, value)
                if not_found:
                    raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), where))
                return found
            else:
                where1 = "/".join(where_parts[:-1])
                where2 = where_parts[-1]
                return self.AddElem(where1, where2, value)
    # ******************************************************************************
    # ******************************************************************************
    def __xpath(self, parent: OrderedDict, path: str = None, mode: int = None):
        """
        Private function: recursively collect elements xpath starts from parent
        """
        result = []
        for key, value in parent.items():
            if isinstance(value, list):
                for i,subitm in enumerate(value):
                    result += self.__xpath( subitm, "%s/%s[%d]" % (path, key, i), mode )
            elif isinstance(value, str):
                result.append( ("%s/%s" % (path, key), value) )
            elif isinstance(value, (n0dict, dict, OrderedDict)):
                result += self.__xpath( value, "%s/%s" % (path, key), mode )
            elif value == None:
                result.append( ("%s/%s" % (path, key), None) )
            else:
                raise Exception("%s/%s ==  %s" % (path, key, value))
        return result
    # ******************************************************************************
    # ******************************************************************************
    def xpath(self, mode: int = None):
        """
        Public function: collect elements xpath starts from root
        """
        return self.__xpath( self, "/", mode )
    # ******************************************************************************
    # ******************************************************************************
    def formated_xpath(self, mode: int = None):
        """
        Public function: collect elements xpath starts from root and print with indents
        """
        result = ""
        xpath_list = self.xpath()
        xpath_maxlen = max(len(itm[0]) for itm in xpath_list) + 2 # plus 2 chars '"]'
        for itm in xpath_list:
            result += ("['%-"+str(xpath_maxlen)+"s = %s\n") % (itm[0]+"']", '"'+itm[1]+'"' if itm[1] else "None")
        return result
    # ******************************************************************************
    # ******************************************************************************
    def isExist(self, xpath):
        """
        Public function: return empty lists in dict, if self[xpath] exists
        """
        validation_results = n0dict({
            "messages"      : [],
            "notequal"      : [],
            "difftypes"     : [],
            "selfnotfound"  : [],
            "othernotfound" : [],
        })
        # TODO: redo with 'in'
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
    def isTheSame(self, xpath, other_n0dict, other_xpath=None, transformation = lambda x: x):
        """
        Public function: return empty lists in dict, if transformation(self[xpath]) == transformation(other_n0dict[other_xpath])
        """
        if not other_xpath: other_xpath = xpath
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
