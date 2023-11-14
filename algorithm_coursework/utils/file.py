from collections.abc import Generator
from os import path
from typing import TypeVar

from .path import runtime_path_resolver

# TODO: migrate to 3.12 generic feature.
_R = TypeVar('_R', covariant=True)
_A = TypeVar('_A', covariant=True)

__cached_file_unique_lines: dict[int, frozenset[str]] = dict()


def read_file_lines_from(file_path: str, /) -> Generator[str, None, None]:
    full_path = path.join(runtime_path_resolver.RUNTIME_DIR, file_path)
    buffer_size = 1024 * 1024
    with open(full_path, 'r', buffering=buffer_size) as file:
        for line in file:
            yield line.strip()


def injected_cached_file_unique_lines_from(file_path: str) -> frozenset[str]:
    global __cached_file_unique_lines

    expected_file_cache_hash = hash(file_path)
    if expected_file_cache_hash not in __cached_file_unique_lines:
        __cached_file_unique_lines[expected_file_cache_hash] = frozenset(
            read_file_lines_from(file_path)
        )
    return __cached_file_unique_lines[expected_file_cache_hash]
