import typing
from .n0struct_n0dict__ import n0dict__
from .n0struct_logging import n0pretty

# *****************************************************************************
# https://www.w3.org/TR/html4/sgml/entities.html#h-24.4.1
# https://www.htmlhelp.com/reference/html40/entities/special.html
html_entities = {
    # C0 Controls and Basic Latin
    0x22:           "&quot;",   # quotation mark = APL quote
    0x26:           "&amp;",    # ampersand
    0x3C:           "&lt;",     # less-than sign
    0x3E:           "&gt;",     # greater-than sign
    # Latin Extended-A
    0x152:          "&OElig;",  # latin capital ligature OE
    0x153:          "&oelig;",  # latin small ligature oe
    # ligature is a misnomer, this is a separate character in some languages
    0x160:          "&Scaron;", # latin capital letter S with caron
    0x161:          "&scaron;", # latin small letter s with caron
    0x178:          "&Yuml;",   # latin capital letter Y with diaeresis
    # Spacing Modifier Letters
    0x02C6:         "&circ;",   # modifier letter circumflex accent
    0x02DC:         "&tilde;",  # small tilde, U+02DC ISOdia
    # General Punctuation
    0x2002:         "&ensp;",   # en space
    0x2003:         "&emsp;",   # em space
    0x2009:         "&thinsp;", # thin space
    0x200C:         "&zwnj;",   # zero width non-joiner
    0x200D:         "&zwj;",    # zero width joiner
    0x200E:         "&lrm;",    # left-to-right mark
    0x200F:         "&rlm;",    # right-to-left mark
    0x2013:         "&ndash;",  # en dash
    0x2014:         "&mdash;",  # em dash
    0x2018:         "&lsquo;",  # left single quotation mark
    0x2019:         "&rsquo;",  # right single quotation mark
    0x201A:         "&sbquo;",  # single low-9 quotation mark
    0x201C:         "&ldquo;",  # left double quotation mark
    0x201D:         "&rdquo;",  # right double quotation mark
    0x201E:         "&bdquo;",  # double low-9 quotation mark
    0x2020:         "&dagger;", # dagger
    0x2021:         "&Dagger;", # double dagger
    0x2030:         "&permil;", # per mille sign
    0x2039:         "&lsaquo;", # single left-pointing angle quotation mark, it is proposed but not yet ISO standardized
    0x203A:         "&rsaquo;", # single right-pointing angle quotation mark, it is proposed but not yet ISO standardized
    0x20AC:         "&euro;",   # euro sign, U+20AC NEW
}
# **********************************************************************************************************************
class n0dict_(n0dict__):
    # *************************************************************************
    # XPATH
    # *************************************************************************
    def __xpath(self, value, path: str = None, mode: int = None) -> list:
        """
        Private function: recursively collect elements xpath starts from parent
        """
        result = []
        if isinstance(value, (list, tuple)):
            for i, subitm in enumerate(value):
                result += self.__xpath(subitm, f"{path}[{i}]", mode)
        elif isinstance(value, dict):
            for key, value in value.items():
                result += self.__xpath(value, f"{path}/{key}", mode)
        elif isinstance(value, (str, int, float)) or value is None:
            result.append((path, value))
        else:
            raise TypeError(f"Not expected type ({type(value)}) in {path} == {value}")
        return result
    # **************************************************************************
    def _xpath(self, mode: int = None) -> list:  # list[(xpath, value)]
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
        xpath_list = self._xpath(mode)
        if xpath_list:
            xpath_maxlen = max(len(itm[0]) for itm in xpath_list) + 2  # plus 2 chars '"]'
            for itm in xpath_list:
                result += ("['%-" + str(xpath_maxlen) + "s = %s\n") % \
                            (
                                itm[0] + "']",  # Don't move to the main part
                                ('"' + str(itm[1]) + '"') if itm[1] else "None"
                            )
        return result
    # **************************************************************************
    # XML
    # **************************************************************************
    def _xml(self, parent: dict, indent: int = 0, indent_size: int = 4) -> typing.Union[str, None]:
        """
        Private function: recursively export n0dict into xml result string
        """
        result = ""
        if parent is not None:
            if isinstance(parent, dict):
                if not len(parent.items()):
                    return ""
                for key, value in parent.items():
                    # if result and (len(parent) > 2 or key not in ("Parm",)):
                    if key not in ("Parm","ParmCode","Value"):
                        if result:
                            result += "\n"
                        result += f"{' '*indent}"

                    if isinstance(value, (list, tuple)):
                        if not value:
                            result += f"<{key}/>"
                        else:
                            result += f"<{key}>"
                            for i, subitm in enumerate(value):
                                result += "\n" + self._xml(subitm, indent+indent_size, indent_size)
                            result += f"\n{' '*indent}</{key}>"
                    elif isinstance(value, (int, float)):
                        if not key.startswith("@"):
                            result += f"<{key}>{value}</{key}>"
                        else:
                            raise NotImplementedError(f"Export of attibtures ({key}) is not supported yet")
                    elif isinstance(value, str):
                        if not key.startswith("@"):
                            result += f"<{key}>"
                            if value.lstrip().upper().startswith("<![CDATA[") and value.rstrip().endswith("]]>"):
                                result += f"\n{' '*(indent+indent_size)}{value}\n{' '*indent}"
                            else:
                                result += value.translate(html_entities)
                            result += f"</{key}>"
                        else:
                            raise NotImplementedError(f"Export of attibtures ({key}) is not supported yet")
                    elif isinstance(value, dict):
                        sub_result = self._xml(value, indent+indent_size, indent_size)

                        attribs = ""
                        attribs_of_current_key = [(__key[1:], __value) for __key,__value in value.items() if __key.startswith("@")]
                        if len(attribs_of_current_key):
                            for __key, __value in attribs_of_current_key:
                                attribs += f' {__key}="{__value}"'
                        if sub_result:
                            if '\n' in sub_result:
                                result += f"<{key}{attribs}>\n{sub_result}\n{' '*indent}</{key}>"
                            else:
                                if key in ("Parm",):
                                    result += f"{' '*indent}"
                                result += f"<{key}{attribs}>{sub_result.lstrip()}</{key}>"
                        else:
                            result += f"<{key}{attribs}/>"
                    elif value is None:
                        result += f"<{key}/>"
                    else:
                        raise TypeError(f"_xml(..): Unknown type ({type(value)}) {key} == {value}")
            elif isinstance(parent, (list, tuple)):
                if not len(parent):
                    return None
                for i, itm in enumerate(parent):
                    if i:
                        result += "\n"
                    result += self._xml(itm, indent+indent_size, indent_size)
            elif isinstance(parent, (str, int, float)):
                result += str(parent)
            else:
                raise TypeError(f"_xml(..): Unknown type ({type(parent)}) == {parent}")

            return result
        else:
            return ""
    # **************************************************************************
    def to_xml(self, indent: int = 0, indent_size: int = 4, encoding: str = "utf-8", quote: str = '"') -> str:
        """
        Public function: export self into xml result string
        """
        return (f'<?xml version={quote}1.0{quote} encoding={quote}{encoding}{quote}?>\n' if encoding else '') + \
            self._xml(self, indent, indent_size)
    # **************************************************************************
    # JSON
    # **************************************************************************
    def to_json(self,
                indent_size: int = 4,
                pairs_in_one_line = True,
                skip_empty_arrays: bool = False,
                compress: bool = False,
    ) -> str:
        """
        Public function: export self into json result string
        """
        if compress:
            indent_size = 0

        return n0pretty(
            self,
            show_object_type  = False,
            indent_size       = indent_size,
            quote             = '"',
            pairs_in_one_line = pairs_in_one_line,
            json_convention   = True,
            skip_empty_arrays = skip_empty_arrays,
            skip_simple_types = True,
            show_item_count   = False,
        )


################################################################################
__all__ = (
    'n0dict_',
    'html_entities',
)
################################################################################
