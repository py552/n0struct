import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import (
    split_with_escape,
    n0print,
    n0debug,
    init_logger,
)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)


def test_split_with_escape():
    buffer_str = "AAAA1;BBBB2;CCCC3;DDDD4"; n0debug("buffer_str")
    result = split_with_escape(buffer_str, ';'); n0debug("result")
    expected_result = ["AAAA1", "BBBB2", "CCCC3", "DDDD4"]; n0debug("expected_result")
    assert result == expected_result

    buffer_str = "\\\\AA\\AA1\\;\\\\BB\\BB2;\\CC\\\\CC3\\\\;DD\\DD4\\\\"; n0debug("buffer_str")
    result = split_with_escape(buffer_str, ';'); n0debug("result")
    expected_result = ["\\\\AA\\AA1;\\\\BB\\BB2", "\\CC\\\\CC3\\", "DD\\DD4\\"]; n0debug("expected_result")
    assert result == expected_result

    buffer_str = "\\\\AA\\AA1\\;\\\\BB\\BB2;\\CC\\\\CC3\\\\;DD\\DD4\\\\"; n0debug("buffer_str")
    result = split_with_escape(buffer_str, ';', trim_trailing_double_escape_characters = False); n0debug("result")
    expected_result = ["\\\\AA\\AA1;\\\\BB\\BB2", "\\CC\\\\CC3\\\\", "DD\\DD4\\\\"]; n0debug("expected_result")
    assert result == expected_result


# ******************************************************************************
def main():
    test_split_with_escape()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_split_with_escape',
    'main',
)
################################################################################
