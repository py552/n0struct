from __future__ import annotations  # Python 3.7+: for using own class name inside body of class
import typing
from .n0struct_utils_find import split_name_index
from .n0struct_findall import findall as n0struct_findall__findall
from .n0struct_findall import findfirst as n0struct_findall__findfirst
from .n0struct_files import n0eval
# from .n0struct_logging import *
# ******************************************************************************
# ******************************************************************************
class n0dict__(dict):
    def findall(self, xpath: str, raise_exception: bool = True):
        return n0struct_findall__findall(self, xpath, raise_exception)
    def findfirst(self, xpath: str, raise_exception: bool = True):
        return n0struct_findall__findfirst(self, xpath, raise_exception)
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
            raise IndexError("xpath '%s' is not valid" % str(xpath))
        if xpath.startswith('?'):
            xpath = xpath[1:]
            raise_exception = False
            if_not_found = ''
        if any(char in xpath for char in "/["):
            parent_node, node_name_index, cur_value, xpath_found_str, not_found_xpath_list = self._find(xpath, self, return_lists)
            if not not_found_xpath_list:
                return cur_value
            else:
                if raise_exception:
                    raise IndexError("not found '%s' in '%s'" % ('/'.join(not_found_xpath_list), xpath_found_str))
                else:
                    return if_not_found
        else:
            try:
                return super(n0dict__, self).__getitem__(xpath)
            except KeyError as ex:
                if raise_exception:
                    raise ex
                else:
                    return if_not_found
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
        if isinstance(result, (list, tuple)) and len(result) == 1:
            result = result[0]
        return result
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
            parent_node, node_name_index, cur_value, xpath_found_str, not_found_xpath_list = self._find(xpath, self, return_lists = True)
            if not_found_xpath_list:
                parent_node, node_name_index = self._add(parent_node, node_name_index, not_found_xpath_list)

            node_name, node_index = split_name_index(node_name_index)
            if isinstance(parent_node, dict):
                if node_index:
                    raise IndexError("How is it possible: index '%s' for dictionary (%s)'%s'?"% (node_index, type(parent_node), parent_node))
                parent_node.update({node_name_index: new_value})
            elif isinstance(parent_node, (list, tuple)):
                if node_name:
                    raise IndexError("How is it possible: key '%s' for list (%s)'%s'?" % (node_name, type(parent_node), parent_node))
                eval_node_index = n0eval(node_index)
                parent_node[n0eval(node_index)] = new_value
            else:
                raise TypeError("How is it possible: unknown type of parent node (%s) of '%s'" % (type(parent_node), parent_node))
        else:
            super(n0dict__, self).__setitem__(xpath, new_value)

        return new_value  # For speed
    # **************************************************************************
    def delete(self, xpath: str, recursively: bool = False) -> n0dict__:
        xpath_list = xpath.split('/')
        for i,last_xpath_index in enumerate(range(len(xpath_list), 0, -1)):
            parent_node, node_name_index, cur_value, xpath_found_str, not_found_xpath_list = \
                self._find(xpath_list[0:last_xpath_index], self, return_lists=True)
            if i == 0 or (
                recursively and
                isinstance(cur_value, n0dict__) and not len(cur_value)
            ):
                if isinstance(parent_node, list) and not isinstance(node_name_index, int):
                    if not isinstance(node_name_index, str) or not node_name_index.startswith('[') or not node_name_index.endswith(']'):
                        raise IndexError(f"Not expactable index for list {node_name_index}")
                    node_name_index = n0eval(node_name_index[1:-1])
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
            elif isinstance(validate, (list, tuple)):
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
    # **************************************************************************
    # **************************************************************************
    def update_extend(self, other):
        if other is None:
            return self
        elif isinstance(other, dict):
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
        elif isinstance(other, (list, tuple)):
            key = list(self.items())[0][0]  # [0]= first item, [0] = key
            for itm in other:
                if isinstance(itm, (list, tuple)):
                    self[key].extend(itm)
                else:
                    self[key].append(itm)
        else:
            raise TypeError("Unexpected type of other: " + str(type(other)))
        return self
    # **************************************************************************
    # **************************************************************************
    def isExist(self, xpath) -> dict:
        """
        Public function: return empty lists in dict, if self[xpath] exists
        """
        validation_results = dict({
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
    def has_all(self, tupple_of_keys: typing.Union[tuple, list]) -> bool:
        for key in tupple_of_keys:
            if key not in self or not self[key]:
                return False
        return True
    # **************************************************************************
    # **************************************************************************
    def has_any_of(self, tupple_of_keys: typing.Union[tuple, list]) -> bool:
        for key in tupple_of_keys:
            if key in self:
                return True
        return False
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
# ******************************************************************************
# ******************************************************************************
