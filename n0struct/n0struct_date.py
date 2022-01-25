# from typing import Any, Union, Dict, Tuple, List, Set, FrozenSet, NewType, Sequence
import typing
# from mypy_extensions import (Arg, DefaultArg, NamedArg, DefaultNamedArg, VarArg, KwArg)
# from mypy_extensions import Arg

# from datetime import datetime, timedelta, date
import datetime
# ******************************************************************************
# ******************************************************************************
def date_delta(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> datetime.datetime:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> date
    """
    date_delta_ = (now or datetime.datetime.today()) + timedelta(days=day_delta)
    month_quotient, month_remainder = divmod(date_delta_.month + month_delta - 1, 12)
    date_delta_ = datetime.datetime  (
                            date_delta_.year + month_quotient, month_remainder + 1, date_delta_.day,
                            date_delta_.hour, date_delta_.minute,  date_delta_.second,  date_delta_.microsecond
                            )
    return date_delta_
# ******************************************************************************
def date_now(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str 20 characters YYYYMMDDHHMMSSFFFFFF
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y%m%d%H%M%S%f")
# ******************************************************************************
def timestamp() -> str:
    """
    :return: now -> str 13 characters YYMMDD_HHMMSS
    """
    # return (timestamp := date_now())[2:8] + "_" + timestamp[8:14] # Only for 3.8+
    timestamp = date_now()
    return timestamp[2:8] + "_" + timestamp[8:14]
# ******************************************************************************
def date_iso(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str ISO date format
    """
    return date_delta(now, day_delta, month_delta).isoformat(timespec='microseconds')
# ******************************************************************************
def date_yymmdd(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMMDD
    """
    return date_delta(now, day_delta, month_delta).strftime("%y%m%d")
# ******************************************************************************
def date_yyyymmdd(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_delta(now, day_delta, month_delta).strftime("%Y-%m-%d")
# ******************************************************************************
def date_slash_ddmmyyyy(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD/MM/YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d/%m/%Y")
# ******************************************************************************
def date_ddmmyyyy(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD-MM-YYYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%d-%m-%Y")
# ******************************************************************************
def date_yymm(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMM
    """
    return date_delta(now, day_delta, month_delta).strftime("%y%m")
# ******************************************************************************
def date_mmyy(now: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str MMYY
    """
    return date_delta(now, day_delta, month_delta).strftime("%m%y")
# ******************************************************************************
def from_ddmmmyy(date_str: str) -> typing.Union[datetime.date, str, None]:
    """
    :param date_str: DD-MMM-YY # 16-JUL-20
    :return: str -> date
    """
    try:
        return datetime.datetime.strptime(date_str, "%d-%b-%y").date()  # 16-JUL-20
    except (ValueError, TypeError):
        return date_str
# ******************************************************************************
def from_yyyymmdd(date_str: str) -> typing.Union[datetime.date, str, None]:
    """
    :param date_str: YYYY-MM-DD # 2020-07-16
    :return: str -> date
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()  # 2020-07-16
    except (ValueError, TypeError):
        return date_str
# ******************************************************************************
def from_ddmmyyyy(date_str: str) -> typing.Union[datetime.date, str, None]:
    """
    :param date_str: DD-MM-YYYY # 16-07-2020
    :return: str -> date
    """
    try:
        return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()  # 16-07-2020
    except (ValueError, TypeError):
        return date_str
# ******************************************************************************
def to_date(date_str: str) -> typing.Union[datetime.date, str]:
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()  # 2020-07-16
    except (ValueError, TypeError):
        try:
            return datetime.datetime.strptime(date_str, "%d-%b-%y").date()  # 16-JUL-20
        except (ValueError, TypeError):
            try:
                return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()  # 16-07-2020
            except (ValueError, TypeError):
                try:
                    return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()  # 16.07.2020
                except (ValueError, TypeError):
                    try:
                        return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()  # 07/16/2020
                    except (ValueError, TypeError):
                        return date_str
# ******************************************************************************
def is_date_format(date: datetime.date, format: str) -> bool:
    try:
        datetime.datetime.strptime(date, format)
        return True
    except ValueError:
        return False
# ******************************************************************************
# ******************************************************************************
