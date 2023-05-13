import typing
from .n0struct_utils import n0eval
from .n0struct_findall import findall as n0struct_findall__findall
from .n0struct_findall import findfirst as n0struct_findall__findfirst
# ******************************************************************************
# ******************************************************************************
class n0list_(list):
    def findall(self, xpath: str, raise_exception: bool = True):
        return n0struct_findall__findall(self, xpath, raise_exception)
    def findfirst(self, xpath: str, raise_exception: bool = True):
        return n0struct_findall__findfirst(self, xpath, raise_exception)
    # **************************************************************************
    # **************************************************************************
    # n0list_. _get()
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
            _parent_node, _node_name_index, cur_value, xpath_found_str, not_found_xpath_list = self._find(xpath, self, return_lists)
            if not not_found_xpath_list:
                return cur_value
            else:
                if raise_exception:
                    raise IndexError(f"not found '{'/'.join(not_found_xpath_list)}' in '{xpath_found_str}'")
                else:
                    return if_not_found
        else:
            try:
                return super(n0list_, self).__getitem__(n0eval(xpath))
            except IndexError as ex:
                if raise_exception:
                    raise ex
                else:
                    return if_not_found
    # **************************************************************************
    # n0list_. get()
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
    # n0list_. first()
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
            return super(n0list_, self).__getitem__(xpath)
    # # **************************************************************************
    # # def append(self, sigle_item):
    # # if isinstance(sigle_item, (list, n0list_)):
    # # raise (TypeError, f"({type(sigle_item)}){sigle_item} must be scalar")
    # # super(n0list_, self).append(sigle_item)  #append the item to itself (the list)
    # # return self
    # # **************************************************************************
    # # def extend(self, other_list):
    # # if not isinstance(other_list, (list, n0list_)):
    # # raise (TypeError, f"({type(sigle_item)}){sigle_item} must be list")
    # # super(n0list_, self).extend(other_list)
    # # return self
    # # **************************************************************************
    def _in(self, other_list, in_is_expected: bool):
        if not isinstance(other_list, (list, tuple)):
            other_list = [other_list]
        for itm in self:
            if (itm in other_list) == in_is_expected:
                return True
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
        if not isinstance(other_list, (list, tuple)):
            other_list = [other_list]
        for itm in other_list:
            if super(n0list_, self).__contains__(itm) == in_is_expected:
                return True
        return False
    # **************************************************************************
    def consists_of_any(self, other_list):
        return self._consists_of(other_list, True)
    # **************************************************************************
    def consists_of_all(self, other_list):
        return not self._consists_of(other_list, False)
    # **************************************************************************
    def __contains__(self, other_list):  # otherlist in n0list_([a])
        return self.consists_of_all(other_list)
    # **************************************************************************
    def not_consists_of_any(self, other_list):
        return not self._consists_of(other_list, True)
# ******************************************************************************
# ******************************************************************************
