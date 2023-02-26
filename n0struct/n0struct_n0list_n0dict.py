from __future__ import annotations  # Python 3.7+: for using own class name inside body of class
import typing

import xmltodict
import json
import contextlib
import datetime

from .n0struct_utils_compare import get__flag_compare_check_different_types
from .n0struct_utils_compare import get__flag_compare_return_difference_of_values
from .n0struct_utils_compare import get__flag_compare_return_equal
from .n0struct_utils_compare import get__flag_compare_return_place
from .n0struct_utils_compare import xpath_match
from .n0struct_utils_compare import generate_composite_keys

from .n0struct_utils import n0eval
from .n0struct_utils_find import split_name_index

from .n0struct_n0list_ import n0list_
from .n0struct_n0dict_ import n0dict_

# ******************************************************************************
# ******************************************************************************
class n0list(n0list_):
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
            super(n0list, self).__init__(*args, **kw)
        elif isinstance(args, tuple):
            if len__args == 1:
                from_tuple = args[0]
            else:
                from_tuple = args
            _recursively = kw.get("recursively") or False
            for value in from_tuple:
                if _recursively:
                    # if isinstance(value, (dict, OrderedDict)):
                    if isinstance(value, dict):
                        value = n0dict(value, recursively = _recursively)
                    elif isinstance(value, (list, tuple)):
                        value = n0list(value, recursively = _recursively)
                self.append(value)
        else:
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
        [3] = xpath_found_str: str = "" if nothing found
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
                raise IndexError("Impossible to have complex index for lists")

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

                    if isinstance(next_parent_node, dict):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists,  xpath_found_str + f"[{i}]")
                    elif isinstance(next_parent_node, (list, tuple)):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = self._find(xpath_list[1:], next_parent_node, return_lists, xpath_found_str + f"[{i}]")
                    else:
                        raise TypeError("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))

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

                if isinstance(parent_node, (list, tuple)):
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
                    if isinstance(next_parent_node, dict):
                        return n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists, "%s[%d]" % (xpath_found_str, node_index_int))
                    if isinstance(next_parent_node, (list, tuple)):
                        return self._find(xpath_list[1:], next_parent_node, return_lists, "%s[%d]" % (xpath_found_str, node_index_int))
                    else:
                        raise TypeError("Unexpected type (%s) of %s" % (type(next_parent_node), str(next_parent_node)))
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
                if not returned["differences"]: self and other are equal with conditions:
                    except exclude_xpaths;
                    compare_only
                    transform
        """
        if continuity_check != "continuity_check":
            raise SyntaxError("Incorrect order of arguments")
        if not isinstance(other, n0list):
            raise TypeError("n0list.direct_compare(): other (%s) must be n0list" % str(other))

        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})
        if get__flag_compare_return_equal():
            result.update({"self_equal": []})
            result.update({"other_equal": []})

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
                if get__flag_compare_return_place():
                    result["self_unique"].append(("%s[%i]" % (prefix, i), self[i]))
                else:
                    result["self_unique"].append(self[i])
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
                                if isinstance(self_value, (datetime.date, datetime.datetime)):
                                    difference = datetime.datetime.fromtimestamp(float(other_value.timestamp()) - float(self_value.timestamp()))
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
                    else:
                        # NOT TESTED! #1
                        if get__flag_compare_return_equal():
                            result["self_equal"].append(self)
                            result["other_equal"].append(other)
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
                # elif isinstance(self[i], (n0dict, dict, OrderedDict)):
                elif isinstance(self[i], dict):
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
                    raise TypeError(
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
                if get__flag_compare_return_place():
                    result["other_unique"].append(("%s[%i]" % (prefix, i), other[i]))
                else:
                    result["other_unique"].append(other[i])
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
                if not returned["differences"]: self and other are equal with conditions:
                    except exclude_xpaths;
                    compare_only
                    transform
        """
        if continuity_check != "continuity_check":
            raise SyntaxError("n0list. compare(..): incorrect order of arguments")
        if not isinstance(other, n0list):
            raise TypeError("n0list. compare(..): other (%s) must be n0list" % str(other))
        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})
        if get__flag_compare_return_equal():
            result.update({"self_equal": []})
            result.update({"other_equal": []})

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
            if other_i is not None:
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
                    if isinstance(self_value, (str, int, float, datetime.date)):
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
                        else:
                            # NOT TESTED! #2
                            if get__flag_compare_return_equal():
                                result["self_equal"].append(self)
                                result["other_equal"].append(other)
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
                    elif isinstance(self[self_i], dict):
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
                    elif self[self_i] is None:
                        # type(self[self_i]) == type(other[other_i]) and self[self_i] is None
                        # So both are None
                        pass
                    else:
                        raise TypeError(
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
                if get__flag_compare_return_place():
                    result["self_unique"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
                else:
                    result["self_unique"].append(self[self_i])

        if other_not_exist_in_self:
            for composite_key, other_i in other_not_exist_in_self:
                result["differences"].append(
                    "Element %s[%d]='%s' doesn't exist in %s" %
                    (
                        other_name, other_i, str(other[other_i]),
                        self_name
                    )
                )
                if get__flag_compare_return_place():
                    result["other_unique"].append(("%s[%d]" % (prefix, other_i), other[other_i]))
                else:
                    result["other_unique"].append(other[other_i])

        return result
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
class n0dict(n0dict_):
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
            force_dict=True     =>  leave JSON subnodes as dict.
                                    by default all dictionaries will be converted into n0dict,
                                               but all lists will stay lists. lists could be
                                               converted into n0list only with recursively=True.
            force_dict=True is required to slightly decrease time for convertion of JSON-text into structure.

            recursively=True    =>  convert all dict/list/XML-text/JSON-text subnodes into n0dict/n0list.
                                    by default all subnodes are dict/list, only the root node is n0dict/n0list.
            recursively=True is required to have ability to apply n0dict/n0list speci-fic methods to all subnodes,
            not only to the root node. This option will impact to memory consumation.

            file=f"{file_path}" =>  load XML-text/JSON-text from {file_path}
        """
        len__args = len(args)
        if not len__args:
            _file = kw.pop("file", None)
            if _file:
                with open(_file, "rb") as in_filehandler:
                    buffer = in_filehandler.read()
                    if buffer[:3] == b'\xEF\xBB\xBF': # UTF-8 BOM (Byte Order Mark)
                        buffer = buffer[3:]
                    self.__init__(buffer.decode('utf-8').strip(), **kw)
            else:
                super(n0dict, self).__init__(*args, **kw)
        elif len__args == 1:
            # Not kw.pop()! Because of in case of .get "recursively" will be provided deeper into _constructor(..)
            _recursively = kw.get("recursively", False)
            if isinstance(args[0], str):
                if _recursively:
                    _constructor = self.__init__
                else:
                    _constructor = super(n0dict, self).__init__

                if args[0].strip()[0] == "<":
                    # https://github.com/martinblech/xmltodict/issues/252
                    # The main function parse has a force_n0dict keyword argument useful for this purpose.
                    _constructor(
                        xmltodict.parse(args[0], dict_constructor = n0dict),
                        **kw
                    )
                elif args[0].strip()[0] == "{":
                    # By default all JSON dictinaries will be converted into n0dict
                    _object_pairs_hook = None if kw.pop("force_dict", None) else n0dict
                    _constructor(
                        json.loads(args[0], object_pairs_hook = _object_pairs_hook),
                        **kw
                    )
            elif isinstance(args[0], dict):
                for key in args[0]:
                    value = args[0][key]
                    if _recursively:
                        if isinstance(value, dict):
                            value = n0dict(value, recursively = _recursively)
                        elif isinstance(value, (list, tuple)):
                            value = n0list(value, recursively = _recursively)
                    self.update({key: value})
            elif isinstance(args[0], (list, tuple)):
                # [key1, value1, key2, value2, ..., keyN, valueN]
                if (len(args[0]) % 2) == 0 and all(isinstance(itm, str) for itm in args[0][0::2]):
                    for key, value in zip(args[0][0::2],args[0][1::2]):
                        self.update({key: value})
                    # return None
                # [(key1, value1), (key2, value2), ..., (keyN, valueN)]
                elif all(isinstance(itm, (tuple,list)) and len(itm) == 2 and isinstance(itm[0], str) for itm in args[0]):
                    for pair in args[0]:
                        self.update({pair[0]: pair[1]})
                else:
                    raise TypeError("Expected even strings in the list [k1,v1,k2,v2] or list of pairs [[k1,v1],[k2,v2]] as argument for n0dict.__init__({args})")
            elif isinstance(args[0], zip):
                for key, value in args[0]:
                    self.update({key: value})
            else:
                raise TypeError("Expected str/dict/list/tuple/zip, but received {type((args[0])} as first argument for n0dict.__init__({args})")
        else:
            raise TypeError("n0dict.__init__(..) takes exactly one notnamed argument (string (XML or JSON) or dict/zip or paired tuple/list)")
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
            raise SyntaxError("n0dict. compare(..): incorrect order of arguments")
        if not isinstance(other, n0dict):
            raise TypeError("n0dict. compare(..): other ((%s)%s) must be n0dict" % (type(other), str(other)))
        result = n0dict({
            "differences":  [],
            "not_equal":    [],
            "self_unique":  [],
            "other_unique": [],
        })
        if get__flag_compare_check_different_types():
            result.update({"difftypes": []})
        if get__flag_compare_return_equal():
            result.update({"self_equal": []})
            result.update({"other_equal": []})

        self_keys = list(self.keys())
        self_not_exist_in_other = list(self.keys())
        other_not_exist_in_self = list(other.keys())
        is_still_equal = True

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
                        if isinstance(self_value, (str, int, float, datetime.date)):
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
                                is_still_equal = False
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
                        # elif isinstance(self[key], (dict, OrderedDict)):
                        elif isinstance(self[key], dict):
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
                            raise TypeError("Not expected type %s in %s[\"%s\"]" % (type(self[key]), key, self_name))
                    else:
                        if not compare_only or xpath_match(fullxpath, compare_only):
                            is_still_equal = False
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
                    is_still_equal = False
                    result["differences"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            self_name,
                            key,
                            str(self[key]),
                            other_name
                        )
                    )
                    if get__flag_compare_return_place():
                        result["self_unique"].append((fullxpath, self[key]))
                    else:
                        result["self_unique"].append(self[key])
                        
        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                fullxpath = "%s/%s" % (prefix, key)
                if not xpath_match(fullxpath, exclude_xpaths) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    is_still_equal = False
                    result["differences"].append(
                        "Element %s[\"%s\"]='%s' doesn't exist in %s" %
                        (
                            other_name,
                            key,
                            str(other[key]),
                            self_name
                        )
                    )
                    if get__flag_compare_return_place():
                        result["other_unique"].append((fullxpath, other[key]))
                    else:
                        result["other_unique"].append(other[key])

        if is_still_equal and get__flag_compare_return_equal():
            result["self_equal"].append(self)
            result["other_equal"].append(other)

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
            raise SyntaxError("n0dict. direct_compare(..): incorrect order of arguments")
        return self.compare(
            other,
            self_name, other_name, prefix,
            one_of_list_compare=one_of_list_compare,  # Only for n0dict. compare()
            composite_key=composite_key, compare_only=compare_only,
            exclude_xpaths=exclude_xpaths, transform=transform,
        )
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
        [3] = xpath_found_str: str = "" if nothing found
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
                return self._find(xpath_found_str, self, return_lists, "/")

        node_name, node_index = split_name_index(xpath_list[0])
        if not node_name and not node_index:
            n0debug("xpath_list")
            raise ValueError("Empty node_name and node_index")
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
                            raise TypeError("If index is in '%s', then (%s)'%s' must be str" %
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
            if isinstance(parent_node, (list, tuple)):
                # *******************************
                # Indulge #1 for incorrect syntax -- [*] was skipped for list in xpath
                # *******************************
                return self._find(["[*]"] + xpath_list, parent_node, return_lists, xpath_found_str)

            # if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
            if not isinstance(parent_node, dict):
                # raise IndexError("If key '%s' is set then (%s)'%s' must be n0dict at '%s'" %
                    # (node_name, type(parent_node), str(parent_node), xpath_found_str)
                # )
                # raise IndexError(f"If key '{node_name}' is set then ({type(parent_node)})'{str(parent_node)}' must be n0dict at '{xpath_found_str}'")
                raise IndexError(f"Internal error: Parent node '{xpath_found_str}' of '{node_name}' is redefined to ({type(parent_node)})'{str(parent_node)}', but must be n0dict")
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            if node_name == "*":
                # cur_values = n0list([])
                cur_values = n0list()
                fst_parent_node = fst_node_name_index = fst_value = fst_found_xpath_str = None
                for next_node_name in parent_node:
                    cur_parent_node, cur_node_name_index, \
                    cur_value, cur_found_xpath_str, cur_not_found_xpath_list = \
                            self._find(
                                        # [next_node_name] + new_xpath_list, # mypy: error: Name 'new_xpath_list' is not defined
                                        [next_node_name] + xpath_list,
                                        # 0.50: return_lists, parent_node,
                                        # return_lists,
                                        # parent_node,
                                        # 0.51: CORRECT: parent_node, return_lists,
                                        parent_node,
                                        return_lists,
                                        xpath_found_str
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
            if node_name not in parent_node:
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
                # # 0.51: NOT CORRECTLY FIXED
                # if isinstance(parent_node[node_name], (dict, OrderedDict, n0dict)):
                    return self._find(
                                    xpath_list[1:],
                                    parent_node[node_name],
                                    return_lists,
                                    xpath_found_str + '/' + node_name
                    )
                # # 0.51: NOT CORRECTLY FIXED
                # else:
                    # return parent_node, None, None, xpath_found_str, xpath_list # Impossible to go deeper
            else:
                # # 0.51: NOT CORRECTLY FIXED
                # if isinstance(parent_node[node_name], (list, tuple, n0list, dict, OrderedDict, n0dict)):
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
                # # 0.51: NOT CORRECTLY FIXED
                # else:
                    # return parent_node, None, None, xpath_found_str, xpath_list  # Impossible to go deeper
        # ##########################################################################################
        # Index in n0list (node_index is not None)
        # ##########################################################################################
        else:
            #--------------------------------
            # NOT FOUND: new element in n0list
            #--------------------------------
            if node_index == "new()":
                parent_node, node_name_index, cur_value, xpath_found_str, \
                    not_found_xpath_list = self._find(xpath_found_str, self, return_lists)
                if not isinstance(parent_node[node_name_index], (list, tuple)):
                    parent_node[node_name_index] = n0list([parent_node[node_name_index]])
                return parent_node[node_name_index], None, None, xpath_found_str, ["[new()]"] + xpath_list[1:]
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            elif node_index == "*":
                if not isinstance(parent_node, (list, tuple)):
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
                        raise SyntaxError("Unknown comparing command in %s" % str(node_index))

                    if node_index[1][0] == '!':
                        comparing_result = not comparing_result
                    elif node_index[1][0] != '=' and node_index[1][0] != '~':
                        raise SyntaxError("Unknown comparing command in %s" % str(node_index))

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
                    if isinstance(parent_node, (list, tuple)) and len(parent_node):
                        # *******************************
                        # Not correct: indulge #2 in incorrect syntax -- [*] was skipped for list in xpath
                        # *******************************
                        return self._find(["[*]"] + xpath_list, parent_node, return_lists, xpath_found_str)

                    # if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                    if not isinstance(parent_node, dict):
                        raise IndexError("If key '%s' is set then (%s)'%s' must be n0dict at '%s'" %
                            (node_index[0], type(parent_node), str(parent_node), xpath_found_str)
                        )
                    if node_index[0] not in parent_node:
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

                if isinstance(parent_node, (list, tuple)):
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
                # if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                if not isinstance(parent_node, dict):
                    raise IndexError("If we are looking for key '%s' then parent (%s)'%s' must be dictionary"
                                     % (cur_node_name, type(parent_node), str(parent_node)))
                parent_node = parent_node[cur_node_name]
            else:
                # It could happen, then just to add key into dictionary
                pass

            if next_node_name:
                if next_node_name not in parent_node:
                    # New node
                    if next_node_index:
                        # NEWFIX
                        if next_node_index != "new()" and next_node_index != "0":
                            # raise Exception("Nonsence! Impossible to add %s[%s] to the list (%s)%s"
                            #                 % (cur_node_name, cur_node_index, type(parent_node), str(parent_node)))
                            raise SyntaxError(f"Nonsence! Impossible to add {next_node_name}[{next_node_index}] to the {cur_node_name}"
                                            + (f"[{cur_node_index}]" if cur_node_index else "")
                                            + f" {str(parent_node)}"
                            )
                        parent_node.update({next_node_name: n0list([None])})
                        next_node = parent_node[next_node_name]
                        # next_node_name_index = "[%s]" % next_node_index
                        next_node_name_index = "[last()]"
                        # item[0] == None, will be reused at the next step with last()
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
            # Original code
            if cur_node_index == "new()":
            # FIXME
            # or (isinstance(parent_node, (list, tuple)) and n0eval(cur_node_index) == len(parent_node)) \
            # or (isinstance(parent_node[cur_node_name], (list, tuple)) and n0eval(cur_node_index) == len(parent_node)[cur_node_name]):
                if cur_node_name and not isinstance(parent_node[cur_node_name], (list, tuple, n0list)):
                # if not isinstance(parent_node[cur_node_name], (list, tuple, n0list)):
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
                    raise ValueError("Nonsence! Both next_node_name and next_node_index could NOT be empty")
            elif cur_node_index == "last()":
                # Came from previous level: we create [None] and point to [last()] for exchange
                if not isinstance(parent_node, (list, tuple, n0list)):
                    raise ValueError("Nonsence! if index '%s' is set then (%s)%s must be n0list"
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
            # New fix
            elif n0eval(cur_node_index) == len(parent_node):
                parent_node.append(None)
                next_node = parent_node
                next_node_name_index = "[last()]"
            else:
                raise SyntaxError(f"Nonsence! Impossible to add item {cur_node_index} to the list {str(parent_node)}")

        if len(xpath_list) == 1:
            return next_node, next_node_name_index
        else:
            return self._add(next_node, next_node_name_index, xpath_list[1:])
    # **************************************************************************
    def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> n0dict__:
        # **********************************************************************
        def multi_define(xpath, new_value):
            # if isinstance(new_value, (dict, OrderedDict, n0dict)):
            if isinstance(new_value, dict):
                self[xpath] = n0dict(new_value, recursively=True)
            elif isinstance(new_value, (list, tuple)):
                self[xpath] = n0list(new_value, recursively=True)
            else:
                self[xpath] = new_value
        # **********************************************************************
        if isinstance(xpath, dict) and new_value is None:
            for item_key in xpath:
                multi_define(item_key, xpath[item_key])
        elif isinstance(xpath, str) and new_value is not None:
            multi_define(xpath, new_value)
        else:
            raise TypeError("Received (%s,%s) as argument, but expected (key,value) or (dict)." % (type(xpath), type(new_value)))
        return self
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
