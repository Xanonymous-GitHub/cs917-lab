from model import CryptoRecord


# highest_price(data, start_date, end_date) -> float
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def highest_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    # replace None with an appropriate return value
    return None


# lowest_price(data, start_date, end_date) -> float
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def lowest_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    # replace None with an appropriate return value
    return None


# max_volume(data, start_date, end_date) -> float
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def max_volume(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    # replace None with an appropriate return value
    return None


# best_avg_price(data, start_date, end_date) -> float
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def best_avg_price(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    # replace None with an appropriate return value
    return None


# moving_average(data, start_date, end_date) -> float
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_average(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> float:
    # replace None with an appropriate return value
    return None


def run(data_: tuple[CryptoRecord]) -> None:
    print(data_)


if __name__ == '__main__':
    print("=" * 60)
    print("Warning: Please run main.py and specify 'a' to run this part.")
    print("DO NOT directly run this file.")
    print("=" * 60)
    raise NotImplementedError
