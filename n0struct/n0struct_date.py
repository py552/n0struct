# from typing import Any, Union, Dict, Tuple, List, Set, FrozenSet, NewType, Sequence
import typing
# from mypy_extensions import (Arg, DefaultArg, NamedArg, DefaultNamedArg, VarArg, KwArg)
# from mypy_extensions import Arg

# from datetime import datetime, timedelta, date
import datetime
# ******************************************************************************
# ******************************************************************************
def date_today() -> datetime.datetime:
    """
    :return: today -> date

    https://stackoverflow.com/questions/32517248/what-is-the-difference-between-python-functions-datetime-now-and-datetime-t
        datetime.datetime.now() takes tzinfo as keyword argument but datetime.today() does not take any keyword arguments.
        By default, now() executes with datetime.datetime.now(tz=None)
    """
    return datetime.datetime.today()
# ******************************************************************************
def date_delta(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> datetime.datetime:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> date
    """
    if input_date is None:
        input_date = date_today()
    elif not isinstance(input_date, datetime.datetime):
        return None
    date_delta_ = input_date + datetime.timedelta(days=day_delta)
    month_quotient, month_remainder = divmod(date_delta_.month + month_delta - 1, 12)
    return datetime.datetime(
                            date_delta_.year + month_quotient, month_remainder + 1, date_delta_.day,
                            date_delta_.hour, date_delta_.minute,  date_delta_.second,  date_delta_.microsecond
    )
# ******************************************************************************
def date_timestamp_full(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str 20 characters YYYYMMDDHHMMSSFFFFFF
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%Y%m%d%H%M%S%f")
# ******************************************************************************
def date_timestamp(input_date: typing.Union[datetime.datetime, None] = None) -> str:
    """
    :return: input_date -> str 13 characters YYMMDD_HHMMSS
    """
    # return (timestamp := date_timestamp_full())[2:8] + "_" + timestamp[8:14] # Only for 3.8+
    timestamp = date_timestamp_full(input_date)
    return timestamp[2:8] + "_" + timestamp[8:14]
# ******************************************************************************
def date_iso(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str ISO date format
    """
    return date_delta(input_date, day_delta, month_delta).isoformat(timespec='microseconds')
# ******************************************************************************
def date_yymmdd(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMMDD
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%y%m%d")
# ******************************************************************************
def date_dash_yyyymmdd(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%Y-%m-%d")
# ******************************************************************************
def date_slash_ddmmyyyy(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD/MM/YYYY
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%d/%m/%Y")
# ******************************************************************************
def date_dash_ddmmyyyy(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str DD-MM-YYYY
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%d-%m-%Y")
# ******************************************************************************
def date_yymm(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str YYMM
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%y%m")
# ******************************************************************************
def date_mmyy(input_date: typing.Union[datetime.datetime, None] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> str MMYY
    """
    return date_delta(input_date, day_delta, month_delta).strftime("%m%y")
# ******************************************************************************
def time_hhmmss(input_date: typing.Union[datetime.datetime, None] = None) -> str:
    """
    :param input_date:
    :return: input_date -> str
    """
    return (input_date or date_today()).strftime("%H%M%S")
# ******************************************************************************
def time_colon_hhmmss(input_date: typing.Union[datetime.datetime, None] = None) -> str:
    """
    :param input_date:
    :return: input_date -> str
    """
    return (input_date or date_today()).strftime("%H:%M:%S")
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
def is_date_format(date_str: str, format: str) -> typing.Union[datetime.datetime, bool]:
    try:
        return datetime.datetime.strptime(date_str, format)
    except ValueError:
        return False
        # return None
# ******************************************************************************
def is_date_YYMM(date_str: str) -> typing.Union[datetime.datetime, bool]:
    return is_date_format(date_str, "%y%m")
# ******************************************************************************
def is_date_MMYY(date_str: str) -> typing.Union[datetime.datetime, bool]:
    return is_date_format(date_str, "%m%y")
# ******************************************************************************
def first_day_of_YYMM(date_str: str) -> typing.Union[datetime.datetime, bool]:
    return is_date_YYMM(date_str)
# ******************************************************************************
def last_day_of_YYMM(date_str: str) -> typing.Union[datetime.datetime, bool]:
    if not (date_datetime := is_date_YYMM(date_str)):
        return date_datetime
    return date_delta(date_datetime, month_delta=1) - datetime.timedelta(microseconds=1)
# ******************************************************************************
# ******************************************************************************
