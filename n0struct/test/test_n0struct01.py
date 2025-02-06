import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import (
    n0dict,
    n0list,
    n0print,
    n0debug,
    n0debug_calc,
    set__flag_compare_check_different_types,
    set__flag_compare_return_difference_of_values,
    init_logger,
    notemptyitems,
)
set__flag_compare_check_different_types(True)
set__flag_compare_return_difference_of_values(True)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False, debug_show_object_type = True)

# ******************************************************************************
# Etalon list in dictionary
# ******************************************************************************
dict1 = n0dict.convert_recursively({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 5},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})
# ******************************************************************************
# Sorted list in dictionary
# ******************************************************************************
dict2 = n0dict.convert_recursively({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},    # Single difference in value2
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})
# ******************************************************************************
# Unsorted list in dictionary
# ******************************************************************************
dict3 = n0dict.convert_recursively({
    "C": [
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},     # Changed order [2] -> [0]
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},    # Single difference in value2
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},     # Changed order [0] -> [2]
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},     # Duplicated with [2]
    ],
})
# ******************************************************************************
def test_sorted_lists():
    n0print("*"*80 + " 1 = Sorted list in dictionary = direct_compare")
    differences1_direct_compare = dict1.direct_compare(dict2, "dict1", "dict2")
    for key in differences1_direct_compare:
        n0print("*"*3 + " " + key)
        for itm in differences1_direct_compare[key]:
            n0print(itm)

    n0print("*"*80 + " 2 = Sorted list in dictionary = wise_compare")
    differences2_wise_compare = dict1.compare(dict2, "dict1", "dict2",
        composite_key = ("a", "b", "c"),
        compare_only = ("value1", "value2")
    )
    for key in differences2_wise_compare:
        n0print("*"*3 + " " + key)
        for itm in differences2_wise_compare[key]:
            n0print(itm)

    n0print("="*80)
    n0debug("differences1_direct_compare")
    n0debug_calc(notemptyitems(differences1_direct_compare["differences"]), 'notemptyitems(differences1_direct_compare["differences"])')
    assert notemptyitems(differences1_direct_compare["differences"])        == 1
    n0debug_calc(notemptyitems(differences1_direct_compare["not_equal"]), 'notemptyitems(differences1_direct_compare["not_equal"])')
    assert notemptyitems(differences1_direct_compare["not_equal"])          == 4
    assert notemptyitems(differences1_direct_compare["difftypes"])          == 0
    assert notemptyitems(differences1_direct_compare["other_unique"])       == 0
    assert notemptyitems(differences1_direct_compare["self_unique"])        == 0

    n0print("="*80)
    n0debug("differences2_wise_compare")
    assert differences1_direct_compare["differences"]  == differences2_wise_compare["differences"]
    assert differences1_direct_compare["not_equal"]    == differences2_wise_compare["not_equal"]
    assert differences1_direct_compare["difftypes"]    == differences2_wise_compare["difftypes"]
    assert differences1_direct_compare["other_unique"] == differences2_wise_compare["other_unique"]
    assert differences1_direct_compare["self_unique"]  == differences2_wise_compare["self_unique"]
# ******************************************************************************
def test_unsorted_lists():
    n0print("*"*80 + " 3 = Unsorted list in dictionary = direct_compare")
    differences1_direct_compare = dict1.direct_compare(dict3, "dict1", "dict3")
    for key in differences1_direct_compare:
        n0print("*"*3 + " " + key)
        for itm in differences1_direct_compare[key]:
            n0print(itm)

    n0print("*"*80 + " 4 = Unsorted list in dictionary = compare")
    differences2_wise_compare = dict1.compare(dict3, "dict1", "dict3",
        composite_key = ("a", "b", "c"),
        compare_only = ("value1", "value2")
    )
    for key in differences2_wise_compare:
        n0print("*"*3 + " " + key)
        for itm in differences2_wise_compare[key]:
            n0print(itm)

    n0print("="*80)
    n0debug("differences1_direct_compare")
    n0debug_calc(notemptyitems(differences1_direct_compare["differences"]), 'notemptyitems(differences1_direct_compare["differences"]')
    assert notemptyitems(differences1_direct_compare["differences"])        == 12
    n0debug_calc(notemptyitems(differences1_direct_compare["not_equal"]), 'differences1_direct_compare["not_equal"]')
    assert notemptyitems(differences1_direct_compare["not_equal"])          == 44
    assert notemptyitems(differences1_direct_compare["difftypes"])          == 0
    n0debug_calc(notemptyitems(differences1_direct_compare["other_unique"]), 'notemptyitems(differences1_direct_compare["other_unique"])')
    assert notemptyitems(differences1_direct_compare["other_unique"])       == 6
    n0debug_calc(notemptyitems(differences1_direct_compare["self_unique"]), 'notemptyitems(differences1_direct_compare["self_unique"])')
    assert notemptyitems(differences1_direct_compare["self_unique"])        == 0

    n0print("="*80)
    n0debug("differences2_wise_compare")
    n0debug_calc(notemptyitems(differences2_wise_compare["differences"]), 'notemptyitems(differences2_wise_compare["differences"]')
    assert notemptyitems(differences2_wise_compare["differences"])          == 2
    n0debug_calc(notemptyitems(differences2_wise_compare["not_equal"]), 'differences2_wise_compare["not_equal"]')
    assert notemptyitems(differences2_wise_compare["not_equal"])            == 4
    assert notemptyitems(differences2_wise_compare["difftypes"])            == 0
    n0debug_calc(notemptyitems(differences2_wise_compare["other_unique"]), 'notemptyitems(differences2_wise_compare["other_unique"])')
    assert notemptyitems(differences2_wise_compare["other_unique"])         == 6
    n0debug_calc(notemptyitems(differences2_wise_compare["self_unique"]), 'notemptyitems(differences2_wise_compare["self_unique"])')
    assert notemptyitems(differences2_wise_compare["self_unique"])          == 0
# ******************************************************************************
def main():
    n0print("="*80)
    n0debug_calc(dict1,"dict1")
    n0print("="*80)
    n0debug_calc(dict2,"dict2")
    n0print("="*80)
    n0debug_calc(dict2,"dict3")

    test_sorted_lists()
    test_unsorted_lists()

    n0debug_calc(dict1,'dict1')
    dict1["moreone/node[new()]/value"] = n0dict()
    n0debug_calc(dict1,'dict1')
    dict1["moreone/node[new()]/value"] = None
    n0debug_calc(dict1,'dict1')  # Defect: new() has not converted single n0dict node into node[]

    dict1["moreone/node[new()]/value"] = ""  # current and next lines generate 2 different new items
    n0debug_calc(dict1,'dict1')
    dict1["moreone/node[new()]/value"] = 1   # current and previous lines generate 2 different new items
    n0debug_calc(dict1,'dict1')
    dict1["moreone/node[last()]/value"] = 2
    dict1["moreone/node[last()]/code"] = "two"
    dict1["moreone/node[new()]/value"] = 3
    dict1["moreone/node[-1]/value"] = 4
    dict1["moreone/node[-1]/code"] = "four"

    assert isinstance(dict1["moreone/node[0]/value"],n0dict)                == True
    assert (dict1["moreone/node[1]/value"] is None)                         == True
    assert isinstance(dict1["moreone/node[2]/value"],str)                   == True
    assert (not dict1["moreone/node[2]/value"])                             == True
    assert dict1["moreone/node[3]/value"]                                   == 2
    assert dict1["moreone/node[4]/value"]                                   == 4

    n0print(dict1.to_json())
    n0print(dict1.to_xml())

    n0print(dict1["moreone/node"])

    assert len(dict1["moreone/node"])                                       == 5
    assert len(dict1["moreone/node[*]"])                                    == 5

    n0print(dict1["moreone"])
    assert len(dict1["moreone"]) == 1

    n0print(dict1["moreone/node/code[text()='four']/../value"])
    assert dict1["moreone/node/code[text()='four']/../value"][0]            == 4
    assert dict1["moreone/node/code[text()='four']/../value"]               == [4]


    n0print(dict1["moreone/node/code[text()='two']/../value"])
    assert dict1["moreone/node/code[text()='two']/../value"]                == [2]

    dict1["moreone/node/code[text()='two']/../value"] = 6
    n0print(dict1["moreone/node/code[text()='two']/../value"])
    assert dict1["moreone/node/code[text()='two']/../value"]                == [6]
    assert dict1["moreone/node/code[text()=two]/../value"]                  == [6]
    assert dict1['moreone/node/code[text()="two"]/../value']                == [6]

    n0print(dict1["moreone/node[code='two']/value"])
    assert dict1["moreone/node[code='two']/value"]                          == [6]

    dict1["moretwo/node/code"] = "seven"
    dict1["moretwo/node/value"] = 7
    n0print(dict1["moretwo/node/code[text()='seven']/../value"])
    assert dict1["moretwo/node/code[text()='seven']/../value"]              == 7

    n0print(dict1["moretwo/node[code='seven']/value"])
    assert dict1["moretwo/node[code='seven']/value"]                        == 7

    n0print(dict1.get("moretwo/node/code[text()='eight']/../value"))
    assert dict1.get("moretwo/node/code[text()='eight']/../value")          is None

    n0print(dict1["?moretwo/node/code[text()='eight']/../value"] or None)
    assert (dict1["?moretwo/node/code[text()='eight']/../value"] or None)   is None

    # set__debug_output(sys.stdout.write)

    str_json = """
    {
        "root": {
            "a": 1.0,
            "b": {
                "c": 2,
                "d": {
                    "e": {
                        "f": 3
                    },
                    "g": [
                        "4",
                        {"h": 5}
                    ],
                    "i": [
                        {"j": 6}
                    ]
                }
            },
            "k": [
                7,
                8
            ]
        }
    }
    """
    dict_from_json_default = n0dict(str_json)
    n0debug("dict_from_json_default")
    assert isinstance(dict_from_json_default, n0dict)                                   == True
    assert isinstance(dict_from_json_default["root"], dict)                             == True
    assert isinstance(dict_from_json_default["root/a"], float)                          == True # XML supports only str, for JSON float
    assert isinstance(dict_from_json_default["root/b"], dict)                           == True
    assert isinstance(dict_from_json_default["root/b/d"], dict)                         == True
    assert isinstance(dict_from_json_default["root/b/d/e"], dict)                       == True
    assert isinstance(dict_from_json_default["root/b/d/g"], list)                       == True # For recursively=False
    assert isinstance(dict_from_json_default["root/b/d/g[0]"], str)                     == True
    assert isinstance(dict_from_json_default["root/b/d/g[1]"], dict)                    == True
    assert isinstance(dict_from_json_default["root/b/d/g[1]/h"], int)                   == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_default["root/b/d/i"], list)                       == True # For JSON list
    assert isinstance(dict_from_json_default["root/b/d/i[0]"], dict)                    == True
    assert isinstance(dict_from_json_default["root/b/d/i[0]/j"], int)                   == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_default["root/k"], list)                           == True # For recursively=False
    assert isinstance(dict_from_json_default["root/k[0]"], int)                         == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_default["root/k[1]"], int)                         == True # XML supports only str, for JSON int
    dict_from_json_default.to_json(); dict_from_json_default.to_xml(); dict_from_json_default.to_xpath()

    dict_from_json_force_n0dict = n0dict(str_json, force_n0dict = True)
    n0debug("dict_from_json_force_n0dict")
    assert isinstance(dict_from_json_force_n0dict, n0dict)                              == True
    assert isinstance(dict_from_json_force_n0dict["root"], n0dict)                      == True
    assert isinstance(dict_from_json_force_n0dict["root/a"], float)                     == True # XML supports only str, for JSON float
    assert isinstance(dict_from_json_force_n0dict["root/b"], n0dict)                    == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d"], n0dict)                  == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d/e"], n0dict)                == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d/g"], list)                  == True # For recursively n0list
    assert isinstance(dict_from_json_force_n0dict["root/b/d/g[0]"], str)                == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d/g[1]"], n0dict)             == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d/g[1]/h"], int)              == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_force_n0dict["root/b/d/i"], list)                  == True # For JSON list, for JSON recursively n0list
    assert isinstance(dict_from_json_force_n0dict["root/b/d/i[0]"], n0dict)             == True
    assert isinstance(dict_from_json_force_n0dict["root/b/d/i[0]/j"], int)              == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_force_n0dict["root/k"], list)                      == True # For recursively n0list
    assert isinstance(dict_from_json_force_n0dict["root/k[0]"], int)                    == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_force_n0dict["root/k[1]"], int)                    == True # XML supports only str, for JSON int
    dict_from_json_force_n0dict.to_json(); dict_from_json_force_n0dict.to_xml(); dict_from_json_force_n0dict.to_xpath()

    dict_from_json_recursevely = n0dict.convert_recursively(n0dict(str_json))
    n0debug("dict_from_json_recursevely")
    assert isinstance(dict_from_json_recursevely, n0dict)                               == True
    assert isinstance(dict_from_json_recursevely["root"], n0dict)                       == True
    assert isinstance(dict_from_json_recursevely["root/a"], float)                      == True # XML supports only str, for JSON float
    assert isinstance(dict_from_json_recursevely["root/b"], n0dict)                     == True
    assert isinstance(dict_from_json_recursevely["root/b/d"], n0dict)                   == True
    assert isinstance(dict_from_json_recursevely["root/b/d/e"], n0dict)                 == True
    assert isinstance(dict_from_json_recursevely["root/b/d/g"], n0list)                 == True # For recursively=True
    assert isinstance(dict_from_json_recursevely["root/b/d/g[0]"], str)                 == True
    assert isinstance(dict_from_json_recursevely["root/b/d/g[1]"], n0dict)              == True
    assert isinstance(dict_from_json_recursevely["root/b/d/g[1]/h"], int)               == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely["root/b/d/i"], n0list)                 == True # For JSON list, for JSON recursively n0list
    assert isinstance(dict_from_json_recursevely["root/b/d/i[0]"], n0dict)              == True
    assert isinstance(dict_from_json_recursevely["root/b/d/i[0]/j"], int)               == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely["root/k"], n0list)                     == True # For recursively=True
    assert isinstance(dict_from_json_recursevely["root/k[0]"], int)                     == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely["root/k[1]"], int)                     == True # XML supports only str, for JSON int
    dict_from_json_recursevely.to_json(); dict_from_json_recursevely.to_xml(); dict_from_json_recursevely.to_xpath()

    dict_from_json_recursevely_force_n0dict = n0dict.convert_recursively(n0dict(str_json))
    n0debug("dict_from_json_recursevely_force_n0dict")
    assert isinstance(dict_from_json_recursevely_force_n0dict, n0dict)                  == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root"], n0dict)          == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/a"], float)         == True # XML supports only str, for JSON float
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b"], n0dict)        == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d"], n0dict)      == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/e"], n0dict)    == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/g"], n0list)    == True # For recursively=True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/g[0]"], str)    == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/g[1]"], n0dict) == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/g[1]/h"], int)  == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/i"], n0list)    == True # For JSON list, for JSON recursively n0list
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/i[0]"], n0dict) == True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/b/d/i[0]/j"], int)  == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/k"], n0list)        == True # For recursively=True
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/k[0]"], int)        == True # XML supports only str, for JSON int
    assert isinstance(dict_from_json_recursevely_force_n0dict["root/k[1]"], int)        == True # XML supports only str, for JSON int
    dict_from_json_recursevely_force_n0dict.to_json(); dict_from_json_recursevely_force_n0dict.to_xml(); dict_from_json_recursevely_force_n0dict.to_xpath()

    str_xml = """
    <root>
        <a>1</a>
        <b>
            <c>2</c>
            <d>
                <e>
                    <f>3</f>
                </e>
                <g>
                    4
                </g>
                <g>
                    <h>5</h>
                </g>
                <i>
                    <j>6</j>
                </i>
            </d>
        </b>
        <k>7</k>
        <k>8</k>
    </root>
    """
    dict_from_xml_default = n0dict(str_xml)
    n0debug("dict_from_xml_default")
    assert isinstance(dict_from_xml_default, n0dict)                                    == True
    assert isinstance(dict_from_xml_default["root"], n0dict)                            == True
    assert isinstance(dict_from_xml_default["root/a"], str)                             == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_default["root/b"], n0dict)                          == True
    assert isinstance(dict_from_xml_default["root/b/d"], n0dict)                        == True
    assert isinstance(dict_from_xml_default["root/b/d/e"], n0dict)                      == True
    assert isinstance(dict_from_xml_default["root/b/d/g"], list)                        == True # For recursively=False
    assert isinstance(dict_from_xml_default["root/b/d/g[0]"], str)                      == True
    assert isinstance(dict_from_xml_default["root/b/d/g[1]"], n0dict)                   == True
    assert isinstance(dict_from_xml_default["root/b/d/g[1]/h"], str)                    == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_default["root/b/d/i"], n0dict)                      == True # For JSON list, for JSON recursively n0list
    assert isinstance(dict_from_xml_default["root/b/d/i[0]"], n0dict)                   == True
    assert isinstance(dict_from_xml_default["root/b/d/i[0]/j"], str)                    == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_default["root/k"], list)                            == True # For recursively=False
    assert isinstance(dict_from_xml_default["root/k[0]"], str)                          == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_default["root/k[1]"], str)                          == True # XML supports only str, for JSON int
    dict_from_xml_default.to_json(); dict_from_xml_default.to_xml(); dict_from_xml_default.to_xpath()

    # force_n0dict = True for XML is useless, in any cases dictionaries will be n0dict
    dict_from_xml_force_n0dict = n0dict(str_xml, force_n0dict = True)
    n0debug("dict_from_xml_force_n0dict")
    assert isinstance(dict_from_xml_force_n0dict, n0dict)                               == True
    assert isinstance(dict_from_xml_force_n0dict["root"], n0dict)                       == True
    assert isinstance(dict_from_xml_force_n0dict["root/a"], str)                        == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_force_n0dict["root/b"], n0dict)                     == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d"], n0dict)                   == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/e"], n0dict)                 == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/g"], list)                   == True # For recursively=False
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/g[0]"], str)                 == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/g[1]"], n0dict)              == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/g[1]/h"], str)               == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/i"], n0dict)                 == True # For JSON list
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/i[0]"], n0dict)              == True
    assert isinstance(dict_from_xml_force_n0dict["root/b/d/i[0]/j"], str)               == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_force_n0dict["root/k"], list)                       == True # For recursively=False
    assert isinstance(dict_from_xml_force_n0dict["root/k[0]"], str)                     == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_force_n0dict["root/k[1]"], str)                     == True # XML supports only str, for JSON int
    dict_from_xml_force_n0dict.to_json(); dict_from_xml_force_n0dict.to_xml(); dict_from_xml_force_n0dict.to_xpath()

    dict_from_xml_recursevely = n0dict.convert_recursively(n0dict(str_xml))
    n0debug("dict_from_xml_recursevely")
    assert isinstance(dict_from_xml_recursevely, n0dict)                                == True
    assert isinstance(dict_from_xml_recursevely["root"], n0dict)                        == True
    assert isinstance(dict_from_xml_recursevely["root/a"], str)                         == True # XML supports only str
    assert isinstance(dict_from_xml_recursevely["root/b"], n0dict)                      == True
    assert isinstance(dict_from_xml_recursevely["root/b/d"], n0dict)                    == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/e"], n0dict)                  == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/g"], n0list)                  == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/g[0]"], str)                  == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/g[1]"], n0dict)               == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/g[1]/h"], str)                == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely["root/b/d/i"], n0dict)                  == True # For JSON list
    assert isinstance(dict_from_xml_recursevely["root/b/d/i[0]"], n0dict)               == True
    assert isinstance(dict_from_xml_recursevely["root/b/d/i[0]/j"], str)                == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely["root/k"], n0list)                      == True
    assert isinstance(dict_from_xml_recursevely["root/k[0]"], str)                      == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely["root/k[1]"], str)                      == True # XML supports only str, for JSON int
    dict_from_xml_recursevely.to_json(); dict_from_xml_recursevely.to_xml(); dict_from_xml_recursevely.to_xpath()

    dict_from_xml_recursevely_force_n0dict = n0dict.convert_recursively(n0dict(str_xml))
    n0debug("dict_from_xml_recursevely_force_n0dict")
    assert isinstance(dict_from_xml_recursevely_force_n0dict, n0dict)                   == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root"], n0dict)           == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/a"], str)            == True # XML supports only str
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b"], n0dict)         == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d"], n0dict)       == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/e"], n0dict)     == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/g"], n0list)     == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/g[0]"], str)     == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/g[1]"], n0dict)  == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/g[1]/h"], str)   == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/i"], n0dict)     == True # For JSON list
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/i[0]"], n0dict)  == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/b/d/i[0]/j"], str)   == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/k"], n0list)         == True
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/k[0]"], str)         == True # XML supports only str, for JSON int
    assert isinstance(dict_from_xml_recursevely_force_n0dict["root/k[1]"], str)         == True # XML supports only str, for JSON int
    dict_from_xml_recursevely_force_n0dict.to_json(); dict_from_xml_recursevely_force_n0dict.to_xml(); dict_from_xml_recursevely_force_n0dict.to_xpath()

    str_xml_empty = "<root/>"
    dict_from_xml_empty = n0dict(str_xml_empty)
    n0debug("dict_from_xml_empty")
    assert isinstance(dict_from_xml_empty, n0dict) == True
    assert (dict_from_xml_empty["root"] is None) == True
    dict_from_xml_empty.to_json(); dict_from_xml_empty.to_xml(); dict_from_xml_empty.to_xpath()

    dict4 = n0dict.convert_recursively(
        {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": 3
                }
            }
        }
    )
    n0debug("dict4")
    assert isinstance(dict4, n0dict)                                                    == True
    assert dict4["a"]                                                                   == 1
    assert dict4["b/c"]                                                                 == 2
    assert dict4["b/d/e"]                                                               == 3
    assert dict4.get("b/d/e", "ALREADY_DELETED")                                        == 3
    assert dict4.pop("b/d/e")                                                           == 3
    assert dict4.get("b/d/e", "ALREADY_DELETED")                                        == "ALREADY_DELETED"
    assert dict4.delete("b/c")["a"]                                                     == 1
    assert dict4.get("b/c", "ALREADY_DELETED")                                          == "ALREADY_DELETED"
    assert dict4.delete("b/d", recursively=True)
    assert dict4.get("b", "ALREADY_DELETED")                                            == "ALREADY_DELETED"
    n0debug("dict4")

    dict5 = n0dict(
        {
            "a": {
                "b": {
                    "c": {
                        "d": 4
                    }
                }
            }
        }
    )
    n0debug("dict5")
    dict5.delete("a/b/c/d", recursively=True)
    n0debug("dict5")

    # ##########################################################################
    # n0struct_findall.py
    # ##########################################################################
    dict6 = n0dict({
        "Root": {
            "Node1": {
                "Subnode1_1": [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode1_1"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode1_1"},
                ],
                "Subnode1_2": [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode1_2"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode1_2"},
                ],
            },
            "Node2": {
                "Subnode2_1": [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode2_1"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode2_1"},
                ],
                "Subnode2_2": [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode2_2"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode2_2"},
                ],
            },
        }
    })
    n0debug("dict6")
    n0debug_calc(dict6.findall("//Root/Node1"))
    n0debug_calc(dict6.findall("//Root/Node2/Subnode2_1/tag[text()==PARAM1]/../value"))
    assert list(dict6.findall("//Root/Node2/Subnode2_1/tag[text()==PARAM1]/../value").keys())[0]    == "//Root/Node2/Subnode2_1[0]/value"
    assert list(dict6.findall("//Root/Node2/Subnode2_1/tag[text()==PARAM1]/../value").values())[0]  == "VALUE1 from subnode2_1"

    dict7 = n0dict({
        "Root": {
            "Nodes": [
                [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode0_0"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode0_1"},
                ],
                [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode1_0"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode1_1"},
                ],
                [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode2_0"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode2_1"},
                ],
                [
                    {"tag": "PARAM1", "value": "VALUE1 from subnode3_0"},
                    {"tag": "PARAM2", "value": "VALUE2 from subnode3_1"},
                ],
            ],
        }
    })
    n0print("\n" + list(dict7.findall("//").values())[0].to_xpath())
    found = dict7.findall("//Root/Nodes/tag[text()==PARAM1]/../value")
    n0debug_calc(found, '"//Root/Nodes/tag[text()==PARAM1]/../value"')
    assert len(found)                                                                               == 4
    assert list(found.values())[2]                                                                  == "VALUE1 from subnode2_0"

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_sorted_lists',
    'test_unsorted_lists',
    'main',
)
################################################################################
