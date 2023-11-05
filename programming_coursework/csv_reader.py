from csv import DictReader
from platform import python_version
from typing import Final

from model import CryptoRecord

CSV = tuple[dict[str, str], ...]

__all__ = ["CryptoCompareCsvDto"]


class CryptoCompareCsvDto:
    __csv_file_path: Final[str]

    TIME_COL_NAME: Final[str] = 'time'
    HIGH_COL_NAME: Final[str] = 'high'
    LOW_COL_NAME: Final[str] = 'low'
    OPEN_COL_NAME: Final[str] = 'open'
    CLOSE_COL_NAME: Final[str] = 'close'
    VOLUME_FROM_COL_NAME: Final[str] = 'volumefrom'
    VOLUME_TO_COL_NAME: Final[str] = 'volumeto'

    def __init__(self, csv_file_path: str) -> None:
        self.__csv_file_path = csv_file_path

    def __read_csv_rows(self) -> CSV:
        try:
            with open(self.__csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
                if python_version() >= '3.12':
                    # FIXME: Remove this when python 3.12 is well-known and widely used.
                    reader = DictReader[dict[str, str]](file)
                else:
                    reader = DictReader(file)
                return tuple([r for r in reader])
        except FileNotFoundError as e:
            raise FileNotFoundError(
                'Error: the dataset is not found.'
                'Please check if the dataset is in the correct location.'
            ) from e

    def __from_row_to_crypto_compare_record(self, row: dict[str, ...]) -> CryptoRecord:
        try:
            return CryptoRecord(
                the_time=int(row[self.TIME_COL_NAME]),
                high=float(row[self.HIGH_COL_NAME]),
                low=float(row[self.LOW_COL_NAME]),
                open_amount=float(row[self.OPEN_COL_NAME]),
                close_amount=float(row[self.CLOSE_COL_NAME]),
                volume_from=float(row[self.VOLUME_FROM_COL_NAME]),
                volume_to=float(row[self.VOLUME_TO_COL_NAME]),
            )
        except KeyError as e:
            raise KeyError(
                'Error: missing column in the dataset.'
                'Please check if the dataset is valid.'
            ) from e

    def to_crypto_records(self, raw_csv: CSV | None = None) -> tuple[CryptoRecord]:
        _raw_csv: Final[CSV] = raw_csv if raw_csv is not None else self.__read_csv_rows()

        records: Final[list[CryptoRecord]] = []

        for row in _raw_csv:
            records.append(self.__from_row_to_crypto_compare_record(row))

        # Sort the records by the time to enhance the performance of the binary search.
        records.sort(key=lambda x: x.the_time)

        return tuple(records)
