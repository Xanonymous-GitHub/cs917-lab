import csv

from section_3 import find_smallest_difference

CSV = tuple[dict[str, str]]


def start():
    with open("data_source/football.csv", "r") as f:
        reader = csv.DictReader(f)
        data: CSV = tuple([r for r in reader])
        ans = find_smallest_difference(data, "Team", "Goals", "Goals Allowed")
        print(ans)


if __name__ == '__main__':
    start()
