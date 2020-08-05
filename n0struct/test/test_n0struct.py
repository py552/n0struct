import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import *

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
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})
# ******************************************************************************
# Unsorted list in dictionary
# ******************************************************************************
dict3 = n0dict({
    "C": [
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
    ],
})
# ******************************************************************************
def test_SortedLists():
    print("*"*80 + " 1 = Sorted list in dictionary = direct_compare_dict")
    differences1 = dict1.direct_compare_dict(dict2, "dict1", "dict2")
    for key in differences1:
        print("*"*3 + " " + key)
        for itm in differences1[key]:
            print(itm)
            
    print("*"*80 + " 2 = Sorted list in dictionary = compare_dict")
    differences2 = dict1.compare_dict(dict2, "dict1", "dict2",
        elements_for_composite_key = ("a", "b", "c"),
        elements_for_compare = ("value1", "value2")
    )
    for key in differences2:
        print("*"*3 + " " + key)
        for itm in differences2[key]:
            print(itm)
            
    n0print("="*80)
    n0debug("differences1")
    n0debug_calc(notemptyitems(differences1["messages"]), 'notemptyitems(differences1["messages"])')
    assert notemptyitems(differences1["messages"]) == 1
    n0debug_calc(notemptyitems(differences1["notequal"]), 'notemptyitems(differences1["notequal"])')
    assert notemptyitems(differences1["notequal"]) == 3
    assert notemptyitems(differences1["difftypes"]) == 0
    assert notemptyitems(differences1["selfnotfound"]) == 0
    assert notemptyitems(differences1["othernotfound"]) == 0
            
    n0print("="*80)
    n0debug("differences2")
    assert differences1["messages"]     == differences2["messages"]
    assert differences1["notequal"]     == differences2["notequal"]
    assert differences1["difftypes"]    == differences2["difftypes"]
    assert differences1["selfnotfound"] == differences2["selfnotfound"]
    assert differences1["othernotfound"]== differences2["othernotfound"]
# ******************************************************************************
def test_UnsortedLists():
    print("*"*80 + " 3 = Unsorted list in dictionary = direct_compare_dict")
    differences1 = dict1.direct_compare_dict(dict3, "dict1", "dict2")
    for key in differences1:
        print("*"*3 + " " + key)
        for itm in differences1[key]:
            print(itm)
    
    print("*"*80 + " 4 = Unsorted list in dictionary = compare_dict")
    differences2 = dict1.compare_dict(dict3, "dict1", "dict2",
        elements_for_composite_key = ("a", "b", "c"),
        elements_for_compare = ("value1", "value2")
    )
    for key in differences2:
        print("*"*3 + " " + key)
        for itm in differences2[key]:
            print(itm)
            
    n0print("="*80)
    n0debug("differences1")
    n0debug_calc(notemptyitems(differences1["messages"]), 'notemptyitems(differences1["messages"]')
    assert notemptyitems(differences1["messages"]) == 16
    n0debug_calc(notemptyitems(differences1["notequal"]), 'differences1["notequal"]')
    assert notemptyitems(differences1["notequal"]) == 45
    assert notemptyitems(differences1["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences1["selfnotfound"]), 'notemptyitems(differences1["selfnotfound"])')
    assert notemptyitems(differences1["selfnotfound"]) == 6
    n0debug_calc(notemptyitems(differences1["othernotfound"]), 'notemptyitems(differences1["othernotfound"])')
    assert notemptyitems(differences1["othernotfound"]) == 0

    n0print("="*80)
    n0debug("differences2")
    n0debug_calc(notemptyitems(differences2["messages"]), 'notemptyitems(differences2["messages"]')
    assert notemptyitems(differences2["messages"]) == 2
    n0debug_calc(notemptyitems(differences2["notequal"]), 'differences2["notequal"]')
    assert notemptyitems(differences2["notequal"]) == 3
    assert notemptyitems(differences2["difftypes"]) == 0
    n0debug_calc(notemptyitems(differences2["selfnotfound"]), 'notemptyitems(differences2["selfnotfound"])')
    assert notemptyitems(differences2["selfnotfound"]) == 6
    n0debug_calc(notemptyitems(differences2["othernotfound"]), 'notemptyitems(differences2["othernotfound"])')
    assert notemptyitems(differences2["othernotfound"]) == 0
# ******************************************************************************
def main():
    test_SortedLists()
    test_UnsortedLists()

if __name__ == '__main__':
    main()
