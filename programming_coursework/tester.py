import unittest
from collections.abc import Callable
from typing import Final

from err import StartDateAfterEndDateError
from model import CryptoRecord
from utils.colors import ConsoleColorWrapper, ConsoleColors, wrap_with_color
from utils.timing import date_str_to_utc_number

__all__ = ('Tester', None)

_TEST_FUNC_TYPE = Callable[[unittest.TestCase, tuple[CryptoRecord]], None]


class Tester:
    __score_name: Final[str]
    __original_data: Final[tuple[CryptoRecord]]
    __test_funcs: Final[tuple[_TEST_FUNC_TYPE, ...]]

    def __init__(self, scope_name: str, original_data: tuple[CryptoRecord], *test_funcs: _TEST_FUNC_TYPE):
        self.__score_name = scope_name
        self.__original_data = original_data
        self.__test_funcs = test_funcs

    def run(self):
        suite = unittest.TestSuite()
        suite.addTests(
            _UnitTester(self.__original_data, test_func)
            for test_func in self.__test_funcs
        )
        runner = unittest.TextTestRunner()

        print(f'Running {self.__score_name} tests...')
        runner.run(suite)


class _UnitTester(unittest.TestCase):
    __original_data: Final[tuple[CryptoRecord]]
    __test_func: Final[_TEST_FUNC_TYPE]

    def __init__(
            self,
            original_data: tuple[CryptoRecord],
            test_func: _TEST_FUNC_TYPE
    ):
        super().__init__()
        self.__original_data = original_data
        self.__test_func = test_func

    # FIXME: do not use runTest to specify the test function.
    def runTest(self):
        print(f"\n-> {self.__test_func.__name__}...")
        try:
            self.__test_func(self, self.__original_data)
            print(wrap_with_color(ConsoleColors.GREEN, "[ PASSED ]"))
        except Exception as e:
            with ConsoleColorWrapper(ConsoleColors.RED):
                print(e)
            self.fail(
                wrap_with_color(ConsoleColors.RED, f"{self.__test_func.__name__} failed.")
            )


def use_validated_date(start_date: str, end_date: str) -> tuple[int, int]:
    """
    Validate the date and return the UTC number of the date.

    :param start_date: string in "dd/mm/yyyy" format
    :param end_date: string in "dd/mm/yyyy" format
    :return: tuple of start date and end date in UTC number
    """

    start_date_utc = date_str_to_utc_number(start_date)
    end_date_utc = date_str_to_utc_number(end_date)

    if start_date_utc > end_date_utc:
        exception = StartDateAfterEndDateError()
        print(exception)
        raise exception

    return start_date_utc, end_date_utc
