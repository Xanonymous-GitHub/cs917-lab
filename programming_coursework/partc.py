from model import CryptoRecord

# moving_avg_short(data, start_date, end_date) -> dict
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_avg_short(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict:
    # replace None with an appropriate return value
    return None


# moving_avg_long(data, start_date, end_date) -> dict
# data: the data from a data_source file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_avg_long(data_: tuple[CryptoRecord], start_date: str, end_date: str) -> dict:
    # replace None with an appropriate return value
    return None


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


def run(data_: tuple[CryptoRecord]) -> None:
    print('partc!')


if __name__ == '__main__':
    print("=" * 60)
    print("Warning: Please run main.py and specify 'c' to run this part.")
    print("DO NOT directly run this file.")
    print("=" * 60)
    raise NotImplementedError
