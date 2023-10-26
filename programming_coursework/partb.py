from unittest import TestCase

from constants import DATA_SOURCE_LOCATION
from err import DateOutOfRangeError, StartDateAfterEndDateError
from model import CryptoRecord
from parta import (
    highest_price,
    lowest_price,
    max_volume,
    best_avg_price,
    moving_average
)
from tester import Tester
from utils import redirect_to_main, date_str_to_utc_number


def test_csv_not_exists(tester: TestCase, _) -> None:
    given_fake_csv_file = 'fake.csv'

    # FIXME: DO NOT import any constants from main.py !! This is only for Coursework requirements.
    from main import use_crypto_data_set

    with tester.assertRaises(FileNotFoundError):
        use_crypto_data_set(given_fake_csv_file)


def test_non_existent_csv_column(tester: TestCase, _) -> None:
    given_problem_csv_file = f"{DATA_SOURCE_LOCATION}/cryptocompare_btc_insufficient_column.csv"

    # FIXME: DO NOT import any constants from main.py !! This is only for Coursework requirements.
    from main import use_crypto_data_set

    with tester.assertRaises(KeyError):
        use_crypto_data_set(given_problem_csv_file)


def test_invalid_date_string(tester: TestCase, _) -> None:
    with tester.assertRaises(ValueError):
        date_str_to_utc_number('01/00/2021')


def test_date_out_of_range(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    def validate_date_range(date_str: str) -> None:
        earliest_time = data[0].the_time
        latest_time = data[-1].the_time
        date_utc = date_str_to_utc_number(date_str)
        if not (earliest_time <= date_utc <= latest_time):
            msg = 'Error: date value is out of range'
            print(msg)
            raise DateOutOfRangeError()

    with tester.assertRaises(DateOutOfRangeError):
        validate_date_range('01/01/2000')


def test_end_date_before_start_date(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    with tester.assertRaises(StartDateAfterEndDateError):
        highest_price(data, '01/01/2021', '01/01/2020')

    with tester.assertRaises(StartDateAfterEndDateError):
        lowest_price(data, '01/01/2021', '01/01/2020')

    with tester.assertRaises(StartDateAfterEndDateError):
        max_volume(data, '01/01/2021', '01/01/2020')

    with tester.assertRaises(StartDateAfterEndDateError):
        best_avg_price(data, '01/01/2021', '01/01/2020')

    with tester.assertRaises(StartDateAfterEndDateError):
        moving_average(data, '01/01/2021', '01/01/2020')


def run(data_: tuple[CryptoRecord]) -> None:
    Tester(
        'part B',
        data_,
        test_csv_not_exists,
        test_non_existent_csv_column,
        test_invalid_date_string,
        test_date_out_of_range,
        test_end_date_before_start_date,
    ).run()


if __name__ == '__main__':
    redirect_to_main('b')
