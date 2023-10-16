from dataclasses import dataclass

from programming_coursework.utils import ValidatableDataClass, JsonSerializable

__all__ = ["CryptoRecord"]


@dataclass(frozen=True)
class CryptoRecord(ValidatableDataClass, JsonSerializable):
    the_time: int
    high: float
    low: float
    open_amount: float
    close_amount: float
    volume_from: float
    volume_to: float
