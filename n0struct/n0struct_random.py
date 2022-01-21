import typing
import random
# ******************************************************************************
# ******************************************************************************
def rnd(till_not_included: int) -> int:
    """
    :param till_not_included:
    :return: int [0..till_not_included)
    """
    return int(random.random() * till_not_included)
# ******************************************************************************
def random_from(from_list: list) -> typing.Any:
    """
    :param from_list:
    :return: from_list[rnd]
    """
    return from_list[rnd(len(from_list))]
# ******************************************************************************
# ******************************************************************************
