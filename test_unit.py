from n0struct import n0dict

dict1 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 5},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})

dict2 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})
# ******************************************************************************
print("*"*80 + " 1 = SortedList = obvious_compare_dict")
difference = dict1.obvious_compare_dict(dict2, "dict1", "dict2")
for key in difference:
    print("*"*3 + " " + key)
    for itm in difference[key]:
        print(itm)
# ******************************************************************************
print("*"*80 + " 2 = SortedList = vogue_compare_dict")
difference = dict1.vogue_compare_dict(dict2, "dict1", "dict2",
    list_elements_for_composite_key = ("a", "b", "c"),
    list_elements_for_compare = ("value1", "value2")
)
for key in difference:
    print("*"*3 + " " + key)
    for itm in difference[key]:
        print(itm)
# ******************************************************************************
dict2 = n0dict({
    "C": [
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 99},
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
    ],
})
# ******************************************************************************
print("*"*80 + " 3 = UnsortedList = obvious_compare_dict")
difference = dict1.obvious_compare_dict(dict2, "dict1", "dict2")
for key in difference:
    print("*"*3 + " " + key)
    for itm in difference[key]:
        print(itm)
# ******************************************************************************
print("*"*80 + " 4 = UnsortedList = vogue_compare_dict")
difference = dict1.vogue_compare_dict(dict2, "dict1", "dict2",
    list_elements_for_composite_key = ("a", "b", "c"),
    list_elements_for_compare = ("value1", "value2")
)
for key in difference:
    print("*"*3 + " " + key)
    for itm in difference[key]:
        print(itm)
# ******************************************************************************
