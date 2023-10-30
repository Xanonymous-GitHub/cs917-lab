from collections.abc import Collection
from statistics import mean
from typing import Final
from unittest import TestCase

from enums import MarketTrend
from model import CryptoRecord
from parta import (
    highest_price,
    lowest_price,
    max_volume,
    moving_average,
    best_avg_price
)
from testdata.partd import next_average_test_data, market_trend_test_data
from tester import use_validated_date, Tester
from utils import redirect_to_main


class Investment:
    __data: Final[tuple[CryptoRecord]]
    __start_date: Final[str]
    __end_date: Final[str]

    def __init__(self, data: tuple[CryptoRecord], start_date: str, end_date: str):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__data = data

    @property
    def data(self) -> tuple[CryptoRecord]:
        start_date_utc, end_date_utc = use_validated_date(self.__start_date, self.__end_date)
        return tuple(record for record in self.__data if start_date_utc <= record.the_time <= end_date_utc)

    def highest_price(self) -> float:
        return highest_price(self.__data, self.__start_date, self.__end_date)

    def lowest_price(self) -> float:
        return lowest_price(self.__data, self.__start_date, self.__end_date)

    def max_volume(self) -> float:
        return max_volume(self.__data, self.__start_date, self.__end_date)

    def moving_average(self) -> float:
        return moving_average(self.__data, self.__start_date, self.__end_date)

    def best_avg_price(self) -> float:
        return best_avg_price(self.__data, self.__start_date, self.__end_date)


def predict_next_average(investment: Investment) -> float:
    """
    Predict the average price of the next day.

    Args:
        investment: The investment.

    Returns:
        The predicted average price of the next day.
    """
    data = investment.data
    m, b = __calculate_regression_coefficients(
        [record.the_time for record in data],
        [record.volume_to / record.volume_from for record in data]
    )

    next_day = data[-1].the_time + 86400

    return m * next_day + b


def classify_trend(investment: Investment) -> str:
    """
    Performs a linear regression on the daily high and daily low for a given investment period,
    and determine whether the highs and lows are increasing or decreasing.

    If the daily highs are increasing and the daily lows are decreasing,
    this means that the stock prices have been fluctuating over the time
    between the start and end date of the investment instance, so return ‘volatile’ to result.

    If the daily highs and daily lows are both increasing,
    this likely means that the overall prices are increasing so assign ‘increasing’.
    Likewise, if the daily highs and lows are both decreasing then assign ‘decreasing’.

    We currently only care about these 3 classifications,
    so if the investment do not follow any of the above trends assign ‘other’ to your result string.
    Args:
        investment: The investment.

    Returns:
        The classification of the trend.
    """
    data = investment.data

    trend_of_high, _ = __calculate_regression_coefficients(
        [record.the_time for record in data],
        [record.high for record in data]
    )

    trend_of_low, _ = __calculate_regression_coefficients(
        [record.the_time for record in data],
        [record.low for record in data]
    )

    if trend_of_high > 0 > trend_of_low:
        return MarketTrend.VOLATILE.value

    if trend_of_high > 0 and trend_of_low > 0:
        return MarketTrend.INCREASING.value

    if trend_of_high < 0 and trend_of_low < 0:
        return MarketTrend.DECREASING.value

    return MarketTrend.OTHER.value


def __calculate_regression_coefficients(
        # FIXME: Use Generic type to specify the type of x_series and y_series.
        x_series: Collection[int | float],
        y_series: Collection[int | float],
) -> tuple[float, float]:
    """
    Calculate the regression of the given series.
    This function has verified by numpy.

    Args:
        x_series: The x series.
        y_series: The y series.

    Returns:
        two coefficients of the regression, m and b.
    """

    if (xy_length := len(x_series)) != len(y_series):
        raise ValueError('x_series and y_series must have the same length.')

    if xy_length == 0:
        raise ValueError('x_series and y_series must not be empty.')

    mean_of_x = mean(x_series)
    mean_of_y = mean(y_series)

    x_minus_mean_of_x = tuple(x - mean_of_x for x in x_series)
    y_minus_mean_of_y = tuple(y - mean_of_y for y in y_series)

    m = (
            sum(x * y for x, y in zip(x_minus_mean_of_x, y_minus_mean_of_y)) /
            sum(x * x for x in x_minus_mean_of_x)
    )

    return m, mean_of_y - m * mean_of_x


def test_predict_next_average(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    for test in next_average_test_data:
        investment = Investment(data, test['start_date'], test['end_date'])
        tester.assertEqual(
            predict_next_average(investment),
            test['next_average']
        )


def test_classify_trend(tester: TestCase, data: tuple[CryptoRecord]) -> None:
    for test in market_trend_test_data:
        investment = Investment(data, test['start_date'], test['end_date'])
        tester.assertEqual(
            classify_trend(investment),
            test['classified_trend']
        )


def run(data_: tuple[CryptoRecord]) -> None:
    Tester(
        'part D',
        data_,
        test_predict_next_average,
        test_classify_trend
    ).run()


if __name__ == '__main__':
    redirect_to_main('d')
