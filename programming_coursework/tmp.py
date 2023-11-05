import csv

from partb import highest_price, lowest_price, max_volume, best_avg_price, moving_average

if __name__ == '__main__':
    data = []
    with open("./data_source/cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    print(highest_price(None, '01/01/2016', '31/01/2016'))
    print(lowest_price(None, '01/01/2022', '01/01/2022'))
    print(max_volume(None, '01/01/2022', '01/01/2022'))
    print(best_avg_price(None, '01/01/2016', '31/01/2016'))
    print(moving_average(None, '01/01/2016', '31/01/2016'))
