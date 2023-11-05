from collections.abc import Callable, Sequence
from functools import wraps
from unittest import TestCase

from constants import DATA_SOURCE_LOCATION
from csv_reader import CryptoCompareCsvDto
from err import DateOutOfRangeError, StartDateAfterEndDateError
from model import CryptoRecord
from parta import (
    highest_price as __highest_price,
    lowest_price as __lowest_price,
    max_volume as __max_volume,
    best_avg_price as __best_avg_price,
    moving_average as __moving_average,
)
from tester import Tester
from utils import redirect_to_main, date_str_to_utc_number


def data_validatable(func: Callable[[Sequence, str, str], float]) -> Callable[[Sequence, str, str], float]:
    @wraps(func)
    def __validate_dates_range(data: tuple[CryptoRecord], *date_strs: str) -> None:
        earliest_time = data[0].the_time
        latest_time = data[-1].the_time

        for date_str in date_strs:
            date_utc = date_str_to_utc_number(date_str)
            if not (earliest_time <= date_utc <= latest_time):
                raise DateOutOfRangeError()

    @wraps(func)
    def __with_validated_data(data_: Sequence, start_date: str, end_date: str) -> float:
        if data_ is None or (isinstance(data_, Sequence) and len(data_) == 0):
            # FIXME: raising FileNotFoundError is not make sense,
            #   as we can't determine whether the file is not found by the length of data_.
            #   However, we expect this error should be raised at this moment for coursework.
            raise FileNotFoundError('dataset not found')

        tmp_dto = CryptoCompareCsvDto(
            'nothing, just for data checking.'
            'We expect data has already read and saved as `data_`.'
        )

        # FIXME: This is a hacky way to validate the data type of data_,
        #   as we expect the data_ may be a `Sequence[dict[str, str], ...]`.
        # In coursework, we expect to check if some of the columns are missing "When we need them",
        # However, this may not be a good idea in real world.
        # So we delegate the responsibility to the dto, and let it raise the error.
        # noinspection PyTypeChecker
        cleaned_data = tmp_dto.to_crypto_records(data_) if not isinstance(data_[0], CryptoRecord) else data_

        __validate_dates_range(cleaned_data, start_date, end_date)

        return func(cleaned_data, start_date, end_date)

    return __with_validated_data


@data_validatable
def highest_price(data: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    return __highest_price(data, start_date, end_date)


@data_validatable
def lowest_price(data: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    return __lowest_price(data, start_date, end_date)


@data_validatable
def max_volume(data: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    return __max_volume(data, start_date, end_date)


@data_validatable
def best_avg_price(data: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    return __best_avg_price(data, start_date, end_date)


@data_validatable
def moving_average(data: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    return __moving_average(data, start_date, end_date)


def test_csv_not_exists(tester: TestCase, _) -> None:
    given_fake_csv_file = 'fake.csv'

    from context import use_crypto_data_set_from

    with tester.assertRaises(FileNotFoundError):
        use_crypto_data_set_from(given_fake_csv_file)


def test_non_existent_csv_column(tester: TestCase, _) -> None:
    given_problem_csv_file = f"{DATA_SOURCE_LOCATION}/cryptocompare_btc_insufficient_column.csv"

    from context import use_crypto_data_set_from

    with tester.assertRaises(KeyError):
        use_crypto_data_set_from(given_problem_csv_file)


def test_invalid_date_string(tester: TestCase, _) -> None:
    with tester.assertRaises(ValueError):
        date_str_to_utc_number('01/00/2021')


def test_date_out_of_range(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    pass
    with tester.assertRaises(DateOutOfRangeError):
        highest_price(data, '01/01/2000', '01/01/2019')
    with tester.assertRaises(DateOutOfRangeError):
        highest_price(data, '01/01/2015', '01/01/2099')

    with tester.assertRaises(DateOutOfRangeError):
        lowest_price(data, '01/01/2000', '01/01/2019')
    with tester.assertRaises(DateOutOfRangeError):
        lowest_price(data, '01/01/2015', '01/01/2099')

    with tester.assertRaises(DateOutOfRangeError):
        max_volume(data, '01/01/2000', '01/01/2019')
    with tester.assertRaises(DateOutOfRangeError):
        max_volume(data, '01/01/2015', '01/01/2099')

    with tester.assertRaises(DateOutOfRangeError):
        best_avg_price(data, '01/01/2000', '01/01/2019')
    with tester.assertRaises(DateOutOfRangeError):
        best_avg_price(data, '01/01/2015', '01/01/2099')

    with tester.assertRaises(DateOutOfRangeError):
        moving_average(data, '01/01/2000', '01/01/2019')
    with tester.assertRaises(DateOutOfRangeError):
        moving_average(data, '01/01/2015', '01/01/2099')


def test_end_date_before_start_date(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    with tester.assertRaises(StartDateAfterEndDateError):
        highest_price(data, '02/01/2019', '01/01/2019')

    with tester.assertRaises(StartDateAfterEndDateError):
        lowest_price(data, '02/01/2019', '01/01/2019')

    with tester.assertRaises(StartDateAfterEndDateError):
        max_volume(data, '02/01/2019', '01/01/2019')

    with tester.assertRaises(StartDateAfterEndDateError):
        best_avg_price(data, '02/01/2019', '01/01/2019')

    with tester.assertRaises(StartDateAfterEndDateError):
        moving_average(data, '02/01/2019', '01/01/2019')


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
