from testdata.parta import find_highest_price, find_lowest_price, find_max_volume, find_best_average_value, calculate_moving_average

def find_highest_price(data):
    # implementation of the function to find the highest price
    return max(data, key=lambda x: x['price'])

def find_lowest_price(data):
    # implementation of the function to find the lowest price
    return min(data, key=lambda x: x['price'])

def find_max_volume(data):
    # implementation of the function to find the maximum volume
    return max(data, key=lambda x: x['volume'])

def find_best_average_value(data):
    # implementation of the function to find the best average value
    return max(data, key=lambda x: x['average_value'])

def calculate_moving_average_for_data(data):
    # implementation of the function to calculate the moving average for the data
    moving_average = []
    for i in range(len(data)):
        if i < 3:
            moving_average.append(None)
        else:
            moving_average.append(sum([data[j]['price'] for j in range(i-3, i)]) / 3)
    return moving_average

def run_data_analysis(data):
    find_highest_price(data)
    find_lowest_price(data)
    find_max_volume(data)
    find_best_average_value(data)
    calculate_moving_average_for_data(data)
