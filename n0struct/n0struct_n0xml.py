from collections import defaultdict
import typing
import xml.etree.ElementTree as ET
import re

class n0xml:
    """
    A parser to process XML into an ordered list of tuples,
    search elements by custom XPath-like expressions, and handle multi-level wildcards.
    """

    def __init__(self, xml_text: str):
        """
        Parse an XML string into an ordered list of tuples.

        :param xml_text: The XML string to parse.
        """
        self.ordered_items = self._parse_node(ET.fromstring(xml_text))

    def _parse_node(self, element: ET.Element) -> list:
        """
        Recursively parse an XML element into a list of tuples preserving order.

        :param element: The XML element to parse.
        :return: A list of tuples where each tuple contains the tag name and its data.
        """
        result = []
        for child in element:
            if len(child):
                element_data = {
                    'value': self._parse_node(child),
                    'attrib': {k: v for k, v in child.attrib.items()}
                }
            else:
                element_data = {
                    'value': child.text,
                    'attrib': {k: v for k, v in child.attrib.items()}
                }
            result.append((child.tag, element_data))
        return result

    def get(
        self,
        xpath: typing.Union[str, list],
        default=None,
    ) -> typing.Union[list, typing.Any]:
        """
        Find an element's value/subnodes in the ordered list based on an XPath-like expression.

        :param xpath: The XPath-like string or list specifying the search path.
        :param default: Value to return if the element is not found.
        :return: The found element or the default value if not found.
        """
        return self._get(self.ordered_items, xpath, default)

    def get_attrib(
        self,
        xpath: typing.Union[str, list],
        default=None,
    ) -> typing.Union[list, typing.Any]:
        """
        Find an element's attributes in the ordered list based on an XPath-like expression.

        :param xpath: The XPath-like string or list specifying the search path.
        :param default: Value to return if the element is not found.
        :return: The found element attributes or the default value if not found.
        """
        return self._get(self.ordered_items, xpath, default, what_to_return='attrib')

    @staticmethod
    def _get(
        ordered_items: list,
        xpath: typing.Union[str, list],
        default=None,
        what_to_return: str = 'value',
    ) -> typing.Union[list, typing.Any]:
        """
        Find an element in the ordered list based on an XPath-like expression.

        :param ordered_items: The ordered list of tuples to search.
        :param xpath: The XPath-like string or list specifying the search path.
        :param default: Value to return if the element is not found.
        :return: The found element or the default value if not found.
        """
        if not isinstance(xpath, (str, list)):
            raise TypeError(f"'{xpath}' must be str or list")
        if not xpath:
            # n0debug("ordered_items")
            # n0debug("what_to_return")
            if isinstance(ordered_items, dict):
                return ordered_items[what_to_return]
                return ordered_items # in case of requested root: '' or '/' or '//'
            elif what_to_return == 'value':
                return ordered_items # in case of requested root: '' or '/' or '//'
            else:
                raise RuntimeError(f"Impossible to get {what_to_return} of {xpath}")
        if isinstance(xpath, str):
            xpath = xpath.replace("/[", '[').strip('/').split('/')

        node_index = 0
        node_name = xpath[0]

        # Handle indexing like "tag[index]"
        if '[' in node_name:
            node_name, index = node_name.rstrip(']').split('[', 1)
            node_index = int(index)

        if isinstance(ordered_items, dict):
            ordered_items = ordered_items['value']
        for item in ordered_items:
            if item[0] == node_name:
                if node_index == 0:
                    return n0xml._get(item[1], xpath[1:], default, what_to_return)
                else:
                    node_index -= 1

        return default


    def __len__(self) -> int:
        return len(self.ordered_items)

    '''
    def __repr__(self) -> str:
        return repr(self.ordered_items)
    '''
    def __repr__(self) -> list:
        return self.ordered_items

    def __str__(self) -> str:
        # return str(self.ordered_items)
        return n0pretty(self.ordered_items)

    def __getitem__(self, index: typing.Union[int, str]) -> typing.Any:
        if isinstance(index, int):
            return self.ordered_items[index]
        else:
            result = self.get(index, "@n0tF0uNd$")
            if result == "@n0tF0uNd$":
                raise KeyError(index)
            return result


    def findall(
        self,
        xpath: typing.Union[str, list],
        root_xpath: typing.Union[str, list] = [],
        find_first: bool = False
    ) -> list:
        """
        Find elements based on an XPath-like expression, supporting multi-level wildcards.

        :param xpath: The XPath-like string or list specifying the search path.
        :param root_xpath: The root path for the search.
        :param find_first: Whether to stop at the first match.
        :return: A list of found elements or the first match if find_first is True.
        """
        def recurse(
            ordered_items: list,
            sought_xpath_parts: list,
            passed_xpath_parts: list,
            any_xpath: int = 0,
        ):
            nonlocal first_found

            found = []
            while sought_xpath_parts or any_xpath == 2:
                current_xpath_part = "**" if any_xpath == 2 else sought_xpath_parts[0]

                if current_xpath_part == '..':
                    return None

                match = re.match(
                    r"([a-zA-Z0-9_]+|\*\*|\*)(?:\[(\d+|\*)\])?(?:\[(text)(\(\))?(==|!=|<>|=)['\"]?([^'\"]+)['\"]?\])?",
                    current_xpath_part
                )
                if not match:
                    raise ValueError(f"Incorrect xpath '{current_xpath_part}' in {'/'.join(passed_xpath_parts + sought_xpath_parts)}")

                required_tag = match.group(1)
                if required_tag != "**":
                    any_xpath = 0 # items/a/A/subitem: no "**", so check the tag of element
                else:
                    if any(_xpath_part != "**" for _xpath_part in sought_xpath_parts[1:]):
                        any_xpath = 1 # items/**/subitem: specific tag is in the xpath:
                    else:
                        any_xpath = 2 # items/**: no any more specific tags in the xpath, so return the deepest elements in the tree:
                                      # items/a/A/subitem, items/a/B/subitem...

                required_index = match.group(2)
                if required_index not in (None,'*'):
                    required_index = int(required_index)
                condition_function = match.group(3)
                condition_comparison = match.group(5)
                condition_value = match.group(6)
                if condition_function == "text":
                    if condition_comparison:
                        if condition_comparison in {"==", "="}:
                            if condition_value.lower() in {"none","null","nul"}:
                                condition_validation = lambda x: x is None
                            else:
                                condition_validation = lambda x: x == f"{condition_value}"
                        elif condition_comparison in {"!=", "<>"}:
                            if condition_value.lower() in {"none","null","nul"}:
                                condition_validation = lambda x: x is not None
                            else:
                                condition_validation = lambda x: x != f"{condition_value}"
                        else:
                            raise ValueError(f"Unknown condition '{condition_function}{condition_comparison}{condition_value}' in {'/'.join(passed_xpath_parts + sought_xpath_parts)}")
                elif condition_function is None:
                    condition_validation = lambda x: True
                else:
                    raise ValueError(f"Unknown function '{condition_function}' in {'/'.join(passed_xpath_parts + [current_xpath_part])}")

                if isinstance(ordered_items, list) \
                   and len(ordered_items) > 0 \
                   and isinstance(ordered_items[0], tuple) \
                   and isinstance(ordered_items[0][1], dict):
                    indexes = defaultdict(int)
                    for _cur_level_tag, _cur_level_dict in ordered_items:
                        if _cur_level_tag == required_tag or required_tag in {"*", "**"} or any_xpath:
                            if required_index in {None, '*'} or indexes[_cur_level_tag] == required_index:
                                if condition_validation(_cur_level_dict['value']):
                                    _found = recurse(
                                        _cur_level_dict['value'],
                                        sought_xpath_parts[1:],
                                        passed_xpath_parts + [
                                            _cur_level_tag +
                                            (
                                                f"[{indexes[_cur_level_tag]}]"
                                                if required_index or indexes[_cur_level_tag]
                                                else ""
                                            )
                                        ],
                                        any_xpath
                                    )
                                    if _found is None: # .. was found
                                        sought_xpath_parts = sought_xpath_parts[2:]
                                        break # go to while
                                    found.extend(_found)
                                    if first_found:
                                        return found
                            if any_xpath == 1:
                                # More one dive without any conditions
                                _found = recurse(
                                    _cur_level_dict['value'],
                                    sought_xpath_parts, # .../**/...
                                    passed_xpath_parts + [
                                        _cur_level_tag +
                                        (
                                            f"[{indexes[_cur_level_tag]}]"
                                            if required_index or indexes[_cur_level_tag]
                                            else ""
                                        )
                                    ],
                                    any_xpath
                                )
                                if _found is None: # .. was found
                                    sought_xpath_parts = sought_xpath_parts[2:]
                                    break # go to while
                                found.extend(_found)
                                if first_found:
                                    return found
                            indexes[_cur_level_tag] += 1
                    else:
                        return found
                else:
                    # n0debug("found")
                    if any_xpath == 2:
                        # n0debug("ordered_items")
                        # found.extend([(passed_xpath_parts + [ordered_items[0][0]], ordered_items[0][1]['value'])])
                        found.extend([(passed_xpath_parts, ordered_items)])
                    return found

            if not sought_xpath_parts:
                if find_first and not first_found:
                    first_found = passed_xpath_parts
                return [(passed_xpath_parts, ordered_items)]

            raise RuntimeError("Unexpected exit during xpath traversal")

        if isinstance(xpath, str):
            while True:
                normalized_xpath = xpath.replace("**/**", "**")
                if normalized_xpath == xpath:
                    break
                xpath = normalized_xpath
            xpath = xpath.replace("/[", '[').strip('/').split('/')
        if isinstance(root_xpath, str):
            root_xpath = root_xpath.replace("/[", '[').strip('/').split('/')

        first_found = None

        # return n0xml.to_dict(recurse(self.ordered_items, xpath, root_xpath))
        return recurse(self.ordered_items, xpath, root_xpath)

    def findfirst(
        self,
        xpath: typing.Union[str, list],
        root_xpath: typing.Union[str, list] = [],
    ) -> tuple:
        found = self.findall(xpath, root_xpath, find_first=True)
        if found:
            return found[0]  # tuple(list, dict('value':, attrib':???)/str)
        else:
            return tuple()

    def __contains__(
        self,
        xpath: typing.Union[str, list],
    ) -> typing.Union[str, None]:
        found = self.findall(xpath, [], find_first=True)
        if found:
            return f"/{'/'.join(found[0])}"
        else:
            return None

    @staticmethod
    def to_dict(from_list_of_tuples: list):
        return {
            '/'.join(_tuple): _value
            for _tuple,_value in  from_list_of_tuples
        }

    @staticmethod
    def to_tuple(from_list_of_tuples: list):
        return [
            ('/'.join(_tuple), _value)
            for _tuple,_value in  from_list_of_tuples
        ]


################################################################################
__all__ = (
    'n0xml',
)
################################################################################
