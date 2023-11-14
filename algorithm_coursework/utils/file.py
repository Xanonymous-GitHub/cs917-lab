from os import path

from .path import runtime_path_resolver


def read_file_from(file_path: str, /) -> tuple[str]:
    full_path = path.join(runtime_path_resolver.RUNTIME_DIR, file_path)
    buffer_size = 1024 * 1024
    with open(full_path, 'r', buffering=buffer_size) as file:
        return tuple(line.strip() for line in file)
