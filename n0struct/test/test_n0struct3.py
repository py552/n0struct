import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import (
    n0print,
    n0debug,
    # n0debug_calc,
    # set__flag_compare_check_different_types,
    # set__flag_compare_return_difference_of_values,
    # init_logger,
    
    # deserialize_list,
    # deserialize_fixed_list,
    # deserialize_dict,
    # get_value_by_tag,
    # deserialize_list_of_lists,
    load_ini,
    save_file,
)

# ******************************************************************************
def test_files_processing():
    test_ini_path = os.path.join(mydir, "test.ini")
    n0debug("test_ini_path")
    test_ini = load_ini(test_ini_path)
    n0debug("test_ini")
    save_file(os.path.join(mydir, "test.tmp"), test_ini, mode='b', EOL='\n')
    

# ******************************************************************************
def main():
    test_files_processing()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")
