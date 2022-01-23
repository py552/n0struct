from .n0struct_n0dict__ import n0dict__
from .n0struct_logging import n0pretty
# ******************************************************************************
# ******************************************************************************
class n0dict_(n0dict__):
    # **************************************************************************
    # XPATH
    # **************************************************************************
    def __xpath(self, value, path: str = None, mode: int = None) -> list:
        """
        Private function: recursively collect elements xpath starts from parent
        """
        result = []
        if isinstance(value, (list, tuple)):
            for i, subitm in enumerate(value):
                result += self.__xpath(subitm, "%s[%d]" % (path, i), mode)
        elif isinstance(value, dict):
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
        if xpath_list:
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
    def __xml(self, parent: dict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export n0dict into xml result string
        """
        result = ""
        if not parent is None:
            if isinstance(parent, dict):
                if not len(parent.items()):
                    return ""
                for key, value in parent.items():
                    if result:
                        result += "\n"
                    if isinstance(value, (list, tuple)):
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
                    elif isinstance(value, dict):
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
            elif isinstance(parent, (list, tuple)):
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
    def __json(self, parent: dict, indent: int, inc_indent: int) -> str:
        """
        Private function: recursively export n0dict into json result string
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
                        if isinstance(subitm, dict):
                            sub_result += (" " * (indent + inc_indent) + "{\n%s\n" + " " * (
                                    indent + inc_indent) + "}") % sub_sub_result
                        elif isinstance(subitm, (list, tuple)):
                            sub_result += (" " * (indent + inc_indent) + "[\n%s\n" + " " * (
                                    indent + inc_indent) + "]") % sub_sub_result
                if sub_result:
                    result += (" " * indent + '"%s": [\n%s\n' + " " * indent + "]") % (key, sub_result)
                else:
                    result += " " * indent + '"%s": null' % key
            elif isinstance(value, str):
                result += " " * indent + ('"%s": "%s"' % (key, value))
            elif isinstance(value, dict):
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
    # **************************************************************************
    def to_json(self, indent: int = 4, pairs_in_one_line = True, skip_none = False, skip_empty_arrays = False) -> str:
        """
        Public function: export self into json result string
        """
        return n0pretty(self,
                        show_type=False,
                        auto_quotes=False,
                        __quotes='"',
                        __indent_size=indent,
                        pairs_in_one_line=pairs_in_one_line,
                        skip_none=skip_none,
                        skip_empty_arrays=skip_empty_arrays
        )
# ******************************************************************************
# ******************************************************************************
