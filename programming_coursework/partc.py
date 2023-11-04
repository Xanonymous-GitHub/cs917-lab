from collections.abc import Callable
from statistics import mean
from unittest import TestCase

from model import CryptoRecord
from testdata.partc import strategy_test_data
from tester import Tester, use_validated_date
from utils import redirect_to_main, utc_number_to_date_str


def moving_avg_short(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Takes the dataset with the start and end dates,
    and it calculates the moving average with time window 3 for all the dates within the given range.
    The results are stored in a dictionary with key = date, and value = calculated short average.

    Args:
        data_: the data from a data_source file
        start_date: string in "dd/mm/yyyy" format
        end_date: string in "dd/mm/yyyy" format

    Returns:
        the moving average with time window 3 for all the dates within the given range
    """
    return __moving_avg_with_scope(3, data_, start_date, end_date)


def moving_avg_long(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Takes the dataset with the start and end dates,
    and it calculates the moving average with time window 10 for all the dates within the given range.
    The results are stored in a dictionary with key = date, and value = calculated short average.

    Args:
        data_: the data from a data_source file
        start_date: string in "dd/mm/yyyy" format
        end_date: string in "dd/mm/yyyy" format

    Returns:
        the moving average with time window 10 for all the dates within the given range
    """
    return __moving_avg_with_scope(10, data_, start_date, end_date)


# FIXME: This function named 'find...list' however it returns a dict. This is confusing.
def find_buy_list(short_avg_dict: dict[int, float], long_avg_dict: dict[int, float]) -> dict[int, int]:
    """
    Finds all the dates that we should buy.
    For any date t, if the value of `short_avg_dict` at that date (i.e., date t)
    is “crossing” upward the value of `long_avg_dict`, then we should buy.
    Here, crossing upward means that for the value of `short_avg_dict` at (t-1)
    is still smaller or equal to the value of `long_avg_dict` at (t-1), but at date t,
    the value of `short_avg_dict` already larger than that of `long_avg_dict`.
    Args:
        short_avg_dict: the moving average with time window 3 for all the dates within the given range
        long_avg_dict: the moving average with time window 10 for all the dates within the given range

    Returns:
        all the dates. The key is the date, and the value is 1 when we should buy, 0 otherwise.
        FIXME: The returned type should be `dict[int, bool]` instead of `dict[int, int]`. This is not C.
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
def find_sell_list(short_avg_dict: dict[int, float], long_avg_dict: dict[int, float]) -> dict[int, int]:
    """
    Finds all the dates that we should sell.
    For any date t, if the value of `short_avg_dict` at that date (i.e., date t)
    is “crossing” downward the value of `long_avg_dict`, then we should sell.
    Here, crossing downward means that for the value of `short_avg_dict` at (t-1)
    is still larger or equal to the value of `long_avg_dict` at (t-1), but at date t,
    the value of `short_avg_dict` already smaller than that of `long_avg_dict`.
    Args:
        short_avg_dict: the moving average with time window 3 for all the dates within the given range
        long_avg_dict: the moving average with time window 10 for all the dates within the given range

    Returns:
        all the dates. The key is the date, and the value is 1 when we should sell, 0 otherwise.
        FIXME: The returned type should be `dict[int, bool]` instead of `dict[int, int]`. This is not C.
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
    Given the data, a start date, and an end date (both are string with “dd/mm/yyyy” format),
    return two lists of dates, the first list is the dates that we should buy,
    and the second list is the dates that we should sell.
    Args:
        data_: the data from a data_source file
        start_date: string in "dd/mm/yyyy" format
        end_date: string in "dd/mm/yyyy" format

    Returns:
        two lists of dates, the first list is the dates that we should buy,
        and the second list is the dates that we should sell.
        Note that the dates format is "dd/mm/yyyy".
    """

    short_avg_dict = moving_avg_short(data_, start_date, end_date)
    long_avg_dict = moving_avg_long(data_, start_date, end_date)

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
    # Use `scope` instead of `scope - 1` if we need an extra record to
    # calculate the average of the first record in the strategy list. (will be returned by this function)
    reversed_scoped_records.append(first_record)  # Add the first record to the end of the list.
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

        result[record.the_time] = mean(slide_window_of_record)

    return result


def test_cross_over(tester: TestCase, data_: tuple[CryptoRecord]) -> None:
    for strategy in strategy_test_data:
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
