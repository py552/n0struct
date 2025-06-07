from typing import Any, List, Dict, Optional, Callable, Union, Tuple
from collections import defaultdict
import inspect
import re

_EXCLUDE_NODE_MARKER = object()
class n0compare:
    """
    Class for flexible comparison of nested sctructures dict/list with supporting of composite keys
    """
    def __new__(cls, *args, **kwargs):
        """ __new__() will be executed before __init__() and it will allow to return back custom result """
        # Get signanture of own __init__(...) and get bind arguments as own __init__(...)
        bound = inspect.signature(cls.__init__).bind(None, *args, **kwargs)
        bound.apply_defaults()

        newobj = super().__new__(cls)
        newobj.show_equals = bound.arguments['show_equals']
        newobj.fuzzy_threshold = bound.arguments['fuzzy_threshold']
        newobj.composite_keys = bound.arguments['composite_keys'] or {}

        return newobj._compare_objs(
            bound.arguments['obj1'],
            bound.arguments['obj2'],
            bound.arguments['parent_xpath1'],
            bound.arguments['parent_xpath2']
        )

    def __init__(
        self,
        obj1: Any,
        obj2: Any,
        parent_xpath1: Optional[str] = "",
        parent_xpath2: Optional[str] = "",
        show_equals: Optional[bool] = False,
        fuzzy_threshold: Optional[int] = 6,
        composite_keys: Optional[Dict[re.Pattern, Tuple[str, ...]]] = None,
    ):
        """ Main entry point for comparison: n0compare(dict1, dict2, [optional parameters]) """
        pass

    def _get_composite_keys(self, _dict: Dict, xpath: str) -> Optional[Tuple[str, ...]]:
        """ Return composite keys for xpath or all keys if xpath is not matched """
        _composite_keys = None
        for pattern, keys in self.composite_keys.items():
            if pattern.match(xpath):
                _composite_keys = [key for key in keys if key in _dict]
        return sorted(_composite_keys or _dict.keys())

    def _to_hashable(self, obj: Any, xpath: str = "") -> Any:
        """ Create hashable represenative of object using composite keys for dictionaries. """
        if self.composite_keys:
            if isinstance(obj, dict):
                return tuple(
                        (k, self._to_hashable(obj[k], f"{xpath}/{k}"))
                        for k in self._get_composite_keys(obj, xpath)
                    )
            elif isinstance(obj, (list, tuple)):
                return tuple(self._to_hashable(v, f"{xpath}[{i}]") for i, v in enumerate(obj))
            elif isinstance(obj, (set, frozenset)):
                return tuple(sorted(self._to_hashable(v, f"{xpath}[{hash(v)}]") for v in obj))
        return str(obj)

    def _compare_lists(
        self,
        list1: List[Any],
        list2: List[Any],
        parent_xpath1: str,
        parent_xpath2: str,
    ) -> Dict:
        """ Compare 2 lists using fuzzy logic. """
        result = {"only_in_1": [], "only_in_2": [], "diffs": {}}
        if self.show_equals:
            result["equals"] = {}

        only_in_1 = []
        indexes2_by_hash = defaultdict(list)
        for indx2, item2 in enumerate(list2):
            item2_hash = self._to_hashable(item2, parent_xpath2)
            indexes2_by_hash[item2_hash].append(indx2)

        for indx1, item1 in enumerate(list1):
            item1_hash = self._to_hashable(item1, parent_xpath1)
            found = False
            if item1_hash in indexes2_by_hash and indexes2_by_hash[item1_hash]:
                indx2 = indexes2_by_hash[item1_hash].pop(0)
                if self.show_equals:
                    result["equals"][f"{parent_xpath1}[{indx1}]"] = f"{parent_xpath2}[{indx2}]"
                found = True
            else:
                # Fuzzy matching
                best_match = None
                min_diff = float("inf")
                for indx2 in list(indexes2_by_hash.get(item1_hash, [])):
                    comparison_result = self._compare_objs(
                        item1, list2[indx2], f"{parent_xpath1}[{indx1}]", f"{parent_xpath2}[{indx2}]"
                    )
                    diff_count = sum(
                        len(sublist)
                        for key, sublist in comparison_result.items()
                        if key in ("only_in_1", "only_in_2", "diffs")
                    )
                    if diff_count == 0:
                        indexes2_by_hash[item1_hash].remove(indx2)
                        if self.show_equals:
                            result["equals"][f"{parent_xpath1}[{indx1}]"] = f"{parent_xpath2}[{indx2}]"
                        found = True
                        break
                    elif diff_count < min_diff:
                        min_diff = diff_count
                        best_match = (indx2, comparison_result)
                else:
                    if min_diff < self.fuzzy_threshold:
                        indx2, comparison_result = best_match
                        indexes2_by_hash[item1_hash].remove(indx2)
                        merge_dicts(result, comparison_result)
                        found = True
            if not found:
                only_in_1.append(indx1)

        only_in_2 = sorted(
            indx2 for indexes2 in indexes2_by_hash.values() for indx2 in indexes2
        )

        # try to find most similar mismatches
        if only_in_1 and only_in_2:
            for indx1 in tuple(only_in_1):
                best_match = None
                min_diff = float("inf")
                for indx2 in only_in_2:
                    comparison_result = self._compare_objs(
                        list1[indx1], list2[indx2], f"{parent_xpath1}[{indx1}]", f"{parent_xpath2}[{indx2}]"
                    )
                    diff_count = sum(
                        len(sublist)
                        for key, sublist in comparison_result.items()
                        if key in ("only_in_1", "only_in_2", "diffs")
                    )
                    if diff_count < min_diff:
                        min_diff = diff_count
                        best_match = (indx2, comparison_result)
                if min_diff < self.fuzzy_threshold:
                    indx2, comparison_result = best_match
                    merge_dicts(result, comparison_result)
                    only_in_1.remove(indx1)
                    only_in_2.remove(indx2)

        result = merge_dicts(
            result,
            {
                "only_in_1": [f"{parent_xpath1}[{i}]" for i in only_in_1],
                "only_in_2": [f"{parent_xpath2}[{i}]" for i in only_in_2],
            },
        )
        return result

    def _compare_dicts(
        self, dict1: Dict, dict2: Dict, parent_xpath1: str, parent_xpath2: str
    ) -> Dict:
        """ Compare 2 dicts using fuzzy logic. """
        result = {"only_in_1": [], "only_in_2": [], "diffs": {}}
        if self.show_equals:
            result["equals"] = {}

        keys1, keys2 = set(dict1.keys()), set(dict2.keys())
        for key in keys1 | keys2:
            in_1, in_2 = key in dict1, key in dict2
            if in_1 and not in_2:
                result["only_in_1"].append(f"{parent_xpath1}/{key}")
            elif in_2 and not in_1:
                result["only_in_2"].append(f"{parent_xpath2}/{key}")
            else:
                merge_dicts(
                    result,
                    self._compare_objs(
                        dict1[key],
                        dict2[key],
                        f"{parent_xpath1}/{key}",
                        f"{parent_xpath2}/{key}",
                    ),
                )
        return result

    def _compare_objs(
        self, obj1: Any, obj2: Any, parent_xpath1: str, parent_xpath2: str
    ) -> Dict:
        """ Compare 2 objects using fuzzy logic. """
        result = {"only_in_1": [], "only_in_2": [], "diffs": {}}
        if self.show_equals:
            result["equals"] = {}

        type1, type2 = type(obj1), type(obj2)
        if type1 != type2:
            result["diffs"][parent_xpath1] = (
                f"({type1}) {obj1}",
                (parent_xpath2, f"({type2}) {obj2}"),
            )
        else:
            if isinstance(obj1, dict):
                merge_dicts(
                    result, self._compare_dicts(obj1, obj2, parent_xpath1, parent_xpath2)
                )
            elif isinstance(obj1, (list, tuple)):
                merge_dicts(
                    result, self._compare_lists(obj1, obj2, parent_xpath1, parent_xpath2)
                )
            elif obj1 != obj2:
                result["diffs"][parent_xpath1] = (obj1, (parent_xpath2, obj2))
            elif self.show_equals:
                result["equals"][parent_xpath1] = parent_xpath2
        return result


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """ Merge dict2 into dict1 with extending of lists and int/float summation """
    for key, value in dict2.items():
        if key in dict1 and type(dict1[key]) == type(value):
            if  isinstance(value, dict):
                merge_dicts(dict1[key], value)
            elif isinstance(value, list):
                dict1[key].extend(value)
            elif isinstance(value, (int, float)):
                dict1[key] += value
        else:
            dict1[key] = value
    return dict1


def transform_structure(
    obj: Any, transform_xpaths: Dict[re.Pattern, List[Callable]], xpath: str = ""
):
    """ Apply transfarmation to structure based on xpaths."""
    for pattern, funcs in transform_xpaths.items():
        if pattern.match(xpath):
            for func in funcs:
                obj = func(obj)
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            transformed = transform_structure(value, transform_xpaths, f"{xpath}/{key}")
            if transformed is not _EXCLUDE_NODE_MARKER:
                result[key] = transformed
        return type(obj)(result)
    elif isinstance(obj, (list, tuple)):
        result = []
        for i, value in enumerate(obj):
            transformed = transform_structure(value, transform_xpaths, f"{xpath}[{i}]")
            if transformed is not _EXCLUDE_NODE_MARKER:
                result.append(transformed)
        return type(obj)(result)
    else:
        return obj


################################################################################
__all__ = (
    'n0compare',
    'merge_dicts',
    'transform_structure',
    '_EXCLUDE_NODE_MARKER',
)
################################################################################
