# 0.01 = 2020-07-25 = Initial version
from __future__ import annotations  # Python 3.7+
from collections import OrderedDict

# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
class n0list(list):
    # ******************************************************************************
    # ******************************************************************************
    def obvious_compare_list(
                self,
                other: n0list,
                self_name: str = "self",
                other_name: str = "other",
                prefix: str = "",
                dummy1 = None, # For compatibility with the list of input attributes of vogue_compare_list(..)
                dummy2 = None, # For compatibility with the list of input attributes of vogue_compare_list(..)
    ) -> n0dict:
        """
        Recursively compare self[i] with other[i] strictly according to the order of elements.
        If self[i] (other[i] must be the same) is n0list/n0dict, then goes deeper 
        with n0list.obvious_compare_list/n0dict.obvious_compare_dict(..)

        :param n0list self: etalon list for compare.
        :param n0list other: list to compare with etalon
        :param str self_name: <optional, default = "self"> dict/list format name before self
        :param str other_name: <optional, default = "other"> dict/list format name before other
        :param str prefix: <optional, default = ""> xpath format name before self/other
        :return:
                n0dict({
                    "messages"      :n0list([]), # messages generated for each case of not equality
                    "notequal"      :n0list([]), # generated if elements with the same xpath and type are not equal
                    "difftypes"     :n0list([]), # generated if elements with the same xpath have different types
                    "selfunique"    :n0list([]), # generated if elements from self list don't exist in other list
                    "otherunique"   :n0list([])  # generated if elements from other list don't exist in self list
                })
                if not returned["messages"]: self and other are totally equal.
        :rtype n0dict:
        """
        if not isinstance(other, n0list):
            raise Exception("n0list.obvious_compare_list(): other (%s) must be n0list" % str(other))
        result = n0dict({
            "messages": n0list([]),
            "notequal": n0list([]),
            "difftypes": n0list([]),
            "selfunique": n0list([]),
            "otherunique": n0list([])
        })

        for i,itm in enumerate(self):
            if i >= len(other):
                # other is SHORT
                result["selfunique"].append((prefix + "[" + str(i) + "]", self[i]))
                result["messages"].append("List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                                            (
                                                self_name, other_name,
                                                self_name, i, str(self[i]),
                                                other_name
                                            )
                )
                continue
            ########## if i >= len(other):
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
                        self[i].obvious_compare_list(
                            other[i],
                            self_name + "[" + str(i) + "]",
                            other_name + "[" + str(i) + "]",
                            prefix + "[" + str(i) + "]"
                        )
                    )
                elif isinstance(self[i], (n0dict, dict, OrderedDict)):
                    result.update_extend(
                        n0dict(self[i]).obvious_compare_dict(
                            n0dict(other[i]),
                            self_name + "[" + str(i) + "]",
                            other_name + "[" + str(i) + "]",
                            prefix + "[" + str(i) + "]",
                            self.obvious_compare_list
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
            ########## if type(self[i]) == type(other[i]):
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
        ########## for i in enumerate(self)[0]:
        if len(other) > len(self):
            # self is SHORT
            for i,itm in enumerate(other[len(self):]):
                i += len(self)
                result["otherunique"].append((prefix + "[" + str(i) + "]", other[i]))
                result["messages"].append("List %s is longer %s: %s[%d]='%s' doesn't exist in %s" %
                                          (
                                              other_name, self_name,
                                              other_name, i, str(other[i]),
                                              self_name
                                          )
                )
        return result
    # ******************************************************************************
    # ******************************************************************************
    def vogue_compare_list(
                self,
                other: n0list,
                self_name: str = "self",
                other_name: str = "other",
                prefix: str = "",
    # Strictly recommended to init lists
    # else in case of just only one attribute of element will be different
    # both elements will be marked as not found (unique) inside the opposite list
                list_elements_for_composite_key: tuple = (),  # None/empty means all
                list_elements_for_compare: tuple = (),  # None/empty means all
    ) -> n0dict:
        """
        Recursively compare self[i] with other[?] WITHOUT using order of elements.
        If self[i] (other[?] must be the same) is n0list/n0dict,
        then goes deeper with n0list.vogue_compare_list(..)/n0dict.obvious_compare_dict(..)

        :param n0list self: etalon list for compare.
        :param n0list other: list to compare with etalon
        :param str self_name: optional: dict/list format name before self
        :param str other_name: dict/list format name before other
        :param str prefix: xpath before self/other
        :param tuple list_elements_for_composite_key: ()/None/empty means all
        :param tuple list_elements_for_compare: ()/None/empty means all
        :return:
                n0dict({
                    "messages"      :n0list([]), # messages generated for each case of not equality
                    "notequal"      :n0list([]), # generated if elements with the same xpath and type are not equal
                    "difftypes"     :n0list([]), # generated if elements with the same xpath have different types
                    "selfunique"    :n0list([]), # generated if elements from self list don't exist in other list
                    "otherunique"   :n0list([])  # generated if elements from other list don't exist in self list
                })
                if not returned["messages"]: self and other are totally equal.
        :rtype n0dict:
        """
        if not isinstance(other, n0list):
            raise Exception("n0list.vogue_compare_list(): other (%s) must be n0list" % str(other))
        result = n0dict({
                        "messages": n0list([]),
                        "notequal": n0list([]),
                        "difftypes": n0list([]),
                        "selfunique": n0list([]),
                        "otherunique": n0list([])
        })

        def get_composite_keys(input_list: n0list, list_elements_for_composite_key: tuple) -> list:
            composite_keys = []
            for i, itm in enumerate(input_list):
                composite_key = ""
                for path_to_element in list_elements_for_composite_key if list_elements_for_composite_key else input_list[i]:
                    composite_key += path_to_element + "=" + str(input_list[i][path_to_element]) + ";"
                composite_keys.append(composite_key)
            return composite_keys
            

        self_not_exist_in_other = get_composite_keys(self, list_elements_for_composite_key)
        other_not_exist_in_self = get_composite_keys(other, list_elements_for_composite_key)

        notmutable__self_not_exist_in_other = self_not_exist_in_other.copy()
        notmutable__other_not_exist_in_self = other_not_exist_in_self.copy()
        for self_i,composite_key in enumerate(notmutable__self_not_exist_in_other):
            if composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)

                if type(self[self_i]) == type(other[other_i]):
                    if isinstance(self[self_i], (str, int)):
                        if self[self_i] != other[other_i]:
                            print(self_i)
                            print(other_i)
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
                            self.obvious_compare_list(
                                self[self_i], other[other_i],
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + ("<=>[" + str(other_i) + "]" if self_i != other_i else "")
                            )
                        )
                    elif isinstance(self[self_i], (n0dict, dict, OrderedDict)):
                        result.update_extend(
                            n0dict(self[self_i]).obvious_compare_dict(
                                n0dict(other[other_i]),
                                self_name + "[" + str(self_i) + "]",
                                other_name + "[" + str(other_i) + "]",
                                prefix + "[" + str(self_i) + "]" + ("<=>[" + str(other_i) + "]" if self_i != other_i else ""),
                                self.vogue_compare_list
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
                ########## if type(self[i]) == type(other[i]):
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
                ########## if type(self[i]) == type(other[i]):    
                self_not_exist_in_other.remove(composite_key)
                other_not_exist_in_self.remove(composite_key)
            ########## if key in other_not_exist_in_self:
        ########## for key in notmutable__self_not_exist_in_other:

        if self_not_exist_in_other:
            for composite_key in self_not_exist_in_other:
                self_i = notmutable__self_not_exist_in_other.index(composite_key)
                result["selfunique"].append((prefix + "[" + str(self_i) + "]", self[self_i]))
                result["messages"].append("Element %s[%d]='%s' doesn't exist in %s" %
                                            (
                                                self_name, self_i, str(self[self_i]),
                                                other_name
                                            )
                )
        if other_not_exist_in_self:
            for composite_key in other_not_exist_in_self:
                other_i = notmutable__other_not_exist_in_self.index(composite_key)
                result["otherunique"].append((prefix + "[" + str(other_i) + "]", other[other_i]))
                result["messages"].append("Element %s[%d]='%s' doesn't exist in %s" %
                                          (
                                              other_name, other_i, str(other[other_i]),
                                              self_name
                                          )
                )
                
        return result
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


class n0dict(OrderedDict):
    # ******************************************************************************
    def update_extend(self, other: n0dict) -> n0dict:
        if not isinstance(other, n0dict):
            raise Exception("n0dict.update_extend(): other (%s) must be n0dict" % str(other))
        self_keys = ",".join(sorted(self.keys()))
        other_keys = ",".join(sorted(other.keys()))
        if self_keys != other_keys:
            raise Exception("update_extend(): Structure of self (%s) must be the same with other (%s)" % (self_keys,other_keys))
        for key in self:
            if not isinstance(self[key], n0list):
                raise Exception("update_extend(): Element %s of self is %s, but must be n0list" % (key, type(self[key])))
            if not isinstance(other[key], n0list):
                raise Exception("update_extend(): Element %s of other is %s, but must be n0list" % (key, type(self[key])))
            self[key].extend(other[key])
        return self
    ################################################################################
    ################################################################################
    def obvious_compare_dict(self,
                            other: n0dict,
                            self_name: str = "self",
                            other_name: str = "other",
                            prefix: str = "",
                            one_of_list_compare = n0list.obvious_compare_list,
                            # ONLY FOR VOGUE
                            # Strictly recommended to init lists
                            # else in case of just only one attribute of element will be different
                            # both elements will be marked as not found (unique) inside the opposite list
                            list_elements_for_composite_key: tuple = (),  # None/empty means all
                            list_elements_for_compare: tuple = (),  # None/empty means all
    ) -> n0dict:
        if not isinstance(other, n0dict):
            raise Exception("n0dict.obvious_compare_dict(): other (%s) must be n0dict" % str(other))
        result = n0dict({
            "messages": n0list([]),
            "notequal": n0list([]),
            "difftypes": n0list([]),
            "selfunique": n0list([]),
            "otherunique": n0list([])
        })

        self_not_exist_in_other = list(self.keys())
        other_not_exist_in_self = list(other.keys())

        ##############################################################
        # NEVER fetch data from the mutable list in the loop !!!
        ##############################################################
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
                                                    list_elements_for_composite_key,
                                                    list_elements_for_compare
                                                )
                        )
                    elif isinstance(self[key], (dict, OrderedDict)):
                        result.update_extend(
                                                n0dict(self[key]).obvious_compare_dict(
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
                result["selfunique"].append((prefix + "/" + str(key), self[key]))
                result["messages"].append("Element %s[\"%s\"]='%s' doesn't exist in %s" %
                                                                    (
                                                                        self_name,
                                                                        key,
                                                                        str(self[key]),
                                                                        other_name
                                                                    )
                )
        if other_not_exist_in_self:
            for key in other_not_exist_in_self:
                result["otherunique"].append((prefix + "/" + str(key), other[key]))
                result["messages"].append("Element %s[\"%s\"]='%s' doesn't exist in %s" %
                                  (
                                      other_name,
                                      key,
                                      str(other[key]),
                                      self_name
                                  )
                )
        return result
    # ******************************************************************************
    # ******************************************************************************
    def vogue_compare_dict(self,
                                other: n0dict,
                                self_name: str = "self",
                                other_name: str = "other",
                                prefix: str = "",
                                # ONLY FOR VOGUE
                                # Strictly recommended to init lists
                                # else in case of just only one attribute of element will be different
                                # both elements will be marked as not found (unique) inside the opposite list
                                list_elements_for_composite_key: tuple = (),  # None/empty means all
                                list_elements_for_compare: tuple = (),  # None/empty means all
    ) -> n0dict:
        return self.obvious_compare_dict(
                    other,
                    self_name, other_name, prefix,
                    n0list.vogue_compare_list, list_elements_for_composite_key, list_elements_for_compare
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
                        super(n0dict, self),
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
        """
        # found, not_found = self.__FindElem(super(n0dict, self)
        found, not_found = self.__FindElem(self,
                                           [itm for itm in where.split("/") if itm] # Convert path where:str into list,
                                                                                    # remove all empty separators
                                                                                    # ("//" or leading/trailing "/")
        )
        if not_found:
            raise IndexError("'%s' is not found in path '%s'" % ("/".join(not_found), where))
        return found
    # ******************************************************************************
    # ******************************************************************************
    def __setitem__(self, where: str, value: str):
        """
        Private function:
        self[where1/where2/.../whereN] = value
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
        # print(self.__xpath(super(n0dict, self), "/", mode))
        return self.__xpath( self, "/", mode )
    # ******************************************************************************
    # ******************************************************************************
    def print_xpath(self, mode: int = None):
        """
        Public function: collect elements xpath starts from root and print with indents
        """
        xpath_list = self.xpath()
        xpath_maxlen = max(len(itm[0]) for itm in xpath_list) + 2 # plus 2 chars '"]'
        for itm in xpath_list:
            print(("['%-"+str(xpath_maxlen)+"s = %s") % (itm[0]+"']", '"'+itm[1]+'"' if itm[1] else "None"))
    # ******************************************************************************
    # ******************************************************************************
    def isTheSame(self, xpath, other_n0dict, other_xpath,  transformation = lambda x: x):
        validation_result = []
        validation_result.extend(self.isExist(xpath))
        validation_result.extend(other_n0dict.isExist(other_xpath))
        validation_result = list(filter(None, validation_result))
        if validation_result: 
            # print("## validation_result="+str(validation_result))
            return validation_result

        try:
            if transformation(self[xpath]) == transformation(other_n0dict[other_xpath]):
                return []
        except:
            pass
        return ["[%s]=='%s' != [%s]=='%s'" % (
                    xpath,
                    transformation(self[xpath]),
                    other_xpath,
                    transformation(other_n0dict[other_xpath])
                    )
               ]
    # ******************************************************************************
    # ******************************************************************************
    def isExist(self, xpath):
        try:
            if self[xpath]:
                return []
        except:
            pass
        return ["[%s] doesn't exist" % xpath]
    # ******************************************************************************
    # ******************************************************************************
    def isEqual(self, xpath, value):
        validation_result = self.isExist(xpath)
        if validation_result:
            return validation_result

        try:
            if self[xpath] == value:
                return []
        except:
            pass
        return ["[%s]=='%s' != '%s'" % (xpath, self[xpath], value)]
    # ******************************************************************************
    # ******************************************************************************
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
