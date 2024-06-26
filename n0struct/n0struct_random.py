import typing
import random
import os

try:
    if __system_random:
        pass
except NameError:
    __system_random = random.SystemRandom()

# ******************************************************************************
# ******************************************************************************
def rnd(till_not_included: int) -> int:
    """
    :param till_not_included:
    :return: int [0..till_not_included)
    """
    return __system_random.randrange(0, till_not_included)
# ******************************************************************************
def random_from(from_list: list) -> typing.Any:
    """
    :param from_list:
    :return: from_list[rnd]
    """
    return from_list[rnd(len(from_list))]


################################################################################
__all__ = (
    'rnd',
    'random_from',
)
################################################################################
