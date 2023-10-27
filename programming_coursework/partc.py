from collections.abc import Callable
from statistics import mean
from unittest import TestCase
from pprint import pprint

from model import CryptoRecord
from testdata.partc import strategy_test_data
from tester import Tester, use_validated_date
from utils import redirect_to_main, utc_number_to_date_str


def moving_avg_short(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Calculates the short-term moving average (with a time window of 3) for the given dataset within the specified date range.
    The results are stored in a dictionary where the key is the date (in UTC format) and the value is the calculated short-term average.

    Args:
        data_: Tuple of CryptoRecord objects representing the dataset
        start_date: Start date for the range, in "dd/mm/yyyy" format
        end_date: End date for the range, in "dd/mm/yyyy" format

    Returns:
        Dictionary mapping dates to their corresponding short-term moving average
    """
    return __moving_avg_with_scope(3, data_, start_date, end_date)


def moving_avg_long(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Calculates the long-term moving average (with a time window of 10) for the given dataset within the specified date range.
    The results are stored in a dictionary where the key is the date (in UTC format) and the value is the calculated long-term average.

    Args:
        data_: Tuple of CryptoRecord objects representing the dataset
        start_date: Start date for the range, in "dd/mm/yyyy" format
        end_date: End date for the range, in "dd/mm/yyyy" format

    Returns:
        Dictionary mapping dates to their corresponding long-term moving average
    """
    return __moving_avg_with_scope(10, data_, start_date, end_date)


# FIXME: This function named 'find...list' however it returns a dict. This is confusing.
def find_buy_list(short_avg_dict: dict[int, float], long_avg_dict: dict[int, float]) -> dict[int, bool]:
    """
    Identifies the dates on which a buy action should be performed based on the short-term and long-term moving averages.
    A buy action is recommended when the short-term average crosses upward the long-term average. This means that the short-term average
    at date t-1 is less than or equal to the long-term average at date t-1, but at date t, the short-term average is greater than the long-term average.

    Args:
        short_avg_dict: Dictionary mapping dates to their corresponding short-term moving average
        long_avg_dict: Dictionary mapping dates to their corresponding long-term moving average

    Returns:
        Dictionary mapping dates to a boolean value indicating whether a buy action should be performed (True) or not (False)
    """

    # Skip if there's no records
    if len(short_avg_dict) == 0 or len(long_avg_dict) == 0:
        return {}

    return __find__strategy_decisions(
        short_avg_dict,
        long_avg_dict,
        lambda short_value_t_1, long_value_t_1, short_value_t, long_value_t:
        short_value_t_1 < long_value_t_1 and short_value_t >= long_value_t
    )


# FIXME: This function named 'find...list' however it returns a dict. This is confusing.
def find_sell_list(short_avg_dict: dict[int, float], long_avg_dict: dict[int, float]) -> dict[int, bool]:
    """
    Identifies the dates on which a sell action should be performed based on the short-term and long-term moving averages.
    A sell action is recommended when the short-term average crosses downward the long-term average. This means that the short-term average
    at date t-1 is greater than or equal to the long-term average at date t-1, but at date t, the short-term average is less than the long-term average.

    Args:
        short_avg_dict: Dictionary mapping dates to their corresponding short-term moving average
        long_avg_dict: Dictionary mapping dates to their corresponding long-term moving average

    Returns:
        Dictionary mapping dates to a boolean value indicating whether a sell action should be performed (True) or not (False)
    """

    # Skip if there's no records
    if len(short_avg_dict) == 0 or len(long_avg_dict) == 0:
        return {}

    return __find__strategy_decisions(
        short_avg_dict,
        long_avg_dict,
        lambda short_value_t_1, long_value_t_1, short_value_t, long_value_t:
        short_value_t_1 >= long_value_t_1 and short_value_t < long_value_t
    )


def crossover_method(
        data_: tuple[CryptoRecord],
        start_date: str,
        end_date: str
) -> tuple[[str, ...], [str, ...]]:
    """
    Determines the dates on which buy and sell actions should be performed based on the crossover strategy.
    The crossover strategy involves comparing the short-term and long-term moving averages of the given dataset within the specified date range.
    A buy action is recommended when the short-term average crosses upward the long-term average, and a sell action is recommended when the short-term average crosses downward the long-term average.

    Args:
        data_: Tuple of CryptoRecord objects representing the dataset
        start_date: Start date for the range, in "dd/mm/yyyy" format
        end_date: End date for the range, in "dd/mm/yyyy" format

    Returns:
        Tuple containing two lists of dates (in "dd/mm/yyyy" format): the first list contains the dates on which a buy action should be performed, and the second list contains the dates on which a sell action should be performed.
    """

    short_avg_dict = moving_avg_short(data_, start_date, end_date)
    long_avg_dict = moving_avg_long(data_, start_date, end_date)

    pprint(short_avg_dict)
    pprint(long_avg_dict)

    # FIXME: replace the redundant way to get the buy_list and sell_list

    buy_list = [
        utc_number_to_date_str(date) for date, decision, in find_buy_list(short_avg_dict, long_avg_dict).items()
        if decision == 1
    ]

    sell_list = [
        utc_number_to_date_str(date) for date, decision, in find_sell_list(short_avg_dict, long_avg_dict).items()
        if decision == 1
    ]

    return buy_list, sell_list


def __find__strategy_decisions(
        short_avg_dict: dict[int, float],
        long_avg_dict: dict[int, float],
        decide_func: Callable[[float, float, float, float], bool],
) -> dict[int, int]:
    """
    Apply the decision function to every date in the given dictionaries.
    It holds a sliding window of 2 records, and the decision function is applied to the sliding window.

    Returns:
        all the dates with the decision.
        The key is the date, and the value is 1 when it meets the condition, 0 otherwise.
    """
    short_average_records = sorted(list(short_avg_dict.items()), key=lambda x: x[0])
    long_average_records = sorted(list(long_avg_dict.items()), key=lambda x: x[0])

    # Since we need the previous average record to find the trend, and there's no previous record for the first record,
    # we need to skip the first record. So the decision for the first record is always 0 (False, not sell).
    result: dict[int, int] = {short_average_records[0][0]: 0}

    for t in range(1, len(short_average_records)):
        short_date_t, short_value_t = short_average_records[t]
        short_date_t_1, short_value_t_1 = short_average_records[t - 1]

        long_date_t, long_value_t = long_average_records[t]
        long_date_t_1, long_value_t_1 = long_average_records[t - 1]

        result[short_date_t] = decide_func(short_value_t_1, long_value_t_1, short_value_t, long_value_t)

    return result


def __moving_avg_with_scope(scope: int, data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Calculates the moving average with the given scope.

    Args:
        scope: the scope of the moving average
        data_: the data from a data_source file
        start_date: string in "dd/mm/yyyy" format
        end_date: string in "dd/mm/yyyy" format

    Returns:
        the moving average with the given scope for all the dates within the given range
    """
    if scope < 0:
        raise ValueError('scope should greater than or equal to 0')

    start_date_utc, end_date_utc = use_validated_date(start_date, end_date)

    # Find the first crypto record in the given date range.
    # If nothing found, `first_record` will be `None`.
    first_record = next(
        scoped_records := (record for record in data_ if start_date_utc <= record.the_time <= end_date_utc),
        None
    )

    # It indicates that there's no records in the given date range when `first_record` is `None`.
    if first_record is None:
        return {}

    current_index: int = data_.index(first_record)

    # The reversed clone of `scoped_records`.
    # For our purpose, every calculation requires a record and the previous (moving_avg_scope-1) records in the `data_`.
    # Also, we want to avoid altering memory data by inserting items at the beginning of a list
    # So here we creat a reverse, to let the previous records be added after the end of the list.
    reversed_scoped_records: list[CryptoRecord | None] = list(scoped_records)[::-1]

    # Perform the adding process
    for _ in range(scope - 1):
        current_index -= 1
        # If we encountered the head of `data_`, use `None` to represents a non-existent record.
        reversed_scoped_records.append(data_[current_index] if current_index >= 0 else None)

    result: dict[int, float] = {}

    # Calculates the mean of each sliding window.
    # The sliding window size is expected to `moving_avg_scope`, however, according to the requirement,
    # We want to change the sliding window size when finding insufficient records.
    for i, record in enumerate(reversed_scoped_records[:-scope + 1]):
        slide_window_of_record = []

        for window_index in range(scope):
            if (window_item := reversed_scoped_records[i + window_index]) is not None:
                slide_window_of_record.append(window_item.volume_to / window_item.volume_from)

        result[record.the_time] = round(mean(slide_window_of_record), 2)

    return result


def test_cross_over(tester: TestCase, data_: tuple[CryptoRecord]) -> None:
    for strategy in strategy_test_data[1:2]:
        tester.assertEqual(
            crossover_method(
                data_,
                strategy['start_date'],
                strategy['end_date']
            ),
            (
                strategy['buy_list'],
                strategy['sell_list']
            )
        )


def run(data_: tuple[CryptoRecord]) -> None:
    Tester(
        'part C',
        data_,
        test_cross_over
    ).run()


if __name__ == '__main__':
    redirect_to_main('c')
