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
    n0error,
    # n0debug_object,
    # load_ini,
    # save_file,
    # load_file,
    # load_csv,
    # load_lines,
    init_logger,

    split_pair,
)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)

# ******************************************************************************
def test_n0struct_arrays():
    '''
        '' by '://'                                     => (default_left, default_right)
        'www.aaa.com' by '://'                          => (default_left, 'www.aaa.com')
        'https://www.aaa.com' by '://'                  => ('http', 'www.aaa.com')
        'www.aaa.com',default_element = 0 by '/'        => ('www.aaa.com')
        'www.aaa.com/path',default_element = 0 by '/'   => ('www.aaa.com', 'path')
    '''
    result = split_pair('', '://')
    n0debug("result")
    assert result == ('', '')

    result = split_pair('', '://', default_left='default_left', default_right='default_right')
    n0debug("result")
    assert result == ('default_left', 'default_right')

    result = split_pair(None, '://')
    n0debug("result")
    assert result == ('', '')

    result = split_pair('tag=value', '=')
    n0debug("result")
    assert result == ('tag', 'value')

    result = split_pair('www.aaa.com', '://')
    n0debug("result")
    assert result == ('', 'www.aaa.com')

    result = split_pair('https://www.aaa.com', '://')
    n0debug("result")
    assert result == ('https', 'www.aaa.com')

    result = split_pair('www.aaa.com', '/')
    n0debug("result")
    assert result == ('', 'www.aaa.com')

    result = split_pair('www.aaa.com', '/', default_element=0)
    n0debug("result")
    assert result == ('www.aaa.com', '')

    result = split_pair('www.aaa.com/path/', '/', default_element=0)
    n0debug("result")
    assert result == ('www.aaa.com', 'path/')

    # Negative scenariouses
    try:
        result = split_pair('tag=value', '')
    except ValueError as ex:
        n0error(ex)

    try:
        result = split_pair('tag=value', None)
    except ValueError as ex:
        n0error(ex)

    result = split_pair('tag=value', None)
    n0debug("result")
    assert result == ('', 'tag=value')

    result = split_pair('tag=value', None, default_element=0)
    n0debug("result")
    assert result == ('tag=value', '')

# ******************************************************************************
def main():
    test_n0struct_arrays()

# ******************************************************************************
if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_n0struct_arrays',
    'main',
)
################################################################################
