import typing

# ******************************************************************************
class n0str(str):
    def __new__(cls, text):
        return super().__new__(cls, text)

    def normalize_case(self, substrings: typing.Union[str, list, tuple, set, frozenset], ignore_case: bool):
        text = self.lower() if ignore_case else self
        if isinstance(substrings, str):
            substrings = (substrings,)
        if not isinstance(substrings, (list, tuple, set, frozenset)):
            raise TypeError(f"expected str, list, tuple, set, frozenset, but received {type(substrings)}")
        substrings = (substring.lower() for substring in substrings) if ignore_case else substrings
        return text, substrings

    def has_any(self, substrings: typing.Union[str, list, tuple, set, frozenset], ignore_case = False) -> int:
        text, substrings = self.normalize_case(substrings, ignore_case)
        return any(substring in text for substring in substrings)

    def has_all(self, substrings: typing.Union[str, list, tuple, set, frozenset], ignore_case = False):
        text, substrings = self.normalize_case(substrings, ignore_case)
        return all(substring in text for substring in substrings)

    def has_none(self, substrings: typing.Union[str, list, tuple, set, frozenset], ignore_case = False):
        return not self.has_any(substrings, ignore_case)

    def has_count(self, substrings: typing.Union[str, list, tuple, set, frozenset], ignore_case = False) -> int:
        text, substrings = self.normalize_case(substrings, ignore_case)
        return sum(text.count(substring) for substring in substrings)


################################################################################
__all__ = (
    'n0str',
)
################################################################################
