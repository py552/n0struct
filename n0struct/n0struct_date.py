import typing
import datetime
# ******************************************************************************
pyformat_YYYYMMDD   = "%Y-%m-%d"    # 2020-07-16
pyformat_DDMMYYYY   = "%d-%m-%Y"    # 16-07-2020
pyformat_DDMMMYYYY  = "%d-%b-%y"    # 16-JUL-20
pyformat_YYMM       = "%y%m"        # 2007
pyformat_MMYY       = "%m%y"        # 0720
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
    return date_to_format(input_date, pyformat_YYYYMMDD, day_delta, month_delta)
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
    return date_to_format(input_date, pyformat_DDMMYYYY, day_delta, month_delta)
# ******************************************************************************
def date_yymm(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str YYMM
    """
    return date_to_format(input_date, pyformat_YYMM, day_delta, month_delta)
# ******************************************************************************
def date_mmyy(input_date: typing.Union[None, datetime.datetime], day_delta: int = 0, month_delta: int = 0) -> str:
    """
    :param input_date:
    :param day_delta:
    :param month_delta:
    :return: (input_date or today) + day_delta + month_delta -> str MMYY
    """
    return date_to_format(input_date, pyformat_MMYY, day_delta, month_delta)
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
def to_date(input_date_str: str, date_format: str = None) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str:
    :param date_format:
    :return: input_date_str converted into date_time as date_format
    :return: str -> date
    """
    if not input_date_str:
        return input_date_str
    elif not isinstance(input_date_str, str):
        raise TypeError(f"{input_date_str=} must be str")

    if date_format:
        try:
            return datetime.datetime.strptime(input_date_str, date_format)
        except (ValueError, TypeError):
            return input_date_str
    else:
        try:
            return datetime.datetime.strptime(input_date_str, pyformat_YYYYMMDD).date()             # 2020-07-16
        except (ValueError, TypeError):
            try:
                return datetime.datetime.strptime(input_date_str, pyformat_DDMMMYYYY).date()        # 16-JUL-20
            except (ValueError, TypeError):
                try:
                    return datetime.datetime.strptime(input_date_str, pyformat_DDMMYYYY).date()     # 16-07-2020
                except (ValueError, TypeError):
                    try:
                        return datetime.datetime.strptime(input_date_str, "%d.%m.%Y").date()        # 16.07.2020
                    except (ValueError, TypeError):
                        try:
                            return datetime.datetime.strptime(input_date_str, "%m/%d/%Y").date()    # 07/16/2020
                        except (ValueError, TypeError):
                            return input_date_str
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
    return to_date(input_date_str, pyformat_DDMMMYYYY)  # 16-JUL-20
# ******************************************************************************
def from_yyyymmdd(input_date_str: str) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str: YYYY-MM-DD # 2020-07-16
    :return: str -> date
    """
    return to_date(input_date_str, pyformat_YYYYMMDD)  # 2020-07-16
# ******************************************************************************
def from_ddmmyyyy(input_date_str: str) -> typing.Union[None, datetime.datetime, str]:
    """
    :param input_date_str: DD-MM-YYYY # 16-07-2020
    :return: str -> date
    """
    return to_date(input_date_str, pyformat_DDMMYYYY)  # 16-07-2020
# ******************************************************************************
def is_date_format(input_date_str: str, date_format: str) -> typing.Union[None, datetime.datetime, bool]:
    result = to_date(input_date_str, date_format)
    if isinstance(result, datetime.datetime):
        return result
    else:
        return False
# ******************************************************************************
def is_date_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_to_format(input_date_str, pyformat_YYMM)
# ******************************************************************************
def is_date_mmyy(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_to_format(input_date_str, pyformat_MMYY)
# ******************************************************************************
def first_day_of_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    return is_date_yymm(input_date_str)
# ******************************************************************************
def last_day_of_yymm(input_date_str: str) -> typing.Union[None, datetime.datetime, bool]:
    if not (date_datetime := is_date_yymm(input_date_str)):
        return date_datetime
    return date_delta(date_datetime, month_delta=1) - datetime.timedelta(microseconds=1)
# ******************************************************************************
# ******************************************************************************
