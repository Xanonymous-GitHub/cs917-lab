import __main__
import os
from typing import Final

__all__ = ["runtime_path_resolver"]


class __Path:
    """Path class to provide the current program's main entrypoint runtime directory.

    This class is intended for internal use only.

    Attributes:
        RUNTIME_DIR: A final string representing the runtime directory path.
                     It's initialized at the start of the program.

    Usage:
        To get the runtime directory, use: _Path.RUNTIME_DIR
    """

    # Initialize RUNTIME_DIR at the time of import
    RUNTIME_DIR: Final[str]

    def __init__(self):
        current_dir: Final[str] = os.path.dirname(os.path.abspath(__main__.__file__))

        # This is needed to run the script from the root directory
        os.chdir(f"{current_dir}/")

        # Get the runtime directory path
        self.RUNTIME_DIR = os.getcwd()

        # Add the current directory to the PYTHONPATH
        self.__manually_add_python_path()

    def __manually_add_python_path(self):
        """Add the current directory to the PYTHONPATH.

        This is needed to run the script from the root directory.
        """
        import sys
        sys.path.append(self.RUNTIME_DIR)


runtime_path_resolver: Final[__Path] = __Path()
