import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

import pytest
from xml.etree.ElementTree import ParseError
from n0struct_xml import n0xml
from n0struct import (
    n0print,
    n0debug,
    n0debug_calc,
    init_logger,
)

_simple_xml = """
    <root>
        <item>
            <name>Item 1</name>
        </item>
        <item>
            <name>Item 2</name>
        </item>
        <group>
            <item>
                <name>Item 3</name>
            </item>
        </group>
    </root>
    """
# @pytest.fixture
# def simple_xml():
    # return _simple_xml
_complex_xml = """
    <catalog>
        <book id="1">
            <title>Python 101</title>
            <author>John Doe</author>
        </book>
        <book id="2">
            <title>Advanced Python</title>
            <author>Jane Doe</author>
        </book>
        <magazine>
            <issue>
                <title>Monthly Tech</title>
            </issue>
        </magazine>
    </catalog>
    """
# @pytest.fixture
# def complex_xml():
    # return _complex_xml

# Tests for parsing
def test_01_parse_basic_structure():
    parsed = n0xml(_simple_xml)
    # n0debug("parsed")
    assert len(parsed) == 3
    # n0debug_calc(parsed[0])
    assert parsed[0][0] == 'item'
    # n0debug_calc(parsed[2])
    assert parsed[2][0] == 'group'

def test_02_parse_nested_structure():
    parsed = n0xml(_simple_xml)
    # n0debug("parsed")
    group = parsed[2][1]['value'][0]
    # n0debug("group")
    assert group[0] == 'item'
    assert group[1]['value'][0][1]['value'] == 'Item 3'

def test_03_parse_with_attributes():
    parsed = n0xml(_complex_xml)
    assert parsed[0][1]['attrib']['id'] == '1'
    assert parsed[1][1]['attrib']['id'] == '2'

def test_04_parse_invalid_xml():
    invalid_xml = "<root><item></root>"
    with pytest.raises(ParseError):
        n0xml(invalid_xml)

# Tests for find method
def test_05_find_single_element():
    parsed = n0xml(_simple_xml)
    result = parsed.get('item[0]/name')
    assert result == 'Item 1'

def test_06_find_element_by_index():
    parsed = n0xml(_simple_xml)
    result = parsed.get('item[1]/name')
    assert result == 'Item 2'

def test_07_find_nested_element():
    parsed = n0xml(_simple_xml)
    result = parsed.get('group/item[0]/name')
    assert result == 'Item 3'

def test_08_find_nonexistent_element():
    parsed = n0xml(_simple_xml)
    result = parsed.get('nonexistent', default='Not Found')
    assert result == 'Not Found'

def test_09_find_empty_path():
    parsed = n0xml(_simple_xml)
    # n0debug("parsed")
    result = parsed.get('')
    # n0debug("result")
    assert result == list(parsed)


def test_10_find_no_index_defaults_to_first():
    parsed = n0xml(_simple_xml)
    result = parsed.get('item/name')
    assert result == 'Item 1'

# Edge cases
def test_11_find_with_invalid_xpath_format():
    parsed = n0xml(_simple_xml)
    with pytest.raises(ValueError):
        parsed.get('item[invalid]/name')

def test_12_find_on_empty_data():
    result = n0xml._get([], 'item/name', default='Not Found')
    assert result == 'Not Found'

def test_13_find_with_multiple_levels():
    parsed = n0xml(_complex_xml)
    result = parsed.get('magazine/issue/title')
    assert result == 'Monthly Tech'

def test_14_find_with_attributes():
    parsed = n0xml(_complex_xml)
    book = parsed.get('book[1]/title')
    assert book == 'Advanced Python'

# Tests for invalid input
def test_15_find_with_non_string_xpath():
    parsed = n0xml(_simple_xml)
    with pytest.raises(TypeError):
        parsed.get(123)

def test_16_parse_empty_string():
    with pytest.raises(ParseError):
        n0xml('')

def test_17_find_with_partial_path():
    parsed = n0xml(_simple_xml)
    result = parsed.get('item')
    assert isinstance(result, list)
    assert len(result) == 1
    assert len(result[0]) == 2
    # n0debug_calc(result[0])
    assert result[0][0] == "name"
    assert result[0][1]['value'] == "Item 1"

def test_18_find_return_all_items():
    parsed = n0xml(_simple_xml)
    # n0debug("parsed")
    # results = parsed.findall('item[0][text()=="HELLO"]')
    # n0debug("results")

    try:
        results = parsed.findall('/item/./../')
    except ValueError:
        pass
    else:
        raise AssertionError("Expected exception for incorrect xpath")

    xpath = 'item[*]/name[text()="Item 2"]'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 1
    assert results[0][1] == "Item 2"
    result = parsed.get('/'.join(results[0][0]))
    n0debug_calc(result, xpath + "[0]")
    assert result == results[0][1]

    xpath = 'item[*]/name[text()="Item 2"]/..'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 1
    assert results[0][1][0][1]['value'] == "Item 2"
    result = parsed.get('/'.join(results[0][0]))
    n0debug_calc(result, xpath + "[0]")
    assert result == results[0][1]

    xpath = 'item[*]'
    results = parsed.findall(xpath, find_first=True)
    n0debug_calc(results, "find_first=" + xpath)
    assert len(results) == 1
    result = parsed.get('/'.join(results[0][0] + ['name']))
    n0debug_calc(result, xpath + "[0]")
    assert result == results[0][1][0][1]['value']

    xpath = 'item[*]'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 2
    result = parsed.get('/'.join(results[0][0] + ['name']))
    n0debug_calc(result, xpath + "[0]")
    assert result == results[0][1][0][1]['value']
    result = parsed.get('/'.join(results[1][0] + ['name']))
    n0debug_calc(result, xpath + "[1]")
    assert result == results[1][1][0][1]['value']

    xpath = 'item'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 2
    xpath2 = '/'.join(results[0][0] + ['name'])
    result = parsed.get(xpath2)
    n0debug_calc(result, xpath2 + "[0]")
    assert result == results[0][1][0][1]['value']
    xpath2 = '/'.join(results[1][0] + ['name'])
    result = parsed.get(xpath2)
    n0debug_calc(result, xpath2 + "[1]")
    assert result == results[1][1][0][1]['value']

    xpath = 'item[0]'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 1
    result = parsed.get('/'.join(results[0][0]))
    n0debug_calc(result, xpath)
    assert result == results[0][1]

    xpath = 'item[1]'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 1
    result = parsed.get('/'.join(results[0][0]))
    n0debug_calc(result, xpath)
    assert result == results[0][1]

    xpath = 'item[2]'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 0

    xpath = '**'
    results = parsed.findall(xpath)
    n0debug_calc(results, xpath)
    assert len(results) == 3
    n0debug_calc(results[0][1], '/'.join(results[0][0]) + "[0]")
    assert results[0][1] == "Item 1"
    n0debug_calc(results[1][1], '/'.join(results[1][0]) + "[1]")
    assert results[1][1] == "Item 2"
    n0debug_calc(results[2][1], '/'.join(results[2][0]) + "[2]")
    assert results[2][1] == "Item 3"
    xpath = '/'.join(results[0][0])
    result = parsed.get(xpath)
    n0debug_calc(result, xpath)
    n0debug_calc(results[0][1], "results[0][1]")
    assert result == results[0][1]
    xpath = '/'.join(results[1][0])
    result = parsed.get(xpath)
    n0debug_calc(result, xpath)
    n0debug_calc(results[1][1], "results[1][1]")
    assert result == results[1][1]
    xpath = '/'.join(results[2][0])
    result = parsed.get(xpath)
    n0debug_calc(result, xpath)
    n0debug_calc(results[2][1], "results[2][1]")
    assert result == results[2][1]

def test_19_parse_with_mixed_content():
    mixed_content = """
    <root>
        <data>Some text</data>
        <data><child>Child text</child></data>
    </root>
    """
    parsed = n0xml(mixed_content)
    # n0debug("parsed")
    assert len(parsed) == 2
    # n0debug_calc(parsed[0])
    assert parsed[0][0] == "data"
    assert parsed[0][1]['value'] == "Some text"

def test_20_find_with_multiple_conditions():
    parsed = n0xml(_complex_xml)
    result = parsed.get('book[1]/author')
    assert result == 'Jane Doe'

def test_21_findall():
    xml_data = """
    <root>
        <item>
            <name>Item 1</name>
        </item>
        <item>
            <name>Item 2</name>
        </item>
        <group>
            <item>
                <name>Item 3</name>
            </item>
        </group>
    </root>
    """
    # Parse the XML
    parsed_data = n0xml(xml_data)

    # Find elements using custom XPath
    xpath = 'item[0]/name'
    result = parsed_data.get(xpath)  # First <item> name
    n0debug_calc(result, xpath)
    assert result == "Item 1"

    xpath = 'group/item[0]/name'
    result = parsed_data.get(xpath)  # Name in <group>
    n0debug_calc(result, xpath)
    assert result == "Item 3"

    xpath = 'nonexistent'
    result = parsed_data.get(xpath, default="Not Found")  # Nonexistent element
    n0debug_calc(result, xpath)
    assert result == "Not Found"

    result = parsed_data.get('nonexistent')  # Nonexistent element
    n0debug_calc(result, xpath)
    assert result is None


    xml_data = """
    <root>
        <ARRAY>
            <ELEM>
                <KEY>MYNODE</KEY>
                <VALUE>1</VALUE>
            </ELEM>
            <ELEM>
                <KEY>OTHERNODE</KEY>
                <VALUE>2</VALUE>
            </ELEM>
            <ELEM>
                <KEY>MYNODE</KEY>
                <VALUE>3</VALUE>
            </ELEM>
        </ARRAY>
    </root>
    """
    '''
    parsed_data = [
        ("ARRAY", [
            ("ELEM", {"KEY": "MYNODE", "VALUE": 1}),
            ("ELEM", {"KEY": "OTHERNODE", "VALUE": 2}),
            ("ELEM", {"KEY": "MYNODE", "VALUE": 3})
        ])
    ]
    '''
    parsed_data = n0xml(xml_data)
    # n0debug("parsed_data")

    xpath = 'ARRAY/ELEM[*]/KEY[text()=MYNODE]/../VALUE'
    result = parsed_data.findall(xpath)
    n0debug_calc(result, xpath)
    assert result == [(['ARRAY','ELEM[0]','VALUE'], "1"), (['ARRAY','ELEM[2]','VALUE'], "3")]

    xpath = 'ARRAY/ELEM[*]/KEY[text()=MYNODE]/../VALUE'
    result = parsed_data.findall(xpath, find_first=True)
    n0debug_calc(result, xpath)
    assert result == [(['ARRAY','ELEM[0]','VALUE'], "1")]

    xpath = 'ARRAY/ELEM[1]/KEY[text()=MYNODE]/../VALUE'
    result = parsed_data.findall(xpath)
    n0debug_calc(result, xpath)
    assert result == []

    xpath = '*/ELEM[*]/KEY[text()=MYNODE]/../VALUE'
    result = parsed_data.findall(xpath)
    n0debug_calc(result, xpath)
    assert result == [(['ARRAY','ELEM[0]','VALUE'], "1"), (['ARRAY','ELEM[2]','VALUE'], "3")]

    xpath = '**/KEY[text()=MYNODE]/../VALUE'
    result = parsed_data.findall(xpath)
    # n0print(xpath)
    n0debug_calc(result, xpath)
    n0debug_calc(n0xml.to_dict(result), f"to_dict:{xpath}")
    n0debug_calc(n0xml.to_tuple(result), f"to_list_of_dict:{xpath}")
    assert result == [(['ARRAY','ELEM','VALUE'], "1"), (['ARRAY','ELEM[2]','VALUE'], "3")]

    xpath = '**'
    result = parsed_data.findall(xpath)
    # n0print(xpath)
    n0debug_calc(result, xpath)
    assert result == [
        (["ARRAY", "ELEM",    "KEY"],   "MYNODE"),
        (["ARRAY", "ELEM",    "VALUE"], "1"),
        (["ARRAY", "ELEM[1]", "KEY"],   "OTHERNODE"),
        (["ARRAY", "ELEM[1]", "VALUE"], "2"),
        (["ARRAY", "ELEM[2]", "KEY"],   "MYNODE"),
        (["ARRAY", "ELEM[2]", "VALUE"], "3")
    ]



def test_n0xml():
    test_01_parse_basic_structure()
    test_02_parse_nested_structure()
    test_03_parse_with_attributes()
    test_04_parse_invalid_xml()
    test_05_find_single_element()
    test_06_find_element_by_index()
    test_07_find_nested_element()
    test_08_find_nonexistent_element()
    test_09_find_empty_path()
    test_10_find_no_index_defaults_to_first()
    test_11_find_with_invalid_xpath_format()
    test_12_find_on_empty_data()
    test_13_find_with_multiple_levels()
    test_14_find_with_attributes()
    test_15_find_with_non_string_xpath()
    test_16_parse_empty_string()
    test_17_find_with_partial_path()
    test_18_find_return_all_items()
    test_19_parse_with_mixed_content()
    test_20_find_with_multiple_conditions()
    test_21_findall()


# ******************************************************************************
def main():
    test_n0xml()
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_n0xml',
    'main',
)
################################################################################
