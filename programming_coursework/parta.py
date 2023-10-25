from statistics import mean

from model import CryptoRecord
from utils import date_str_to_utc_number, redirect_to_main


def highest_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    """
    Given the data, a start date, and an end date (both are string with “dd/mm/yyyy” format),
    return a positive or negative floating point number,
    that is the highest price of the BTC currency in bitcoin within the given period.

    :param data_ the data from a data_source file
    :param start_date string in "dd/mm/yyyy" format
    :param end_date string in "dd/mm/yyyy" format
    :return: the highest price in the given date range
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    return max(
        (record for record in data_ if start_date_utc <= record.the_time <= end_date_utc),
        key=lambda x: x.high
    ).high


def lowest_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    """
    Given the data, a start date, and an end date (both are string with “dd/mm/yyyy” format),
    return a positive or negative floating point number (accurate to 2 decimal places),
    that is the lowest price of the BTC currency in bitcoin within the given period.

    :param data_ the data from a data_source file
    :param start_date string in "dd/mm/yyyy" format
    :param end_date string in "dd/mm/yyyy" format
    :return: the lowest price in the given date range
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    # Fix the float number to 2 decimal places
    return round(
        min(
            (record for record in data_ if start_date_utc <= record.the_time <= end_date_utc),
            key=lambda x: x.low
        ).low, 2
    )


def max_volume(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    """
    Given the data, a start date, and an end date (both are string with “dd/mm/yyyy” format),
    return a floating point number that is the maximal daily amount of exchanged BTC currency of a single day
    within the given period.

    :param data_ the data from a data_source file
    :param start_date string in "dd/mm/yyyy" format
    :param end_date string in "dd/mm/yyyy" format
    :return: the maximum volume in the given date range
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    return max(
        (record for record in data_ if start_date_utc <= record.the_time <= end_date_utc),
        key=lambda x: x.volume_from
    ).volume_from


def best_avg_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    """
    Given the data, a start date, and an end date (both are string with “dd/mm/yyyy” format),
    return the highest daily average price of a single BTC coin in USD within the given period.
    To calculate the average price of a single BTC coin of a day,
    we take the ratio between the total volume in USD and the total volume in BTC (the former divided by the latter).

    :param data_ the data from a data_source file
    :param start_date string in "dd/mm/yyyy" format
    :param end_date string in "dd/mm/yyyy" format
    :return: the average price in the given date range
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    highest_price_record = max(
        (record for record in data_ if start_date_utc <= record.the_time <= end_date_utc),
        key=lambda x: x.volume_to / x.volume_from
    )

    return highest_price_record.volume_to / highest_price_record.volume_from


def moving_average(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    """
    Should return the average BTC currency price over the given period of time (accurate to 2 decimal places).
    The average price of a single day is calculated by :func:`best_avg_price`.

    :param data_ the data from a data_source file
    :param start_date string in "dd/mm/yyyy" format
    :param end_date string in "dd/mm/yyyy" format
    :return: the moving average price in the given date range
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    # Fix the float number to 2 decimal places
    return round(
        mean((
            record.volume_to / record.volume_from
            for record in data_ if start_date_utc <= record.the_time <= end_date_utc
        )), 2
    )


def run(data_: tuple[CryptoRecord]) -> None:
    start_date = '01/01/2015'
    end_date = '31/12/2023'

    print(f"{highest_price.__name__}: {highest_price(data_, start_date, end_date)}")
    print(f"{lowest_price.__name__}: {lowest_price(data_, start_date, end_date)}")
    print(f"{max_volume.__name__}: {max_volume(data_, start_date, end_date)}")
    print(f"{best_avg_price.__name__}: {best_avg_price(data_, start_date, end_date)}")
    print(f"{moving_average.__name__}: {moving_average(data_, start_date, end_date)}")


if __name__ == '__main__':
    redirect_to_main('a')
