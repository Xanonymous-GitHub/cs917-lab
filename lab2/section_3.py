from typing import Iterable


def find_smallest_difference(data: Iterable[dict[str, str]], name_key: str, key1: str, key2: str) -> tuple[str, int]:
    difference = {row[name_key]: abs(int(row[key1]) - int(row[key2])) for row in data}
    difference = sorted(difference.items(), key=lambda x: x[1])
    return difference[0]
