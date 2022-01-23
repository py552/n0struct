# -*- coding: utf-8 -*-
# 0.01 = 2020-07-25 = Initial version
# 0.02 = 2020-07-26 = Enhancements
# 0.03 = 2020-08-02 = Huge enhancements
# 0.04 = 2020-08-05 = Prepared for upload to pypi.org
# 0.05 = 2020-08-11 = Huge enhancements: unification of .*compare() .toJson(), .toXml(), n0dict(JSON/XML string)
# 0.06
# 0.07 = 2020-09-02 = .compare(transform=..) and .direct_compare(transform=..) added
# 0.08 = 2020-09-05 = refactoring
# 0.09 = lost
# 0.10 = rewritten date related functions
# 0.11 = 2020-09-17 fixed returning time by date_delta(..)
# 0.12 = 2020-09-24 added function to find keys in n0dict
# 0.13 = 2020-10-11
#        n0dict.nvl(..) now supports complicated path like A/B/C
#        n0dict.__FindElem(..) previously supports modificators [i], [last()], [last()-X], [-X]
#                              now additionally supports modificators [text()="XYZ"], [text()=="XYZ"], [text()!="XYZ"], /../
#                              XYZ must be encoded with urlencode
# 0.14 = 2020-10-17 n0print prints to stderr
# 0.15 = 2020-10-19 n0pretty(..): fix for json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes
#                   strip_namespaces() is added
# 0.16 = 2020-10-20 strip_namespaces() transformed into transform_structure()
#                   n0dict.compare() is fixed to use compare_only=
# 0.17 = 2020-10-22 n0print(..): optimization
# 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
# 0.19 = 2020-10-24 fixed issue with autotests, recursive convertion is added into constructor
# 0.20 = 2020-10-26 get_composite_keys(transform=..) is added, numeric checking is fixed
# 0.21 = 2020-11-09 fixed Exception: Why parent is None?
#                   date_slash_ddmmyyyy() is added
# 0.22 = 2020-11-09 fixed date_now() -> str 20 characters YYYYMMDDHHMMSSFFFFFF
# 0.23 = 2020-11-14 fixed n0list.compare()'s issue if more that one the same records are in the list
#                   *.compare() return ["othernotfound"] -> "self_unique"
#                   *.compare() return ["selfnotfound"]  -> "other_unique"
#                   *.compare() return ["notequal"]      -> "not_equal"
#                   get_composite_keys(..) -> generate_composite_keys(..)
# 0.24 = 2020-11-20 added is_exist(..), rewritten to_json(..), AddElem(..)'s optimization started
# 0.25 = 2020-11-20 removed:
#                       n0dict. __FindElem(..)
#                       n0dict. __AddElem(..)
#                       n0dict. AddElem(..)
#                   rewritten:
#                       n0dict. __getitem__(..)
#                       n0dict. __setitem__(..)
#                   added:
#                       n0dict. _find(..)
#                       n0dict. _add(..)
# 0.26 = 2020-12-15 rewritten n0dict. nvl()
# 0.27 = 2020-12-16
#                   added:
#                       n0dict. _get(..)
#                   rewritten:
#                       n0dict. __getitem__(..)
#                       n0dict. nvl()
#                       n0dict. _add()
#                   fixed:
#                       n0pretty()
# 0.28 = 2020-12-17
#                   renamed:
#                       n0dict. nvl() -> get(..)
#                   rewritten:
#                       n0dict. __setitem__(..)
#                       n0dict. _add()
# 0.29 = 2020-12-18
#                   added:
#                       n0list. any_*()
# 0.30 = 2020-12-20
#                   added:
#                       n0list. __contains__()  # something in n0list()
#                       n0dict. valid()
# 0.31 = 2020-12-20
#                   rewritten:
#                       n0dict. _find(..)
#                       split_name_index(..)
# 0.32 = 2020-12-21
#                   fixed:
#                       n0dict. _find(..): if not parent_node: => if parent_node is None:
#                                          because of parent_node could be '' as allowed value
# 0.33 = 2020-12-22
#                   enhanced:
#                       n0dict. _find(..): parent_node become mandatory argument
#                       n0dict. _get(..): support leading '?' in xpath
# 0.34 = 2020-12-24
#                   enhanced:
#                       n0list. __init__(..): option recursively:bool = True was added
#                       n0dict. __init__(..): option recursively:bool = True was added
# 0.35 = 2020-12-26
#                   enhanced:
#                       n0dict. __xml(..): nodes int, float support added
#                       n0dict. to_xml(..): multi-root support added
#                   enhanced version of xmltodict0121 was incapsulated till changes will be merged with main branch of xmltodic
#                   xmltodict0121 enhancement: automaticaly creation n0dict/n0list structure during XML import
# 0.36 = 2020-12-27
#                   xmltodict0121 was removed -- using strandard fuctionality of json and xmltodict: just only dict to n0dict will be automatic converted
#                   during loading xml/json and automatic conversion list into n0list use named parameter recursively=True in the costructor:
#                   my_n0dict = n0dict(json_txt, recursively=True)
#                   enhanced:
#                       n0dict. __init__(..)
#                       n0list. __init__(..)
#                       n0dict. __path(..)
#                       test_n0struct.py
# 0.37 = 2020-12-28
#                   fixed:
#                       n0dict. __xml(..)
# 0.38 = 2020-12-29
#                   enhanced:
#                       n0dict. __init__(..): option force_n0dict == None|!None was added, used ONLY for JSON text convertion
#                           force_n0dict == False/0/None => create [] (ordinary dict) nodes during JSON text convertion (json.loads)
#                           force_n0dict == True/1/any => create n0dict() nodes during JSON text convertion (json.loads)
#                           recursively == True => convert all list/dict nodes created during JSON text convertion (json.loads) into n0list/n0dict
#
#                       Performance results of some real code with JSON convertion:
#                           JSON_struct = n0dict(JSON_txt, recursively=True) => n0dict/n0list:
#                               36.889860 MB memory is used, 2.566520 seconds are taken for execution
#                           JSON_struct = n0dict(JSON_txt, recursively=False) => dict/list => JSON_subnode = n0dict(JSON_struct["node/subnode"]):
#                               36.945560 MB memory is used, 2.546720 seconds are taken for execution
#                           JSON_struct = n0dict(JSON_txt, force_n0dict=True) => n0dict/list:
#                               36.995180 MB memory is used, 2.576020 seconds are taken for execution
#
#                       Results are VERY strange, but they are true:
#                           Minimum memory usage: load as list/dict, and after convert all of them into n0list/n0dict inside constructor
#                           Maximum speed: load as list/dict, and after convert just requiered nodes into n0dict
#                       *** BEFORE MAKING DECISION MAKE YOUR OWN PERFORMACE TESTING ***
#
#                       Same for XML:
#                           XML_struct = n0dict(XML_txt, recursively=True) => n0dict/n0list:
#                           XML_struct = n0dict(XML_txt, recursively=False) => n0dict/list
#                           XML_struct = n0dict(XML_txt, force_n0dict=True) =>
#                               force_n0dict is ignored -- the same like n0dict(XML_txt, recursively=False) => n0dict/list
# 0.39 = 2021-01-04
#                   fixed:
#                       n0dict. __init__(..): xmltodict.parse(args[0], dict_constuctor = n0dict),
# 0.40 = 2021-01-08
#                   enhanced:
#                       n0pretty(item, indent_: int = 0, show_type:bool = True):
#                   added:
#                       n0dict. first(..)
#                       n0list. __getitem__(..)
#                       n0list. _get(..)
#                       n0list. get(..)
#                       n0list. first(..)
# 0.41 = 2021-01-09
#                   enhanced:
#                       Added predicate attrib[contains(text(),"TEXT")] or attrib[text()~~"TEXT"] or [attrib~~"TEXT"]
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/@value[contains(text(),"PRE")]/../@value'))
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/@value[text()~~"PRE"]/../@value'))
#                           xml.first('/repository/instanceInfo/instanceInfoProperty/[@value~~"PRE"]/@value'))
# 0.42 = 2021-01-22
#                   enhanced:
#                       n0debug(..)
#                       mypy optimization
# 0.43 = 2021-01-28
#                   enhanced:
#                       mypy optimization
#                       compare()["messages"] -> compare()["differences"]
#                       compare(exclude=) -> compare(exclude_xpaths=)
#                   added:
#                       def load_file(file_name: str) -> list:
#                       def save_file(file_name: str, lines: typing.Any):
#                       def load_serialized(...):
# 0.44 = 2021-02-08
#                   fixed:
#                       split_name_index(..)
# 0.45 = 2021-02-27
#                   enhanced:
#                       mypy optimization
#                       def init_logger(..)
#                   added:
#                       def timestamp() -> str:
#                       def date_yymmdd(now: typing.Union[datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
#                       class OrderedSet(MutableSet):
#                       def unpack_references(initial_dict: dict, initial_key: str, recursive: bool = True) -> OrderedSet:
#                       class Git():
#                   fixed:
#                       n0list. _get(..)
# 0.45 = 2021-03-05
#                   added:
#                       n0dict. def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> n0dict:
#                       n0dict. def delete(self, xpath: str, recursively: bool = False) -> n0dict:
#                       n0dict. def pop(self, xpath: str, recursively: bool = False) -> typing.Any:
# 0.46 = 2021-07-21 optimized for debugging
# 0.47 = 2021-07-21 fix for n0pretty()
# 0.48 = 2021-07-22
#                   added:
#                       def mask_number(not_masked_number: str):
#                       def unmask_number(masked_number: str):
#                       def mask_pan(buffer: str):
# 0.49 = 2021-07-23 fix for n0pretty()
# 0.50 = 2021-08-04 Impossible easely adopt for 3.6, only for 3.7, because of some modules (for example: immutables)
#                   are not precompiled for 3.6 at pypi.org. So installing of Visual C/C++ (or MinGW) is required.
# 0.51 = 2021-09-01
#                   fixed:
#                       n0dict. to_xpath(): prevent xpath generating for empty structures
#                       n0dict. _find(): changing incoming var name found_xpath_str -> xpath_found_str
# 0.52 = 2021-09-02
#                   added/enhanced:
#                       n0dict. __init__(file="{file_path}")
#                       n0dict. to_json/n0pretty(pairs_in_one_line=True)
# 0.53 = 2022-01-20 enhanced: n0dict. to_json/n0pretty(skip_none = False, skip_empty_arrays = False, skip_simple_types = True, auto_quotes = True)
# 0.54 = 2022-01-21 fixed defect got in 0.2.51, some enchancements in n0pretty
# 0.55 = 2022-01-21 try #2 to split single __init__.py into separate files
# 0.56 = 2022-01-23 fixed defect with using child class in parent
# ******************************************************************************
# ******************************************************************************
from .n0struct_date import *
from .n0struct_random import *
from .n0struct_references import *
from .n0struct_git import *
from .n0struct_arrays import *
from .n0struct_mask import *
from .n0struct_utils import *
from .n0struct_transform_structure import *
from .n0struct_logging import *
from .n0struct_files import *
from .n0struct_utils_find import *
from .n0struct_utils_compare import *
from .n0struct_findall import *
from .n0struct_n0list_n0dict import *
# ******************************************************************************
# ******************************************************************************
