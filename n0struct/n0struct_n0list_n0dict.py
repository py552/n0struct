from __future__ import annotations  # Python 3.7+: for using own class name inside body of class
import typing

import xmltodict
import json
import contextlib
import datetime

from .n0struct_utils_compare import (
    get__flag_compare_check_different_types,
    get__flag_compare_return_difference_of_values,
    get__flag_compare_return_equal,
    get__flag_compare_return_equal_records,
    get__flag_compare_return_equal_elements,
    get__flag_compare_return_place,
    xpath_match,
    generate_composite_keys,
)

from .n0struct_logging import (
    n0print,
    n0debug,
    n0debug_calc,
    n0error,
)

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
            raise TypeError("n0list.__init__(..) takes exactly one notnamed argument (list/tuple)")
    # **************************************************************************
    # n0list. _find()
    # **************************************************************************
    def _find(self,
            xpath_list: typing.Union[str, list],
            parent_node,
            return_lists,
            xpath_found_str: str = "/") \
        ->  typing.Tuple[
                typing.Union[None, n0dict, n0list],
                typing.Union[None, str, int],
                typing.Union[None, typing.Any],
                str,
                typing.Union[None, list]
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
            raise IndexError(f"xpath ({type(xpath_list)})'{str(xpath_list)}' must be list or string")
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
                for i, next_parent_node in enumerate(parent_node):
                    if isinstance(next_parent_node, dict):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists,  xpath_found_str + f"[{i}]")
                    elif isinstance(next_parent_node, (list, tuple)):
                        cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                            cur_not_found_xpath_list = self._find(xpath_list[1:], next_parent_node, return_lists, xpath_found_str + f"[{i}]")
                    else:
                        raise TypeError(f"Unexpected type ({type(next_parent_node)}) of '{str(next_parent_node)}'")

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
                except Exception:
                    raise IndexError(f"Unknown index '{xpath_found_str}[{node_index_str}]'")

                if isinstance(parent_node, (list, tuple)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index_int >= len__parent_node or node_index_int < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, f"[{node_index_int}]", None, xpath_found_str, xpath_list
                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, f"[{node_index_int}]", parent_node[node_index_int], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    next_parent_node =  parent_node[node_index_int]
                    if isinstance(next_parent_node, dict):
                        return n0dict._find(next_parent_node, xpath_list[1:], next_parent_node, return_lists, f"{xpath_found_str}[{node_index_int}]")
                    if isinstance(next_parent_node, (list, tuple)):
                        return self._find(xpath_list[1:], next_parent_node, return_lists, f"{xpath_found_str}[{node_index_int}]")
                    else:
                        raise TypeError(f"Unexpected type ({type(next_parent_node)}) of {str(next_parent_node)}")
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
            raise TypeError(f"n0list.direct_compare(): other ({str(other)}) must be n0list")

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
                    f"List {self_name} is longer {other_name}: {self_name}[{i}]='{self[i]}' doesn't exist in {other_name}"
                )
                if get__flag_compare_return_place():
                    result["self_unique"].append((f"{prefix}[{i}]", self[i]))
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
                                f"{prefix}[{i}]",
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
                            "Values are different: " +
                            f"{self_name}[{i}]='{self[i]}'" +
                            " != " +
                            f"{other_name}['{i}']='{other[i]}'"
                        )
                    else:
                        if get__flag_compare_return_equal_records():
                            result["self_equal"].append(self)
                            result["other_equal"].append(other)
                elif isinstance(self[i], (list, tuple)):
                    result.update_extend(
                        self[i].direct_compare(
                            other[i],
                            f"{self_name}[{i}]",
                            f"{other_name}[{i}]",
                            f"{prefix}[{i}]",
                            # Not used in real, just for compatibility with compare(..)
                            composite_key=composite_key, compare_only=compare_only,
                            exclude_xpaths=exclude_xpaths, transform=transform,
                        )
                    )
                elif isinstance(self[i], dict):
                    result.update_extend(
                        n0dict(self[i]).direct_compare(
                            n0dict(other[i]),
                            f"{self_name}[{i}]",
                            f"{other_name}[{i}]",
                            f"{prefix}[{i}]",
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
                    raise TypeError(f"Not expected type {type(self[i])} in {self_name}[{i}]/{other_name}[{i}]")
            # ######### if type(self[i]) == type(other[i]):
            else:
                if get__flag_compare_check_different_types():
                    result["difftypes"].append(
                        (
                            f"{prefix}[{i}]",
                            (
                                type(self[i]),
                                self[i],
                                type(other[i]),
                                other[i]
                            )
                        )
                    )
                    result["differences"].append(
                        "!!Types are different: " +
                        f"{self_name}[{i}]=({type(self[i])}){self[i]}" +
                        " != " +
                        f"{other_name}[{i}]=({type(other[i])}){other[i]}"
                    )
                else:
                    result["not_equal"].append(
                        (
                            f"{prefix}[{i}]",
                            (
                                self[i],
                                other[i]
                            )
                        )
                    )
                    result["differences"].append(
                        "Values are different: " +
                        f"{self_name}[{i}]='{self[i]}'" +
                        " != " +
                        f"{other_name}['{i}']='{other[i]}'"
                    )

        # ######### for i in enumerate(self)[0]:
        if len(other) > len(self):
            # self list is SHORTER that other
            for i, itm in enumerate(other[len(self):]):
                i += len(self)
                result["differences"].append(
                    f"List {other_name} is longer {self_name}: {other_name}[{i}]='{other[i]}' doesn't exist in {self_name}"
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
            raise TypeError(f"n0list. compare(..): other ({str(other)}) must be n0list")
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
                                        f"{prefix}[{self_i}]",
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
                                        f"{prefix}[{self_i}]<>[{other_i}]",
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
                                "Values are different: " +
                                f"{self_name}[{self_i}]='{self[self_i]}'" +
                                " != " +
                                f"{other_name}[{other_i}]='{other[other_i]}'"
                            )
                        else:
                            # NOT TESTED! #2
                            if get__flag_compare_return_equal_records():
                                result["self_equal"].append(self)
                                result["other_equal"].append(other)
                    elif isinstance(self[self_i], (list, tuple)):
                        result.update_extend(
                            n0list(self[self_i]).compare(
                                n0list(other[other_i]),
                                f"{self_name}[{self_i}]",
                                f"{other_name}[{other_i}]",
                                f"{prefix}[{other_i}]" + f"<>[{other_i}]" if self_i != other_i else "",
                                composite_key=composite_key, compare_only=compare_only,
                                exclude_xpaths=exclude_xpaths, transform=transform,
                            )
                        )
                    elif isinstance(self[self_i], dict):
                        result.update_extend(
                            n0dict(self[self_i]).compare(
                                # n0dict(other[other_i]),  # 0.18
                                other[other_i],
                                f"{self_name}[{self_i}]",
                                f"{other_name}[{other_i}]",
                                f"{prefix}[{self_i}]" + (f"<>[{other_i}]" if self_i != other_i else ""),
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
                        raise TypeError(f"Not expected type {type(self[self_i])} in {self_name}[{self_i}]/{other_name}[{other_i}]")
                # ######### if type(self[i]) == type(other[i]):
                else:
                    if get__flag_compare_check_different_types():
                        result["difftypes"].append(
                            (
                                f"{prefix}[{self_i}]",
                                (
                                    type(self[self_i]), self[self_i],
                                    type(other[other_i]), other[other_i]
                                )
                            )
                        )
                        result["differences"].append(
                            "++Types are different: " +
                            f"{self_name}[{self_i}]=({type(self[self_i])}){self[self_i]}" +
                            " != " +
                            f"{other_name}[{other_i}]=({type(other[other_i])}){other[other_i]}"
                        )
                    else:
                        if self_i == other_i:
                            result["not_equal"].append(
                                (
                                    f"{prefix}[{self_i}]",
                                    (
                                        self[self_i],
                                        other[other_i]
                                    )
                                )
                            )
                        else:
                            result["not_equal"].append(
                                (
                                    f"{prefix}[{self_i}]<>[{other_i}]",
                                    (
                                        self[self_i],
                                        other[other_i]
                                    )
                                )
                            )
                        result["differences"].append(
                            "Values are different: " +
                            f"{self_name}[{self_i}]='{self[self_i]}'" +
                            " != " +
                            f"{other_name}[{other_i}]='{other[other_i]}'"
                        )
                del self_not_exist_in_other[[itm[0] for itm in self_not_exist_in_other].index(composite_key)]
                del other_not_exist_in_self[[itm[0] for itm in other_not_exist_in_self].index(composite_key)]
            # ######### if key in other_not_exist_in_self:
        # ######### for key in notmutable__self_not_exist_in_other:

        if self_not_exist_in_other:
            for composite_key, self_i in self_not_exist_in_other:
                result["differences"].append(
                    f"Element {self_name}[{self_i}]='{self[self_i]}' doesn't exist in {other_name}"
                )
                if get__flag_compare_return_place():
                    result["self_unique"].append((f"{prefix}[{self_i}]", self[self_i]))
                else:
                    result["self_unique"].append(self[self_i])

        if other_not_exist_in_self:
            for composite_key, other_i in other_not_exist_in_self:
                result["differences"].append(
                    f"Element {other_name}[{other_i}]='{other[other_i]}' doesn't exist in {self_name}"
                )
                if get__flag_compare_return_place():
                    result["other_unique"].append((f"{prefix}[{other_i}]", other[other_i]))
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
                _encoding = kw.pop("encoding", "utf-8-sig") # with possible UTF-8 BOM (Byte Order Mark)
                with open(_file, "rt", encoding=_encoding) as in_filehandler:
                    self.__init__(in_filehandler.read().strip(), **kw)
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
                    for key, value in zip(args[0][0::2], args[0][1::2]):
                        self.update({key: value})
                # [(key1, value1), (key2, value2), ..., (keyN, valueN)]
                elif all(isinstance(itm, (tuple, list)) and len(itm) == 2 and isinstance(itm[0], str) for itm in args[0]):
                    for pair in args[0]:
                        self.update({pair[0]: pair[1]})
                else:
                    raise TypeError(f"Expected even strings in the list [k1, v1, k2, v2] or list of pairs [[k1, v1],[k2, v2]] as argument for n0dict.__init__({args})")
            elif isinstance(args[0], zip):
                for key, value in args[0]:
                    self.update({key: value})
            else:
                raise TypeError(f"Expected str/dict/list/tuple/zip, but received {type(args[0])} as first argument for n0dict.__init__({args})")
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
            raise TypeError(f"n0dict. compare(..): other (({type(other)}){str(other)}) must be n0dict")
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
        whole_dict_is_equal = True

        # #############################################################
        # NEVER fetch data from the mutable list in the loop !!!
        # #############################################################
        for key in self_keys:
            if key in other:
                element_is_equal = True
                fullxpath = prefix + "/" + key
                if not xpath_match(fullxpath, exclude_xpaths):
                    # --- TRANSFORM: START -------------------------------------
                    # Transform self and other linked values with function transform[]()
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
                        if isinstance(self[key], (list, tuple)):
                            result.update_extend(
                                one_of_list_compare(
                                    n0list(self[key]),
                                    n0list(other[key]),
                                    f"{self_name}['{key}']",
                                    f"{other_name}['{key}']",
                                    f"{prefix}/{key}",
                                    composite_key=composite_key, compare_only=compare_only,
                                    exclude_xpaths=exclude_xpaths, transform=transform,
                                )
                            )
                        elif isinstance(self[key], dict):
                            result.update_extend(
                                n0dict(self[key]).compare(
                                    n0dict(other[key]),
                                    f"{self_name}['{key}']",
                                    f"{other_name}['{key}']",
                                    f"{prefix}/{key}",
                                    one_of_list_compare=one_of_list_compare,  # Only for n0dict. compare()
                                    composite_key=composite_key, compare_only=compare_only,
                                    exclude_xpaths=exclude_xpaths, transform=transform,
                                )
                            )
                        elif self[key] is None:
                            # Because of type(self[key]) == type(other[key]) and self[key] is None, so both are None
                            pass
                        else:
                            # raise TypeError(f"Not expected type {type(self[key])} in {key}['{self_name}']")
                        # if isinstance(self_value, (str, int, float, datetime.date)):
                            if self_value != other_value \
                                and (not compare_only or xpath_match(fullxpath, compare_only)):
                                # VERY IMPORTANT TO SHOW ORIGINAL VALUES, NOT TRANSFORMED
                                result["not_equal"].append(
                                    (
                                        f"{prefix}/{key}",
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
                                    "Values are different: " +
                                    f"{self_name}['{key}']={self[key]}" +
                                    " != " +
                                    f"{other_name}['{key}']={other[key]}"
                                )
                                element_is_equal = whole_dict_is_equal = False
                    else:
                        if not compare_only or xpath_match(fullxpath, compare_only):
                            element_is_equal = whole_dict_is_equal = False
                            if get__flag_compare_check_different_types():
                                result["difftypes"].append(
                                    (
                                        f"{prefix}/{key}",
                                        (
                                            type(self[key]), self[key],
                                            type(other[key]), other[key]
                                        )
                                    )
                                )
                                result["differences"].append(
                                    "*Types are different: " +
                                    f"{self_name}['{key}']=({type(self[key])}){self[key]}" +
                                    " != " +
                                    f"{other_name}['{key}']=({type(other[key])}){other[key]}"
                                )
                            else:
                                result["not_equal"].append((prefix + "/" + key, (self[key], other[key])))
                                result["differences"].append(
                                    "Values are different: " +
                                    f"{self_name}['{key}']={self[key]}" +
                                    " != " +
                                    f"{other_name}['{key}']={other[key]}"
                                )
                self_not_exist_in_other.remove(key)
                other_not_exist_in_self.remove(key)
                if element_is_equal and get__flag_compare_return_equal_elements():
                    result["self_equal"].append((key, self[key]))
                    result["other_equal"].append((key, other[key]))

        if self_not_exist_in_other:
            for key in self_not_exist_in_other:
                fullxpath = f"{prefix}/{key}"
                if not xpath_match(fullxpath, exclude_xpaths) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    whole_dict_is_equal = False
                    result["differences"].append(
                        f"Element {self_name}['{key}']='{self[key]}' doesn't exist in {other_name}"
                    )
                    if get__flag_compare_return_place():
                        result["self_unique"].append((fullxpath, self[key]))
                    else:
                        result["self_unique"].append(self[key])

        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                fullxpath = f"{prefix}/{key}"
                if not xpath_match(fullxpath, exclude_xpaths) \
                   and (not compare_only or xpath_match(fullxpath, compare_only)):
                    whole_dict_is_equal = False
                    result["differences"].append(
                        f"Element {other_name}['{key}']='{other[key]}' doesn't exist in {self_name}"
                    )
                    if get__flag_compare_return_place():
                        result["other_unique"].append((fullxpath, other[key]))
                    else:
                        result["other_unique"].append(other[key])

        if whole_dict_is_equal and get__flag_compare_return_equal_records():
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
    def _find(self,
            xpath_list: typing.Union[str, list],
            parent_node,
            return_lists,
            xpath_found_str: str = "/") \
        ->  typing.Tuple[
                typing.Union[None, n0dict, n0list],
                typing.Union[None, str, int],
                typing.Union[typing.Any],
                str,
                typing.Union[None, list]
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
            raise IndexError(f"xpath ({type(xpath_list)})'{str(xpath_list)}' must be list or string")
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
                            raise TypeError(f"If index is in '{cur_node_name_index}', then ({type(cur_node_index)})'{cur_node_index}' must be str")
                else:
                    nxt_parent_node = cur_parent_node

                if node_index or len(xpath_list) > 1:
                    if node_index:
                        return self._find([f"[{node_index}]"] + xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
                    else:
                        return self._find(                      xpath_list[1:], nxt_parent_node, return_lists, cur_found_xpath_str)
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
                raise IndexError(f"Internal error: Parent node '{xpath_found_str}' of '{node_name}' is redefined to ({type(parent_node)})'{str(parent_node)}', but must be n0dict")
            # ..................................................................
            # Try to check all [*] items in the loop
            # ..................................................................
            if node_name == "*":
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
                return self._find(
                                xpath_list[1:],
                                parent_node[node_name],
                                return_lists,
                                xpath_found_str + '/' + node_name
                )
            else:
                return self._find(
                                [
                                    f"[{node_index[0]}{node_index[1]}'{node_index[2]}']"
                                    if isinstance(node_index, tuple)
                                    else f"[{node_index}]"  # Because of mypy: error: Not all arguments converted during string formatting
                                ] + xpath_list[1:],
                                parent_node[node_name],
                                return_lists,
                                f"{xpath_found_str}/{node_name}"
                )
        # ##########################################################################################
        # Index in n0list (node_index is not None)
        # ##########################################################################################
        else:
            #--------------------------------
            # NOT FOUND: new element in n0list
            #--------------------------------
            if node_index == "new()":
                parent_node, node_name_index, cur_value, xpath_found_str, \
                    _not_found_xpath_list = self._find(xpath_found_str, self, return_lists)
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
                cur_values = n0list()
                fst_parent_node = fst_node_name_index = fst_value = fst_found_xpath_str = None
                for i, cur_node in enumerate(parent_node):
                    cur_parent_node, cur_node_name_index, cur_value, cur_found_xpath_str, \
                        cur_not_found_xpath_list = self._find([f"[{i}]"] + xpath_list[1:], parent_node, return_lists, xpath_found_str)
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
                        raise SyntaxError(f"Unknown comparing command in {str(node_index)}")

                    if node_index[1][0] == '!':
                        comparing_result = not comparing_result
                    elif node_index[1][0] != '=' and node_index[1][0] != '~':
                        raise SyntaxError(f"Unknown comparing command in {str(node_index)}")

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

                    if not isinstance(parent_node, dict):
                        raise IndexError(f"If key '{node_index[0]}' is set, then ({type(parent_node)})'{str(parent_node)}' must be n0dict at '{xpath_found_str}'")
                    if node_index[0] not in parent_node:
                        return parent_node, None, None, xpath_found_str, xpath_list

                    return self._find(
                                        [f"[text(){node_index[1]}{node_index[2]}]", ".."] + xpath_list[1:],
                                        parent_node[node_index[0]],
                                        return_lists,
                                        f"{xpath_found_str}/{node_index[0]}"
                    )
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Pure index
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            else:
                try:
                    node_index_int = n0eval(node_index)
                except:
                    raise IndexError(f"Unknown index '{xpath_found_str}[{node_index}]'")

                if isinstance(parent_node, (list, tuple)):
                    len__parent_node = len(parent_node)
                else:
                    len__parent_node = 1
                    parent_node = [parent_node]

                if node_index_int >= len__parent_node or node_index_int < -len__parent_node:
                    #--------------------------------
                    # NOT FOUND: Element in n0list
                    #--------------------------------
                    return parent_node, f"[{node_index_int}]", None, xpath_found_str, xpath_list

                if len(xpath_list) == 1:
                    #================================
                    # FOUND: the last is n0list
                    #================================
                    return parent_node, f"[{node_index_int}]", parent_node[node_index_int], xpath_found_str, None
                else:
                    #*******************************
                    # Deeper: any type under n0dict
                    #*******************************
                    return self._find(xpath_list[1:], parent_node[node_index_int], return_lists, f"{xpath_found_str}[{node_index_int}]")
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

        if cur_node_index is None:
            ####################################################################
            # Parent is DICTIONARY
            ####################################################################
            if cur_node_name:
                # if not isinstance(parent_node, (dict, OrderedDict, n0dict)):
                if not isinstance(parent_node, dict):
                    raise IndexError(f"If we are looking for key '{cur_node_name}' then parent ({type(parent_node)})'{str(parent_node)}' must be dictionary")
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
                            raise SyntaxError(f"Nonsence! Impossible to add {next_node_name}[{next_node_index}] to the {cur_node_name}"
                                            + (f"[{cur_node_index}]" if cur_node_index else "")
                                            + f" {str(parent_node)}"
                            )
                        parent_node.update({next_node_name: n0list([None])})
                        next_node = parent_node[next_node_name]
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
                        next_node_name_index = f"[{next_node_index}]"
                    else:
                        raise IndexError(f"Nonsense! How to create already existed node '{next_node_name}'?")
            else:
                if next_node_index != "new()":
                    raise IndexError(f"Expect new() for adding index, but got '{next_node_index}'")
                parent_node.append(None)
                next_node = parent_node
                next_node_name_index = "[last()]"
        else:
            ####################################################################
            # Parent is LIST or should be a list
            ####################################################################
            # Original code
            if cur_node_index == "new()":
            # FIX ME
            # or (isinstance(parent_node, (list, tuple)) and n0eval(cur_node_index) == len(parent_node)) \
            # or (isinstance(parent_node[cur_node_name], (list, tuple)) and n0eval(cur_node_index) == len(parent_node)[cur_node_name]):
                if cur_node_name and not isinstance(parent_node[cur_node_name], (list, tuple, n0list)):
                    ####################################################################
                    # Convert not LIST into the list
                    ####################################################################
                    if len(parent_node[cur_node_name]):
                        parent_node.update({cur_node_name: n0list([parent_node[cur_node_name]])})
                    else:
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
                        parent_node.append(n0dict({next_node_name: n0list()}))
                        next_node = parent_node[-1][next_node_name]
                        # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                        next_node_name_index = f"[{next_node_index}]"
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = f"[{next_node_index}]"
                else:
                    raise ValueError("Nonsence! Both next_node_name and next_node_index could NOT be empty")
            elif cur_node_index == "last()":
                # Came from previous level: we create [None] and point to [last()] for exchange
                if not isinstance(parent_node, (list, tuple, n0list)):
                    raise ValueError(f"Nonsence! if index '{cur_node_index}' is set, then ({type(parent_node)}){str(parent_node)} must be n0list")
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
                        next_node_name_index = f"[{next_node_index}]"
                elif next_node_index:
                    # List under list: [0][0] or [0]/[0]
                    parent_node.append(n0list([]))
                    next_node = parent_node[-1]
                    # Expected to have 'new()' in next_node_index, else it will be failed at the next step
                    next_node_name_index = f"[{next_node_index}]"
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
            # n0debug("xpath")
            # n0debug("new_value")
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
            raise TypeError(f"Received (type(xpath),{type(new_value)}) as argument, but expected (key, value) or (dict).")
        return self
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
