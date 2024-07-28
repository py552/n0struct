import typing
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
def date_only(input_date: datetime.datetime) -> datetime.date:
    return input_date.date()
# ******************************************************************************
def date_delta(input_date: typing.Union[None, datetime.datetime, datetime.date] = None, day_delta: int = 0, month_delta: int = 0) -> datetime.datetime:
    """
    :param day_delta:
    :param month_delta:
    :return: today + day_delta + month_delta -> date
    """
    if not isinstance(input_date, datetime.datetime):
        if isinstance(input_date, datetime.date):
            input_date = datetime.datetime.combine(input_date, datetime.datetime.min.time())
        else:
            return None

    date_delta_ = input_date + datetime.timedelta(days=day_delta)
    month_quotient, month_remainder = divmod(date_delta_.month + month_delta - 1, 12)

    result = datetime.datetime(
                            date_delta_.year + month_quotient, month_remainder + 1, date_delta_.day,
                            date_delta_.hour, date_delta_.minute,  date_delta_.second,  date_delta_.microsecond
    )
    return result

# ******************************************************************************
def date_to_format(input_date: typing.Union[None, datetime.datetime], date_format: str, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param date_format:
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> date_format
    """
    result = date_delta(input_date, day_delta, month_delta)
    if result:
        result = result.strftime(date_format)
    return result
# ******************************************************************************
# LEGACY
# ******************************************************************************
def date_format(date_format: str, input_date: typing.Union[None, datetime.datetime] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    LEGACY
    """
    return date_to_format(input_date or date_today(), date_format, day_delta, month_delta)
# ******************************************************************************
def date_timestamp_full(input_date: typing.Union[None, datetime.datetime] = None, day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str 20 characters YYYYMMDDHHMMSSFFFFFF
    """
    if not input_date:
        input_date = date_today()
    return date_to_format(input_date, "%Y%m%d%H%M%S%f", day_delta, month_delta)
# ******************************************************************************
def date_timestamp(input_date: typing.Union[None, datetime.datetime] = None) -> str:
    """
    :return: input_date -> str 13 characters YYMMDD_HHMMSS
    """
    timestamp = date_timestamp_full(input_date)
    return timestamp[2:8] + "_" + timestamp[8:14]
# ******************************************************************************
def date_iso(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str ISO date format
    """
    return date_delta(input_date, day_delta, month_delta).isoformat(timespec='microseconds')
# ******************************************************************************
def date_yymmdd(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str YYMMDD
    """
    return date_to_format(input_date, "%y%m%d", day_delta, month_delta)
# ******************************************************************************
def date_dash_yyyymmdd(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str YYYY-MM-DD
    """
    return date_to_format(input_date, "%Y-%m-%d", day_delta, month_delta)
# ******************************************************************************
def date_slash_ddmmyyyy(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str DD/MM/YYYY
    """
    return date_to_format(input_date, "%d/%m/%Y", day_delta, month_delta)
# ******************************************************************************
def date_dash_ddmmyyyy(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str DD-MM-YYYY
    """
    return date_to_format(input_date, "%d-%m-%Y" , day_delta, month_delta)
# ******************************************************************************
def date_yymm(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str YYMM
    """
    return date_to_format(input_date, "%y%m", day_delta, month_delta)
# ******************************************************************************
def date_mmyy(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str MMYY
    """
    return date_to_format(input_date, "%m%y", day_delta, month_delta)
# ******************************************************************************
def date_julian(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str JULIAN
    """
    return date_to_format(input_date, "%j", day_delta, month_delta).zfill(3)
# ******************************************************************************
def time_hhmmss(input_date: typing.Union[None, datetime.datetime]) -> str:
    """
    :param input_date:
    :return: (input_date or today) -> str HHMMSS
    """
    return date_to_format(input_date, "%H%M%S")
# ******************************************************************************
def time_colon_hhmmss(input_date: typing.Union[None, datetime.datetime]) -> str:
    """
    :param input_date:
    :return: (input_date or today) -> str HHMMSS
    """
    return date_to_format(input_date, "%H:%M:%S")
# ******************************************************************************
def to_date(input_date_str: typing.Union[None, datetime.datetime], date_format: typing.Union[None, str, list, tuple] = None, raise_exception: bool = False, return_if_wrong_input: typing.Any = None) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str:
    :param date_format:
    :return: input_date_str converted into date_time as date_format
    :return: str -> date
    """
    if not input_date_str or isinstance(input_date_str, datetime.datetime):
        return input_date_str
    elif not isinstance(input_date_str, str):
        raise TypeError(f"{input_date_str=} must be str or datetime")

    if not date_format:
        date_format = (
            "%Y-%m-%d",             # 2020-07-16
            "%d-%m-%Y",             # 16-07-2020
            "%d-%b-%y",             # 16-JUL-20
            "%d-%b-%Y",             # 16-JUL-2020
            "%d.%m.%Y",             # 16.07.2020
            "%m/%d/%Y",             # 07/16/2020

            "%Y-%m-%d %H:%M:%S",    # 2020-07-16 01:23:45
            "%d-%m-%Y %H:%M:%S",    # 16-07-2020 01:23:45
            "%d-%b-%y %H:%M:%S",    # 16-JUL-20 01:23:45
            "%d-%b-%Y %H:%M:%S",    # 16-JUL-2020 01:23:45
            "%d.%m.%Y %H:%M:%S",    # 16.07.2020 01:23:45
            "%m/%d/%Y %I:%M:%S %p", # 07/16/2020 1:23:45 am
        )
    elif isinstance(date_format, str):
        date_format = (date_format,)

    if not isinstance(date_format, (list, tuple)):
        raise TypeError(f"{date_format=} must be str or list/tuple of str")

    # print(f"{input_date_str=}")
    # print(f"{date_format=}")

    for current_date_format in date_format:
        try:
            return_datetime = datetime.datetime.strptime(input_date_str, current_date_format)
            # print(f"{return_datetime=}")
            if "%M" not in current_date_format:
                return_datetime = return_datetime.date()
                # print(f"{return_datetime=}")
            return return_datetime
        except (ValueError, TypeError) as ex:
            # print(f"Exception: {input_date_str=} {current_date_format=}")
            caught_ex = ex
            continue

    # print(f"{raise_exception=}")
    if raise_exception:
        raise caught_ex
    else:
        # print(f"{return_if_wrong_input=}")
        if return_if_wrong_input is None:
            return input_date_str
        else:
            return return_if_wrong_input

# ******************************************************************************
# LEGACY
# ******************************************************************************
def from_date(input_date_str: str, date_format: str) -> typing.Union[None, datetime.datetime, str]:
    """
    LEGACY
    """
    return to_date(input_date_str, date_format)
# ******************************************************************************
def from_ddmmmyy(input_date_str: str) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str: DD-MMM-YY # 16-JUL-20
    :return: str -> date
    """
    return to_date(input_date_str, "%d-%b-%y")  # 16-JUL-20
# ******************************************************************************
def from_yyyymmdd(input_date_str: str) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str: YYYY-MM-DD # 2020-07-16
    :return: str -> date
    """
    return to_date(input_date_str, "%Y-%m-%d")  # 2020-07-16
# ******************************************************************************
def from_ddmmyyyy(input_date_str: str) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str: DD-MM-YYYY # 16-07-2020
    :return: str -> date
    """
    return to_date(input_date_str, "%d-%m-%Y" )  # 16-07-2020
# ******************************************************************************
def is_date_format(input_date_str: str, date_format: str) -> typing.Union[None, datetime.datetime, bool]:
    result = to_date(input_date_str, date_format)
    if isinstance(result, datetime.datetime):
        return result
    else:
        return False
# ******************************************************************************
def is_date_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_to_format(input_date_str, "%y%m")
# ******************************************************************************
def is_date_mmyy(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_to_format(input_date_str, "%m%y")
# ******************************************************************************
def first_day_of_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_yymm(input_date_str)
# ******************************************************************************
def last_day_of_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    date_datetime = is_date_yymm(input_date_str)  # removed walrus operator for compatibility with 3.7
    if not date_datetime:
        return date_datetime
    return date_delta(date_datetime, month_delta=1) - datetime.timedelta(microseconds=1)


################################################################################
__all__ = (
    'date_today',
    'date_only',
    'date_delta',
    'date_to_format',
    'date_format',
    'date_timestamp_full',
    'date_timestamp',
    'date_iso',
    'date_yymmdd',
    'date_dash_yyyymmdd',
    'date_slash_ddmmyyyy',
    'date_dash_ddmmyyyy',
    'date_yymm',
    'date_mmyy',
    'date_julian',
    'time_hhmmss',
    'time_colon_hhmmss',
    'to_date',
    'from_date',
    'from_ddmmmyy',
    'from_yyyymmdd',
    'from_ddmmyyyy',
    'is_date_format',
    'is_date_yymm',
    'is_date_mmyy',
    'first_day_of_yymm',
    'last_day_of_yymm',
    'datetime',
)
################################################################################
