import os
import sys
import datetime
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
from n0struct import (
    n0print,
    n0debug,
    n0debug_calc,
    n0error,
    init_logger,
    
    is_date_format,
    to_date,
)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)

# ******************************************************************************
def test_n0struct_date():
    result = is_date_format("230502", '%Y%m%d')
    n0debug("result")
    assert result == False

    # Reproducing of issue in standard library
    result = datetime.datetime.strptime("200129", '%Y%m%d')
    n0debug("result")
    assert result == to_date("2001-02-09 00:00:00")

    result = datetime.datetime.strptime("200129", '%Y%m%d').date()
    n0debug("result")
    assert result == to_date("2001-02-09")

    result = is_date_format("200129", '%Y%m%d')
    n0debug("result")
    assert result == False

    result = is_date_format("230502", '%y%m%d')
    n0debug("result")
    assert result == to_date("2023-05-02")

    result = is_date_format("200129", '%y%m%d')
    n0debug("result")
    assert result == to_date("2020-01-29")

    result = is_date_format("230502", '%y%d%m')
    n0debug("result")
    assert result == to_date("2023-02-05")

    result = is_date_format("200129", '%y%d%m')
    n0debug("result")
    assert result == False

    result = not is_date_format("200129", '%y%d%m')
    n0debug("result")
    assert result == True


# ******************************************************************************
def main():
    test_n0struct_date()

# ******************************************************************************
if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_n0struct_date',
    'main',
)
################################################################################
