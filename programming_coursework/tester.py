import unittest
from collections.abc import Callable
from typing import Final

from model import CryptoRecord
from utils.colors import ConsoleColorWrapper, ConsoleColors, wrap_with_color


class Tester(unittest.TestCase):
    __original_data: Final[tuple[CryptoRecord]]
    __test_func: Final[Callable[[unittest.TestCase, tuple[CryptoRecord]], None]]

    def __init__(
            self,
            original_data: tuple[CryptoRecord],
            test_func: Callable[[unittest.TestCase, tuple[CryptoRecord]], None]
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
