import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import *

def test_use_external_libraries():
    n0print(Path(__file__))
    n0debug_calc(Path(__file__))
    n0error(Path(__file__))
    n0warning(Path(__file__))
    n0info(Path(__file__))

# ******************************************************************************
def main():
    test_use_external_libraries()
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")


