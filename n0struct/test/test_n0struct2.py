import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import (
    n0print,
    n0debug,
    n0debug_calc,
    set__flag_compare_check_different_types,
    set__flag_compare_return_difference_of_values,
    init_logger,
    
    deserialize_list,
    deserialize_fixed_list,
    deserialize_dict,
    get_value_by_tag,
    deserialize_list_of_lists,
)
set__flag_compare_check_different_types(True)
set__flag_compare_return_difference_of_values(True)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)

# ******************************************************************************
def test_deserialization():
    my_list = ("1", "2", "3")
    
    serialized_list = ';'.join(my_list)
    n0debug("serialized_list")
    deserialized_list = deserialize_list(serialized_list)
    n0debug("deserialized_list")
    assert deserialized_list[1] == my_list[1]

    serialized_list = ','.join(my_list)
    n0debug("serialized_list")
    deserialized_list = deserialize_list(serialized_list, ',')
    n0debug("deserialized_list")
    assert deserialized_list[1] == my_list[1]
    
    serialized_list = ';'.join(my_list)
    n0debug("serialized_list")
    deserialized_list = deserialize_fixed_list(serialized_list, 4, default_item = "444")
    n0debug("deserialized_list")
    assert deserialized_list[3] == "444"

    my_list = ("a=1", "b=2", "c=3")
    serialized_dict = ';'.join(my_list)
    n0debug("serialized_dict")
    deserialized_dict = deserialize_dict(serialized_dict)
    n0debug("deserialized_dict")
    assert deserialized_dict["c"] == "3"
    
    n0debug("serialized_dict")
    n0debug_calc(get_value_by_tag("b", serialized_dict), 'get_value_by_tag("b", serialized_dict)')
    assert get_value_by_tag("b", serialized_dict) == "2"

    my_list = ("a1,a2,a3", "b1,b2,b3", "c1,c2,c3")
    serialized_list_of_lists = ';'.join(my_list)
    n0debug("serialized_list_of_lists")
    deserialized_list_of_lists = deserialize_list_of_lists(serialized_list_of_lists)
    n0debug("deserialized_list_of_lists")
    assert deserialized_list_of_lists[1][2] == "b3"

# ******************************************************************************
def main():
    test_deserialization()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_deserialization',
    'main',
    'mydir',
)
################################################################################
