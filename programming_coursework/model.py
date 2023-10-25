from dataclasses import dataclass

from utils import ValidatableDataClass, JsonSerializable

__all__ = ["CryptoRecord"]


@dataclass(frozen=True)
class CryptoRecord(ValidatableDataClass, JsonSerializable):
    """
    This class represents a record of cryptocurrency data.

    Attributes:
        the_time: epoch timestamp in second (in UTC time zone) – indicates the day
        high: highest BTC price of the day
        low: lowest BTC price of the day
        open_amount: first BTC price of the day
        close_amount: last BTC price of the day
        volume_from: total volume (i.e., the total amount of currency exchanged) of the day in BTC
        volume_to: total (i.e., the total amount of currency exchanged) volume of the day in USD
    """

    the_time: int
    high: float
    low: float
    open_amount: float
    close_amount: float
    volume_from: float
    volume_to: float
