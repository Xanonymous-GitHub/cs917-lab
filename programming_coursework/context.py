import inspect
from collections.abc import Callable
from typing import TypeVar, Final, Any

from constants import DEFAULT_DATA_SOURCE_LOCATION
from csv_reader import CryptoCompareCsvDto
from model import CryptoRecord

# TODO: migrate to 3.12 generic feature.
_R = TypeVar('_R', covariant=True)

FRIEND_CONTEXT_MODULE_NAMES: Final[frozenset[str]] = frozenset({
    'parta',
    'partb',
    'partc',
    'partd',
})


def expect_illegal_data_type(
        func: Callable[[tuple[CryptoRecord], str, str], _R]
) -> Callable[[Any, str, str], _R]:
    def __get_original_module_name() -> str:
        # noinspection PyUnresolvedReferences
        return func.__module__

    def __context_applied_func(given_data: Any, start_date: str, end_date: str) -> _R:
        if (
                isinstance(given_data, tuple)
                and len(given_data) > 0
                and isinstance(given_data[0], CryptoRecord)
        ):
            return func(given_data, start_date, end_date)

        original_module_name = __get_original_module_name()

        # This operation can not be extracted to a function, because the caller_module_name
        # is the module name of the caller of the caller of this function.
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        caller_module_name = caller_module.__name__ if caller_module is not None else None

        if original_module_name != caller_module_name:
            if caller_module_name not in FRIEND_CONTEXT_MODULE_NAMES:
                data = use_default_crypto_data_set()
                return func(data, start_date, end_date)

        return func(given_data, start_date, end_date)

    return __context_applied_func


def use_crypto_data_set_from(data_source_location: str) -> tuple[CryptoRecord]:
    dto = CryptoCompareCsvDto(data_source_location)
    return dto.to_crypto_records()


def use_default_crypto_data_set() -> tuple[CryptoRecord]:
    return use_crypto_data_set_from(DEFAULT_DATA_SOURCE_LOCATION)
