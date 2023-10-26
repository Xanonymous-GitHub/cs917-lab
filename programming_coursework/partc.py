from pprint import pprint
from statistics import mean

from model import CryptoRecord
from tester import Tester, use_validated_date
from utils import redirect_to_main


def moving_avg_short(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
    Calculates the short-term moving average of cryptocurrency data.
    
    Args:
        data_ (tuple[CryptoRecord]): The cryptocurrency data.
        start_date (str): The start date in "dd/mm/yyyy" format.
        end_date (str): The end date in "dd/mm/yyyy" format.
        
    Returns:
        dict[int, float]: A dictionary with dates as keys and the calculated short-term moving averages as values.
    """
    return __moving_avg_with_scope(3, data_, start_date, end_date)


def moving_avg_long(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict:
    """
    Calculates the long-term moving average of cryptocurrency data.
    
    Args:
        data_ (tuple[CryptoRecord]): The cryptocurrency data.
        start_date (str): The start date in "dd/mm/yyyy" format.
        end_date (str): The end date in "dd/mm/yyyy" format.
        
    Returns:
        dict[int, float]: A dictionary with dates as keys and the calculated long-term moving averages as values.
    """
    return __moving_avg_with_scope(10, data_, start_date, end_date)

# find_buy_list(short_avg_dict, long_avg_dict) -> dict
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def find_buy_list(short_avg_dict: dict, long_avg_dict: dict) -> dict:
    # replace None with an appropriate return value
    return None


# find_sell_list(short_avg_dict, long_avg_dict) -> dict
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def find_sell_list(short_avg_dict, long_avg_dict):
    # replace None with an appropriate return value
    return None


# crossover_method(data, start_date, end_date) -> [buy_list, sell_list]
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def crossover_method(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> tuple[list, list]:
    # replace None with an appropriate return value
    return None


def __moving_avg_with_scope(scope: int, data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict[int, float]:
    """
        Takes the dataset with the start and end dates,
        and it calculates the moving average with time window `scope` for all the dates within the given range.
        The results are stored in a dictionary with key = date, and value = calculated short average.
        Args:
            data_: the data from a data_source file
            start_date: string in "dd/mm/yyyy" format
            end_date: string in "dd/mm/yyyy" format

        Returns:
            the moving average with time window `scope` for all the dates within the given range
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


def run(data_: tuple[CryptoRecord]) -> None:
    """
    Runs the program, calculating and printing the short-term moving average of cryptocurrency data.
    
    Args:
        data_ (tuple[CryptoRecord]): The cryptocurrency data.
    """
    pprint(moving_avg_short(data_, '01/01/2015', '30/04/2015'))
    Tester(
        'part C',
        data_,
    ).run()

if __name__ == '__main__':
    redirect_to_main('c')
