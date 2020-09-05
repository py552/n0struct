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
})
# ******************************************************************************
# Sorted list in dictionary
# ******************************************************************************
dict2 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},    # Single difference in value2
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})
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
})
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
    n0debug_calc(notemptyitems(differences1_direct_compare["notequal"]), 'notemptyitems(differences1_direct_compare["notequal"])')
    assert notemptyitems(differences1_direct_compare["notequal"]) == 4
    assert notemptyitems(differences1_direct_compare["difftypes"]) == 0
    assert notemptyitems(differences1_direct_compare["selfnotfound"]) == 0
    assert notemptyitems(differences1_direct_compare["othernotfound"]) == 0
            
    n0print("="*80)
    n0debug("differences2_wise_compare")
    assert differences1_direct_compare["messages"]     == differences2_wise_compare["messages"]
    assert differences1_direct_compare["notequal"]     == differences2_wise_compare["notequal"]
    assert differences1_direct_compare["difftypes"]    == differences2_wise_compare["difftypes"]
    assert differences1_direct_compare["selfnotfound"] == differences2_wise_compare["selfnotfound"]
    assert differences1_direct_compare["othernotfound"]== differences2_wise_compare["othernotfound"]
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
    n0debug_calc(notemptyitems(differences1_direct_compare["notequal"]), 'differences1_direct_compare["notequal"]')
    assert notemptyitems(differences1_direct_compare["notequal"]) == 44
    assert notemptyitems(differences1_direct_compare["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences1_direct_compare["selfnotfound"]), 'notemptyitems(differences1_direct_compare["selfnotfound"])')
    assert notemptyitems(differences1_direct_compare["selfnotfound"]) == 6
    n0debug_calc(notemptyitems(differences1_direct_compare["othernotfound"]), 'notemptyitems(differences1_direct_compare["othernotfound"])')
    assert notemptyitems(differences1_direct_compare["othernotfound"]) == 0

    n0print("="*80)
    n0debug("differences2_wise_compare")
    n0debug_calc(notemptyitems(differences2_wise_compare["messages"]), 'notemptyitems(differences2_wise_compare["messages"]')
    assert notemptyitems(differences2_wise_compare["messages"]) == 2
    n0debug_calc(notemptyitems(differences2_wise_compare["notequal"]), 'differences2_wise_compare["notequal"]')
    assert notemptyitems(differences2_wise_compare["notequal"]) == 4
    assert notemptyitems(differences2_wise_compare["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences2_wise_compare["selfnotfound"]), 'notemptyitems(differences2_wise_compare["selfnotfound"])')
    assert notemptyitems(differences2_wise_compare["selfnotfound"]) == 6
    n0debug_calc(notemptyitems(differences2_wise_compare["othernotfound"]), 'notemptyitems(differences2_wise_compare["othernotfound"])')
    assert notemptyitems(differences2_wise_compare["othernotfound"]) == 0
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

if __name__ == '__main__':
    main()
