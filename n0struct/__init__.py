'''
list/dict extensions allow to
* work (find/get/set/update) with tree-like structures, generated for example by json.loads(..), using xpath approach
* wise compare of lists/dictionaries/tree-like structures + unification/transform (exclude from comparison) sub-nodes/values
* .to_json(): convert tree-like structures into string buffer for saving into JSON file
* .to_xml(): convert tree-like structures into string buffer for saving into XML file
* .to_xpath: convert tree-like structures into string buffer for saving into XPATH file
'''
import typing
from pathlib import Path
import sys
import os
import re

from .n0struct_arrays import *
from .n0struct_comprehensions import *
from .n0struct_data_to_json import *
from .n0struct_data_to_xml import *
from .n0struct_data_to_xpath import *
from .n0struct_date import *
from .n0struct_files import *
from .n0struct_files_csv import *
from .n0struct_files_fwf import *
from .n0struct_findall import *
from .n0struct_git import *
from .n0struct_logging import *
from .n0struct_mask import *
from .n0struct_n0compare import *
from .n0struct_n0dict_ import *
from .n0struct_n0dict__ import *
from .n0struct_n0list_ import *
from .n0struct_n0list_n0dict import *
from .n0struct_n0xml import *
from .n0struct_n1dict_n1list import *
from .n0struct_random import *
from .n0struct_references import *
from .n0struct_transform_dicts import *
from .n0struct_utils import *
from .n0struct_utils_compare import * # obsolete and will be decommissioned
from .n0struct_utils_find import *


################################################################################
__all__ = list(
    ('typing', 'Path', 'sys', 'os', 're')
    + n0struct_arrays.__all__
    + n0struct_comprehensions.__all__
    + n0struct_data_to_json.__all__
    + n0struct_data_to_xml.__all__
    + n0struct_data_to_xpath.__all__
    + n0struct_date.__all__
    + n0struct_files.__all__
    + n0struct_files_csv.__all__
    + n0struct_files_fwf.__all__
    + n0struct_findall.__all__
    + n0struct_git.__all__
    + n0struct_logging.__all__
    + n0struct_mask.__all__
    + n0struct_n0compare.__all__
    # + n0struct_n0dict_.__all__
    # + n0struct_n0dict__.__all__
    # + n0struct_n0list_.__all__
    + n0struct_n0list_n0dict.__all__
    + n0struct_n0xml.__all__
    + n0struct_n1dict_n1list.__all__
    + n0struct_random.__all__
    + n0struct_references.__all__
    + n0struct_transform_dicts.__all__
    + n0struct_utils.__all__
    + n0struct_utils_compare.__all__
    + n0struct_utils_find.__all__
    
)
