import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
# import n0struct
# n0struct._DIFFTYPES = True  # For updating global variables using prefix is mandatory
# n0struct._DIFFVALUES = True
from n0struct import * # For using n0dict(), n0print(), n0debug without prefixes
set__flag_compare_check_different_types(True)
set__flag_compare_return_difference_of_values(True)

# ******************************************************************************
# Etalon list in dictionary
# ******************************************************************************
dict1 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 5},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
}, recursively=True)
# ******************************************************************************
# Sorted list in dictionary
# ******************************************************************************
dict2 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},    # Single difference in value2
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
}, recursively=True)
# ******************************************************************************
# Unsorted list in dictionary
# ******************************************************************************
dict3 = n0dict({
    "C": [
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},     # Changed order [2] -> [0]
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},    # Single difference in value2
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},     # Changed order [0] -> [2]
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},     # Duplicated with [2]
    ],
}, recursively=True)
# ******************************************************************************
def test_SortedLists():
    print("*"*80 + " 1 = Sorted list in dictionary = direct_compare")
    differences1_direct_compare = dict1.direct_compare(dict2, "dict1", "dict2")
    for key in differences1_direct_compare:
        print("*"*3 + " " + key)
        for itm in differences1_direct_compare[key]:
            print(itm)
            
    print("*"*80 + " 2 = Sorted list in dictionary = wise_compare")
    differences2_wise_compare = dict1.compare(dict2, "dict1", "dict2",
        composite_key = ("a", "b", "c"),
        compare_only = ("value1", "value2")
    )
    for key in differences2_wise_compare:
        print("*"*3 + " " + key)
        for itm in differences2_wise_compare[key]:
            print(itm)
            
    n0print("="*80)
    n0debug("differences1_direct_compare")
    n0debug_calc(notemptyitems(differences1_direct_compare["messages"]), 'notemptyitems(differences1_direct_compare["messages"])')
    assert notemptyitems(differences1_direct_compare["messages"]) == 1
    n0debug_calc(notemptyitems(differences1_direct_compare["not_equal"]), 'notemptyitems(differences1_direct_compare["not_equal"])')
    assert notemptyitems(differences1_direct_compare["not_equal"]) == 4
    assert notemptyitems(differences1_direct_compare["difftypes"]) == 0
    assert notemptyitems(differences1_direct_compare["other_unique"]) == 0
    assert notemptyitems(differences1_direct_compare["self_unique"]) == 0
            
    n0print("="*80)
    n0debug("differences2_wise_compare")
    assert differences1_direct_compare["messages"]     == differences2_wise_compare["messages"]
    assert differences1_direct_compare["not_equal"]     == differences2_wise_compare["not_equal"]
    assert differences1_direct_compare["difftypes"]    == differences2_wise_compare["difftypes"]
    assert differences1_direct_compare["other_unique"] == differences2_wise_compare["other_unique"]
    assert differences1_direct_compare["self_unique"]== differences2_wise_compare["self_unique"]
# ******************************************************************************
def test_UnsortedLists():
    print("*"*80 + " 3 = Unsorted list in dictionary = direct_compare")
    differences1_direct_compare = dict1.direct_compare(dict3, "dict1", "dict3")
    for key in differences1_direct_compare:
        print("*"*3 + " " + key)
        for itm in differences1_direct_compare[key]:
            print(itm)
    
    print("*"*80 + " 4 = Unsorted list in dictionary = compare")
    differences2_wise_compare = dict1.compare(dict3, "dict1", "dict3",
        composite_key = ("a", "b", "c"),
        compare_only = ("value1", "value2")
    )
    for key in differences2_wise_compare:
        print("*"*3 + " " + key)
        for itm in differences2_wise_compare[key]:
            print(itm)
            
    n0print("="*80)
    n0debug("differences1_direct_compare")
    n0debug_calc(notemptyitems(differences1_direct_compare["messages"]), 'notemptyitems(differences1_direct_compare["messages"]')
    assert notemptyitems(differences1_direct_compare["messages"]) == 12
    n0debug_calc(notemptyitems(differences1_direct_compare["not_equal"]), 'differences1_direct_compare["not_equal"]')
    assert notemptyitems(differences1_direct_compare["not_equal"]) == 44
    assert notemptyitems(differences1_direct_compare["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences1_direct_compare["other_unique"]), 'notemptyitems(differences1_direct_compare["other_unique"])')
    assert notemptyitems(differences1_direct_compare["other_unique"]) == 6
    n0debug_calc(notemptyitems(differences1_direct_compare["self_unique"]), 'notemptyitems(differences1_direct_compare["self_unique"])')
    assert notemptyitems(differences1_direct_compare["self_unique"]) == 0

    n0print("="*80)
    n0debug("differences2_wise_compare")
    n0debug_calc(notemptyitems(differences2_wise_compare["messages"]), 'notemptyitems(differences2_wise_compare["messages"]')
    assert notemptyitems(differences2_wise_compare["messages"]) == 2
    n0debug_calc(notemptyitems(differences2_wise_compare["not_equal"]), 'differences2_wise_compare["not_equal"]')
    assert notemptyitems(differences2_wise_compare["not_equal"]) == 4
    assert notemptyitems(differences2_wise_compare["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences2_wise_compare["other_unique"]), 'notemptyitems(differences2_wise_compare["other_unique"])')
    assert notemptyitems(differences2_wise_compare["other_unique"]) == 6
    n0debug_calc(notemptyitems(differences2_wise_compare["self_unique"]), 'notemptyitems(differences2_wise_compare["self_unique"])')
    assert notemptyitems(differences2_wise_compare["self_unique"]) == 0
# ******************************************************************************
def main():
    n0print("="*80)
    n0debug_calc(dict1,"dict1")
    n0print("="*80)
    n0debug_calc(dict2,"dict2")
    n0print("="*80)
    n0debug_calc(dict2,"dict3")
    
    test_SortedLists()
    test_UnsortedLists()
    
    dict1["moreone/node[new()]/value"] = n0dict()
    dict1["moreone/node[new()]/value"] = None
    dict1["moreone/node[new()]/value"] = ""
    dict1["moreone/node[new()]/value"] = 1
    dict1["moreone/node[last()]/value"] = 2
    dict1["moreone/node[last()]/code"] = "two"
    dict1["moreone/node[new()]/value"] = 3
    dict1["moreone/node[-1]/value"] = 4
    dict1["moreone/node[-1]/code"] = "four"

    assert isinstance(dict1["moreone/node[0]/value"],n0dict) == True
    assert (dict1["moreone/node[1]/value"] is None) == True
    assert isinstance(dict1["moreone/node[2]/value"],str) == True
    assert (not dict1["moreone/node[2]/value"]) == True
    assert dict1["moreone/node[3]/value"] == 2
    assert dict1["moreone/node[4]/value"] == 4

    print(dict1.to_json())
    print(dict1.to_xml())

    print(dict1["moreone/node"])

    assert len(dict1["moreone/node"]) == 5
    assert len(dict1["moreone/node[*]"]) == 5

    print(dict1["moreone"])
    assert len(dict1["moreone"]) == 1

    print(dict1["moreone/node/code[text()='four']/../value"])
    assert dict1["moreone/node/code[text()='four']/../value"][0] == 4
    assert dict1["moreone/node/code[text()='four']/../value"] == [4]


    print(dict1["moreone/node/code[text()='two']/../value"])
    assert dict1["moreone/node/code[text()='two']/../value"] == [2]

    dict1["moreone/node/code[text()='two']/../value"] = 6
    print(dict1["moreone/node/code[text()='two']/../value"])
    assert dict1["moreone/node/code[text()='two']/../value"] == [6]
    assert dict1["moreone/node/code[text()=two]/../value"] == [6]
    assert dict1['moreone/node/code[text()="two"]/../value'] == [6]
    
    print(dict1["moreone/node[code='two']/value"])
    assert dict1["moreone/node[code='two']/value"] == [6]

    dict1["moretwo/node/code"] = "seven"
    dict1["moretwo/node/value"] = 7
    print(dict1["moretwo/node/code[text()='seven']/../value"])
    assert dict1["moretwo/node/code[text()='seven']/../value"] == 7
    
    print(dict1["moretwo/node[code='seven']/value"])
    assert dict1["moretwo/node[code='seven']/value"] == 7
    
    print(dict1.get("moretwo/node/code[text()='eight']/../value"))
    assert dict1.get("moretwo/node/code[text()='eight']/../value") is None
    
    print(dict1["?moretwo/node/code[text()='eight']/../value"] or None)
    assert (dict1["?moretwo/node/code[text()='eight']/../value"] or None) is None

if __name__ == '__main__':
    main()
