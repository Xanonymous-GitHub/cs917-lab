from typing import Final

from utils import runtime_path_resolver

RUNTIME_DIR: Final[str] = runtime_path_resolver.RUNTIME_DIR
DATA_SOURCE_LOCATION: Final[str] = f"{RUNTIME_DIR}/data_source"
DEFAULT_DATA_SOURCE_LOCATION: Final[str] = f"{DATA_SOURCE_LOCATION}/cryptocompare_btc.csv"
