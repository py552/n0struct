import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import (
    n0dict,
    n0print,
    n0debug,
    init_logger,
)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)

# ******************************************************************************
dict1 = n0dict.convert_recursively({
    "C": [
        {"a": 1, "b": 2, "c": 3, "value1": 1, "value2": 4},
        {"a": 4, "b": 5, "c": 6, "value1": 2, "value2": 5},
        {"a": 7, "b": 8, "c": 9, "value1": 3, "value2": 6},
    ],
})


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
    n0debug("to_xpath_expected_result")

    assert to_xpath_result == to_xpath_expected_result

# ******************************************************************************
def main():
    test_n0dict()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_n0dict',
    'main',
)
################################################################################
