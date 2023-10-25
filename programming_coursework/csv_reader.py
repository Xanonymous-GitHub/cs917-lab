from csv import DictReader
from typing import Final

from model import CryptoRecord

    def __read_csv_rows(self) -> CSV:
        with open(self.__csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = DictReader(file)
            return tuple([r for r in reader])

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
        with open(self.__csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = DictReader(file)
            return tuple([r for r in reader])

    def __from_row_to_crypto_compare_record(self, row: dict[str, ...]) -> CryptoRecord:
        return CryptoRecord(
            the_time=int(row[self.TIME_COL_NAME]),
            high=float(row[self.HIGH_COL_NAME]),
            low=float(row[self.LOW_COL_NAME]),
            open_amount=float(row[self.OPEN_COL_NAME]),
            close_amount=float(row[self.CLOSE_COL_NAME]),
            volume_from=float(row[self.VOLUME_FROM_COL_NAME]),
            volume_to=float(row[self.VOLUME_TO_COL_NAME]),
        )

    def to_crypto_records(self) -> tuple[CryptoRecord]:
        raw_csv: Final[CSV] = self.__read_csv_rows()

        records: Final[list[CryptoRecord]] = []

        for row in raw_csv:
            records.append(self.__from_row_to_crypto_compare_record(row))

        return tuple(records)
