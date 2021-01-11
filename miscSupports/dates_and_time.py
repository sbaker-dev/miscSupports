from datetime import datetime


def invert_dates(dates_list, delimiter="/"):
    """
    Returns dates of type dd-mmy-yyy into yyyymmdd

    :param dates_list: List of dates to invert, or a string of a date to invert
    :type dates_list: list[str] | str

    :param delimiter: The delimiter to split the string into [dd, mm, yyyy]
    :type delimiter: str

    :return: list of inverted dates, or a string of an inverted date
    :rtype: list[str] | str
    """

    if isinstance(dates_list, str):
        day, month, year = [time.zfill(2) for time in dates_list.split(delimiter)]
        return year + month + day

    elif isinstance(dates_list, (list, tuple)):
        split_dates = [[time.zfill(2) for time in date.split(delimiter)] for date in dates_list]
        return [year + month + day for day, month, year in split_dates]

    else:
        raise TypeError(f"invert_dates expects a str, list, or tuple yet found {type(dates_list)}")


def terminal_time():
    """
    A way to remember when you initialised a cell by return the current hour and minute as a string
    """
    return f"{datetime.now().time().hour}:{datetime.now().time().minute}"


