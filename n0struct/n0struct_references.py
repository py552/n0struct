import typing
from collections.abc import MutableSet
# ******************************************************************************
# ******************************************************************************
# https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
# https://code.activestate.com/recipes/576694/
class OrderedSet(MutableSet):
    def __init__(self, iterable=None):
        self.end = __end = []
        __end += [None, __end, __end]   # sentinel node for doubly linked list
        self.map = {}                   # __key --> [__key, __prev, __next]
        if iterable is not None:
            self |= iterable

    def __len__(self) -> int:
        return len(self.map)

    def __contains__(self, key) -> bool:
        return key in self.map

    def add(self, key):
        if key not in self.map:
            __end = self.end
            __curr = __end[1]
            __curr[2] = __end[1] = self.map[key] = [key, __curr, __end]

    def discard(self, key):
        if key in self.map:
            key, __prev, __next = self.map.pop(key)
            __prev[2] = __next
            __next[1] = __prev

    def __iter__(self) -> typing.Generator:
        __end = self.end
        __curr = __end[2]
        while __curr is not __end:
            yield __curr[0]
            __curr = __curr[2]

    def __reversed__(self) -> typing.Generator:
        __end = self.end
        __curr = __end[1]
        while __curr is not __end:
            yield __curr[0]
            __curr = __curr[1]

    def pop(self, last=True) -> typing.Any:
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self) -> str:
        if not self:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}({list(self)})"

    def __eq__(self, other) -> bool:
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
# ******************************************************************************
# 2 levels dict:
# initial_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - key1
#       - item3
#       - item4
# Unpack references recursive: bool = True
# unpacked_dict = {key : list(unpack_references(initial_dict, key)) for key in initial_dict}
# unpacked_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - item1
#       - item2
#       - item3
#       - item4
# Remove references recursive: bool = False
# unpacked_dict = {key : list(unpack_references(initial_dict, key), False) for key in initial_dict}
# unpacked_dict:
#   key1:
#       - item1
#       - item2
#   key2:
#       - item3
#       - item4
# ******************************************************************************
def unpack_references(initial_dict: dict, initial_key: str, recursive: bool = True) -> OrderedSet:
    collected_set = OrderedSet() # Not allow to save order with ordinary set
    node = initial_dict[initial_key]
    if isinstance(node, str):
        node = [node]
    if not isinstance(node, list):
        raise TypeError(f"node under {initial_key} must be str or list")

    for item in node:
        if item in initial_dict:    # item == reference (key)
            if recursive:
                collected_set |= unpack_references(initial_dict, item)
        else:                       # item == component dir
            collected_set.add(item)
    return collected_set


################################################################################
__all__ = (
    'OrderedSet',
    'unpack_references',
)
################################################################################
