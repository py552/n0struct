import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import *
# from n0struct import (
    # n0print,
    # n0debug,
    # # n0debug_calc,
    # # set__flag_compare_check_different_types,
    # # set__flag_compare_return_difference_of_values,
    # # init_logger,
    
    # # deserialize_list,
    # # deserialize_fixed_list,
    # # deserialize_dict,
    # # get_value_by_tag,
    # # deserialize_list_of_lists,
    # load_ini,
    # save_file,
# )

# ******************************************************************************
dict1 = n0dict({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 5},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
}, recursively=True)


def test_n0dict():
    to_xpath_result = dict1.to_xpath()
    n0debug("to_xpath_result")
    
    to_xpath_expected_result = '''[\'//C[0]/a\']      = "1"
[\'//C[0]/b\']      = "2"
[\'//C[0]/c\']      = "3"
[\'//C[0]/value1\'] = "1"
[\'//C[0]/value2\'] = "4"
[\'//C[1]/a\']      = "4"
[\'//C[1]/b\']      = "5"
[\'//C[1]/c\']      = "6"
[\'//C[1]/value1\'] = "2"
[\'//C[1]/value2\'] = "5"
[\'//C[2]/a\']      = "7"
[\'//C[2]/b\']      = "8"
[\'//C[2]/c\']      = "9"
[\'//C[2]/value1\'] = "3"
[\'//C[2]/value2\'] = "6"
'''
    # n0debug("to_xpath_expected_result")

    assert to_xpath_result == to_xpath_expected_result

# ******************************************************************************
def main():
    test_n0dict()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")
