import re
from typing import Any, List, Tuple, Optional, Union, Generator
from pathlib import Path

# from .n0struct_logging import (
    # n0debug,
    # n0debug_calc,
    # # n0error,
    # n0pretty,
# )

from .n0struct_data_to_json import data_to_json
from .n0struct_data_to_xml import data_to_xml
from .n0struct_data_to_xpath import data_to_xpath

########################################################################################################################
########################################################################################################################
########################################################################################################################

regex_attached_index = re.compile(r'^([^[\]]+)(\[[^\]]*\])?$')
regex_brackets =  re.compile(r'\[([^\]]+)\]')
regex_first_bracket =  re.compile(r'\[')
class n0XPathParser:
    """ XPath expression parser for working with complex data structures. """
    def __init__(self):
        self.path_parts = []
        self.current_path = []

    def _parse_xpath(self, xpath: str) -> List[dict]:
        """ Parse XPath expression into components with enhanced format support. """
        parts = []

        # Split by slashes first, but preserve structure
        segments = [s for s in xpath.split('/') if s]

        for segment in segments:
            if not segment:
                continue

            # Check if segment is just an index [0], [*], etc.
            if segment.startswith('[') and segment.endswith(']'):
                parts.append(self._parse_index_part(segment))
                continue

            # Parse segment with potential attached index
            match = regex_attached_index.match(segment)
            if match:
                name, index_part = match.groups()

                # Add the named part
                name_part = self._create_named_part(name)
                parts.append(name_part)

                # Add index part if present
                if index_part:
                    parts.append(self._parse_index_part(index_part))
            else:
                # Fallback - treat as simple name
                parts.append(self._create_named_part(segment))

        return parts

    def _create_named_part(self, name: str) -> dict:
        """Create a named part structure."""
        result = {
            'type': 'node',
            'name': name,
            'conditions': [],
            'is_wildcard': False,
            'is_recursive': False,
            'is_parent': False,
            'auto_first': False  # New flag for automatic first element selection
        }

        if name == '..':
            result['type'] = 'parent'
            result['is_parent'] = True
        elif name == '*':
            result['is_wildcard'] = True
        elif name == '**':
            result['is_recursive'] = True

        return result

    def _parse_index_part(self, index_str: str) -> dict:
        """Parse index part like [0], [*], etc."""
        result = {
            'type': 'index',
            'name': None,
            'conditions': [],
            'is_wildcard': False,
            'is_recursive': False,
            'is_parent': False,
            'auto_first': False
        }

        # Remove brackets
        index_content = index_str[1:-1]

        if index_content == '*':
            result['conditions'].append({'type': 'any_index'})
        elif index_content.isdigit():
            result['conditions'].append({'type': 'index', 'value': int(index_content)})
        elif index_content.startswith('text()='):
            text_value = index_content[7:].strip('"\'')
            result['conditions'].append({'type': 'text', 'value': text_value})
        else:
            # Try to parse as number anyway
            try:
                result['conditions'].append({'type': 'index', 'value': int(index_content)})
            except ValueError:
                result['conditions'].append({'type': 'text', 'value': index_content})

        return result

    def _parse_single_part(self, part: str) -> dict:
        """Parse single XPath part (legacy method for compatibility)."""
        result = {
            'type': 'node',
            'name': None,
            'conditions': [],
            'is_wildcard': False,
            'is_recursive': False,
            'is_parent': False,
            'auto_first': False
        }

        # Handle special cases
        if part == '..':
            result['type'] = 'parent'
            result['is_parent'] = True
            return result
        elif part == '*':
            result['is_wildcard'] = True
            return result
        elif part == '**':
            result['is_recursive'] = True
            return result

        # Find conditions in brackets
        conditions = regex_brackets.findall(part)
        # Node name (before first bracket or entire part)
        name_part = regex_first_bracket.split(part)[0]
        if name_part == '*':
            result['is_wildcard'] = True
        elif name_part == '**':
            result['is_recursive'] = True
        else:
            result['name'] = name_part if name_part else None

        # Process conditions
        for condition in conditions:
            if condition == '*':
                result['conditions'].append({'type': 'any_index'})
            elif condition.isdigit():
                result['conditions'].append({'type': 'index', 'value': int(condition)})
            elif condition.startswith('text()='):
                text_value = condition[7:].strip('"\'')
                result['conditions'].append({'type': 'text', 'value': text_value})

        return result

    def _build_path(self, path_parts: List[str]) -> str:
        """Build path string from parts."""
        if not path_parts:
            return '/'

        result = ''
        for part in path_parts:
            if part.startswith('['):
                result += part
            else:
                result += '/' + part

        return result if result else '/'


########################################################################################################################

    def find_nodes(
        self,
        data: Any,
        xpath: str,
        first_only: bool = False,
    ) -> Union[List[Tuple[str, Any, Any, Union[str, int]]], Optional[Tuple[str, Any, Any, Union[str, int]]], None]:
        if first_only:
            gen = self._find_nodes_generator(data, xpath)
            try:
                return next(gen)
            except StopIteration:
                return None
        else:
            return list(self._find_nodes_generator(data, xpath))

    def _find_nodes_generator(
        self,
        data: Any,
        xpath: str,
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        xpath = xpath.strip('/')
        if not xpath:
            yield ('/', data, None, None)
            return

        parts = self._parse_xpath(xpath)
        yield from self._search_recursive(data, parts, [], None, None)

    def _search_recursive(
        self,
        data: Any,
        parts: List[dict],
        current_path: List[str],
        parent: Any,
        parent_key: Union[str, int],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        if not parts:
            yield (self._build_path(current_path), data, parent, parent_key)
            return

        current_part = parts[0]
        remaining_parts = parts[1:]

        if current_part['is_parent']:
            if len(current_path) > 0:
                parent_path = current_path[:-1]
                yield from self._search_recursive(data, remaining_parts, parent_path, parent, parent_key)
            return

        if current_part['is_recursive']:
            yield from self._recursive_deep_search(data, remaining_parts, current_path, parent, parent_key)
            return

        if current_part['type'] == 'index':
            if isinstance(data, list):
                yield from self._handle_list_index(data, current_part, remaining_parts, current_path)
            elif not isinstance(data, dict):
                yield from self._handle_scalar_index(data, current_part, remaining_parts, current_path, parent, parent_key)
            return

        if isinstance(data, dict):
            yield from self._search_in_dict(data, current_part, remaining_parts, current_path)
        elif isinstance(data, list):
            yield from self._search_in_list(data, current_part, remaining_parts, current_path)
        else:
            for condition in current_part.get('conditions', []):
                if condition['type'] == 'text' and str(data) == condition['value']:
                    if not remaining_parts:
                        yield (self._build_path(current_path), data, parent, parent_key)

    def _handle_list_index(
        self,
        data: list,
        part: dict,
        remaining_parts: List[dict],
        current_path: List[str],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        for condition in part.get('conditions', []):
            if condition['type'] == 'index':
                idx = condition['value']
                if 0 <= idx < len(data):
                    new_path = current_path + [f'[{idx}]']
                    if remaining_parts:
                        # yield from self._search_recursive(data[idx], remaining_parts, new_path, data, idx)
                        yield from self._search_recursive(list.__getitem__(data, idx), remaining_parts, new_path, data, idx)
                    else:
                        # yield (self._build_path(new_path), data[idx], data, idx)
                        yield (self._build_path(new_path), list.__getitem__(data, idx), data, idx)
            elif condition['type'] == 'any_index':
                for idx, item in enumerate(data):
                    new_path = current_path + [f'[{idx}]']
                    if remaining_parts:
                        yield from self._search_recursive(item, remaining_parts, new_path, data, idx)
                    else:
                        yield (self._build_path(new_path), item, data, idx)

    def _handle_scalar_index(
        self,
        data: Any,
        part: dict,
        remaining_parts: List[dict],
        current_path: List[str],
        parent: Any,
        parent_key: Union[str, int],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        for condition in part.get('conditions', []):
            if condition['type'] == 'index':
                idx = condition['value']
                if idx == 0:
                    new_path = current_path + [f'[{idx}]']
                    if remaining_parts:
                        yield from self._search_recursive(data, remaining_parts, new_path, parent, parent_key)
                    else:
                        yield (self._build_path(new_path), data, parent, parent_key)
            elif condition['type'] == 'any_index':
                new_path = current_path + ['[0]']
                if remaining_parts:
                    yield from self._search_recursive(data, remaining_parts, new_path, parent, parent_key)
                else:
                    yield (self._build_path(new_path), data, parent, parent_key)

    def _search_in_dict(
        self,
        data: dict,
        part: dict,
        remaining_parts: List[dict],
        current_path: List[str],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        for key, value in data.items():
            should_process = False
            new_path = current_path + [str(key)]

            if part['is_wildcard'] or part['name'] is None or part['name'] == key:
                should_process = True

            if part.get('conditions'):
                for condition in part['conditions']:
                    if condition['type'] == 'text':
                        if str(key) == condition['value']:
                            should_process = True
                        else:
                            should_process = False
                            break

            if should_process:
                if isinstance(value, list) and remaining_parts and not any(rp['type'] == 'index' for rp in remaining_parts[:1]):
                    if len(value) > 0:
                        if remaining_parts:
                            yield from self._search_recursive(value[0], remaining_parts, new_path + ['[0]'], value, 0)
                        else:
                            yield (self._build_path(new_path + ['[0]']), value[0], value, 0)
                else:
                    if remaining_parts:
                        yield from self._search_recursive(value, remaining_parts, new_path, data, key)
                    else:
                        yield (self._build_path(new_path), value, data, key)

    def _search_in_list(
        self,
        data: list,
        part: dict,
        remaining_parts: List[dict],
        current_path: List[str],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        has_index_conditions = any(c['type'] in ['index', 'any_index'] for c in part.get('conditions', []))

        if has_index_conditions:
            for condition in part.get('conditions', []):
                if condition['type'] == 'index':
                    idx = condition['value']
                    if 0 <= idx < len(data):
                        new_path = current_path + [f'[{idx}]']
                        if remaining_parts:
                            yield from self._search_recursive(data[idx], remaining_parts, new_path, data, idx)
                        else:
                            yield (self._build_path(new_path), data[idx], data, idx)
                elif condition['type'] == 'any_index':
                    for idx, item in enumerate(data):
                        new_path = current_path + [f'[{idx}]']
                        if remaining_parts:
                            yield from self._search_recursive(item, remaining_parts, new_path, data, idx)
                        else:
                            yield (self._build_path(new_path), item, data, idx)
        else:
            if part['is_wildcard'] or not part.get('name'):
                for idx, item in enumerate(data):
                    new_path = current_path + [f'[{idx}]']
                    if remaining_parts:
                        yield from self._search_recursive(item, remaining_parts, new_path, data, idx)
                    else:
                        yield (self._build_path(new_path), item, data, idx)
            else:
                for idx, item in enumerate(data):
                    new_path = current_path + [f'[{idx}]']
                    if remaining_parts:
                        yield from self._search_recursive(item, remaining_parts, new_path, data, idx)
                    else:
                        yield (self._build_path(new_path), item, data, idx)

    def _recursive_deep_search(
        self,
        data: Any,
        remaining_parts: List[dict],
        current_path: List[str],
        parent: Any,
        parent_key: Union[str, int],
    ) -> Generator[Tuple[str, Any, Any, Union[str, int]], None, None]:
        if remaining_parts:
            yield from self._search_recursive(data, remaining_parts, current_path, parent, parent_key)

        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [str(key)]
                yield from self._recursive_deep_search(value, remaining_parts, new_path, data, key)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = current_path + [f'[{idx}]']
                yield from self._recursive_deep_search(item, remaining_parts, new_path, data, idx)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# **********************************************************************************************************************
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

class n0dict_n0list_mixin():
    def __init__(self, *args, **kwargs):
        self.n0xpathparser = n0XPathParser()
        if args and isinstance(args[0], (str, Path)):
            data = load_file(args[0]).strip()
            super().__init__(data, **kwargs)
        else:
            super().__init__(*args, **kwargs)

    def __getitem__(self, xpath: str) -> Any:
        """Get value by XPath."""
        result = self.n0xpathparser.find_nodes(self, xpath, first_only=True)  # self.data
        if result is None:
            raise KeyError(f"XPath '{xpath}' not found")
        return result[1]  # Return value, not path

    def __setitem__(self, xpath: str, value: Any) -> None:
        """Set value by XPath."""
        result = self.n0xpathparser.find_nodes(self, xpath, first_only=True)  # self.data

        if result is None:
            # If node not found, try to create it
            self._create_path(xpath, value)
        else:
            # Update existing node
            __xpath, __old_value, parent, parent_key = result
            if parent is not None:
                if isinstance(parent, dict):
                    # parent[parent_key] = value
                    dict.__setitem__(parent, parent_key, value)
                elif isinstance(parent, list):
                    # parent[parent_key] = value
                    list.__setitem__(parent, parent_key, value)
            else:
                # Root element
                self  # self.data = value

    def get(self, xpath: str, default: Any = None) -> Any:
        """ Get value with default option. """
        try:
            return self[xpath]
        except KeyError:
            return default

    def find_all(self, xpath: str) -> List[Tuple[str, Any]]:
        """ Find all nodes by XPath. """
        result = self.n0xpathparser.find_nodes(self, xpath)  # self.data
        return result if result else []

    def remove(self, xpath: str) -> bool:
        """ Remove node by XPath. Returns True if removed, False if not found. """
        result = self.n0xpathparser.find_nodes(self, xpath, first_only=True)  # self.data

        if result is None:
            return False

        __xpath, __old_value, parent, parent_key = result

        if parent is not None:
            if isinstance(parent, dict):
                del parent[parent_key]
            elif isinstance(parent, list):
                parent.pop(parent_key)
            return True
        else:
            # Cannot remove root element
            return False

    def pop(self, xpath: str, default: Any = None) -> Any:
        """ Remove and return node value by XPath. """
        result = self.n0xpathparser.find_nodes(self, xpath, first_only=True)  # self.data

        if result is None:
            if default is not None:
                return default
            raise KeyError(f"XPath '{xpath}' not found")

        __xpath, __old_value, parent, parent_key = result

        if parent is not None:
            if isinstance(parent, dict):
                return parent.pop(parent_key, default)
            elif isinstance(parent, list):
                return parent.pop(parent_key) if 0 <= parent_key < len(parent) else default
        else:
            # Cannot pop root element
            if default is not None:
                return default
            raise KeyError(f"Cannot pop root element")

    def _create_path(self, xpath: str, value: Any) -> None:
        """ Create path if it doesn't exist. """
        # Enhanced path creation with support for different formats
        xpath = xpath.strip('/')

        # Parse the xpath to understand the structure
        parts = self.n0xpathparser._parse_xpath(xpath)

        current = self  # self.data
        path_so_far = []

        for i, part in enumerate(parts[:-1]):
            if part['type'] == 'index':
                # Handle index access
                for condition in part.get('conditions', []):
                    if condition['type'] == 'index':
                        idx = condition['value']
                        if isinstance(current, list):
                            while len(current) <= idx:
                                current.append(None)
                            if current[idx] is None:
                                current[idx] = {}
                            current = current[idx]
                            path_so_far.append(f'[{idx}]')
                        break
            else:
                # Handle named access
                name = part['name']
                if isinstance(current, dict):
                    if name not in current:
                        # Decide what to create based on next part
                        next_part = parts[i + 1] if i + 1 < len(parts) else None
                        if next_part and next_part['type'] == 'index':
                            current[name] = []
                        else:
                            current[name] = {}
                    current = current[name]
                    path_so_far.append(name)

        # Handle the final part
        final_part = parts[-1]
        if final_part['type'] == 'index':
            for condition in final_part.get('conditions', []):
                if condition['type'] == 'index':
                    idx = condition['value']
                    if isinstance(current, list):
                        while len(current) <= idx:
                            current.append(None)
                        current[idx] = value
                    break
        else:
            # Named final part
            name = final_part['name']
            if isinstance(current, dict):
                # current[name] = value
                dict.__setitem__(current, name, value)

########################################################################################################################

    # Alternative approach with more intuitive method names

    def append_to_path(self, xpath: str, value: Any) -> 'n0dict_n0list_mixin':
        """
        Append value to path, converting scalar to list if needed.
        Creates new list if path doesn't exist.

        Usage: nav.append_to_path('/a/b', value)
        """
        try:
            current_value = self[xpath]

            if isinstance(current_value, list):
                current_value.append(value)
            else:
                # Transform scalar to list with existing value + new value
                self[xpath] = [current_value, value]

        except KeyError:
            # Path doesn't exist, create new list with single element
            self[xpath] = [value]

        return self


    def to_list(self, xpath: str) -> 'n0dict_n0list_mixin':
        """
        Convert path value to list format.

        - If already list: leave as is
        - If scalar/dict/other: wrap in list
        - If doesn't exist: create empty list
        """
        try:
            current_value = self[xpath]

            if isinstance(current_value, list):
                # Already a list, leave as is
                pass
            else:
                # Transform to list (even if it's a dict or other type)
                self[xpath] = [current_value]

        except KeyError:
            # Path doesn't exist, create empty list
            self[xpath] = []

        return self


    def to_scalar(self, xpath: str) -> 'n0dict_n0list_mixin':
        """
        Convert path value to scalar format.

        - If single-element list: extract the element
        - If empty list: convert to None
        - If multi-element list: leave as is
        - If doesn't exist: create None
        - If already scalar: leave as is
        """
        try:
            current_value = self[xpath]

            if isinstance(current_value, list):
                if len(current_value) == 1:
                    # Transform single-element list to scalar
                    self[xpath] = current_value[0]
                elif len(current_value) == 0:
                    # Empty list becomes None
                    self[xpath] = None
                # If list has multiple elements, leave as is
            # If not a list, leave as is

        except KeyError:
            # Path doesn't exist, create with None
            self[xpath] = None

        return self


    def extend_path(self, xpath: str, values: list) -> 'n0dict_n0list_mixin':
        """
        Extend path with multiple values.
        Converts scalar to list if needed, creates new list if path doesn't exist.
        """
        try:
            current_value = self[xpath]

            if isinstance(current_value, list):
                current_value.extend(values)
            else:
                # Transform scalar to list with existing value + new values
                self[xpath] = [current_value] + list(values)

        except KeyError:
            # Path doesn't exist, create new list with values
            self[xpath] = list(values)

        return self


    def push(self, xpath: str, value: Any) -> 'n0dict_n0list_mixin':
        """ Alias for append_to_path for more familiar naming. """
        return self.append_to_path(xpath, value)


    def listify(self, xpath: str) -> 'n0dict_n0list_mixin':
        """ Alias for to_list for more familiar naming. """
        return self.to_list(xpath)


    def scalarify(self, xpath: str) -> 'n0dict_n0list_mixin':
        """ Alias for to_scalar for more familiar naming. """
        return self.to_scalar(xpath)


    # Chaining support methods
    def chain(self):
        """ Start a method chain. """
        return n0XPathChain(self)

########################################################################################################################

    def to_json(
        self,
        indent: Union[int, None] = None,
        indent_size: int = 4,
        pairs_in_one_line: bool = True,
        skip_empty_arrays: bool = False,
        compress: bool = False,
        sort_keys: bool = False,
        ensure_ascii: bool = False,
        allow_nan: bool = True,
        escape_special: bool = False,
        escape_unicode: bool = False,
    ) -> str:
        return data_to_json(
            self,
            indent,
            indent_size,
            pairs_in_one_line,
            skip_empty_arrays,
            compress,
            sort_keys,
            ensure_ascii,
            allow_nan,
            escape_special,
            escape_unicode,
        )

    def to_xml(
        self,
        indent: Union[int, None] = None,
        indent_size: int = 4,
        encoding: str = "utf-8",
        quote: str = '"',
    ) -> str:
        return data_to_xml(
            self,
            indent,
            indent_size,
            encoding,
            quote,
        )

    def to_xpath(
        self,
        indent: Union[int, None] = None,
    ) -> str:
        return data_to_xpath(
            self,
            indent,
        )

########################################################################################################################
########################################################################################################################
########################################################################################################################

class n1dict(n0dict_n0list_mixin, dict):
    pass

########################################################################################################################
########################################################################################################################
########################################################################################################################

class n1list(n0dict_n0list_mixin, list):
    pass

########################################################################################################################
########################################################################################################################
########################################################################################################################

class n0XPathChain:
    """ Helper class for method chaining. """
    def __init__(self, structure: Union[n1dict, n1list]):
        self.structure = structure

    def append(self, xpath: str, value: Any):
        """ Chain-friendly append. """
        self.structure.append_to_path(xpath, value)
        return self

    def to_list(self, xpath: str):
        """ Chain-friendly to_list. """
        self.structure.to_list(xpath)
        return self

    def to_scalar(self, xpath: str):
        """ Chain-friendly to_scalar. """
        self.structure.to_scalar(xpath)
        return self

    def set(self, xpath: str, value: Any):
        """ Chain-friendly set."""
        self.structure[xpath] = value
        return self

    def done(self):
        """ End chain and return structure. """
        return self.structure

########################################################################################################################
########################################################################################################################
########################################################################################################################

def xpath_search(
    data: Any,
    xpath: str,
    first_only: bool = False
) -> Union[List[Tuple[str, Any]], Optional[Tuple[str, Any]], None]:
    """ Search nodes in complex data structure by XPath. """
    return n0XPathParser().find_nodes(data, xpath, first_only)

################################################################################
__all__ = (
    'n1dict',
    'n1list',
    'xpath_search',
)
################################################################################
