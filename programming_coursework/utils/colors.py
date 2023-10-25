from enum import Enum
from typing import Final


class ConsoleColors(Enum):
    """
    This class is used to store the ANSI escape sequences for the console colors.
    """

    # Foreground colors
    BLACK: Final[str] = '\033[30m'
    RED: Final[str] = '\033[31m'
    GREEN: Final[str] = '\033[32m'
    YELLOW: Final[str] = '\033[33m'
    BLUE: Final[str] = '\033[34m'
    MAGENTA: Final[str] = '\033[35m'
    CYAN: Final[str] = '\033[36m'
    WHITE: Final[str] = '\033[37m'

    # Background colors
    BLACK_BACKGROUND: Final[str] = '\033[40m'
    RED_BACKGROUND: Final[str] = '\033[41m'
    GREEN_BACKGROUND: Final[str] = '\033[42m'
    YELLOW_BACKGROUND: Final[str] = '\033[43m'
    BLUE_BACKGROUND: Final[str] = '\033[44m'
    MAGENTA_BACKGROUND: Final[str] = '\033[45m'
    CYAN_BACKGROUND: Final[str] = '\033[46m'
    WHITE_BACKGROUND: Final[str] = '\033[47m'

    # Special
    BOLD: Final[str] = '\033[1m'
    UNDERLINE: Final[str] = '\033[4m'
    RESET: Final[str] = '\033[0m'


class ConsoleColorWrapper:
    """
    This class is used to wrap the ANSI escape sequences for the console colors.
    """

    def __init__(self, color: ConsoleColors) -> None:
        self.color = color

    def __enter__(self) -> None:
        print(self.color.value, end='')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print(ConsoleColors.RESET.value, end='')
