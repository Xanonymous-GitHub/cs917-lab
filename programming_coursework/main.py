"""
Originate from self-implemented project few years ago.
https://github.com/Xanonymous-GitHub/MultimediaX/blob/main/main.py
// FIXME: Re-organize project file structure and address the top level package not found issue.
"""

import importlib
import sys

from context import use_default_crypto_data_set
from model import CryptoRecord
from utils.colors import ConsoleColorWrapper, ConsoleColors

PACKAGE_ENTRY_POINT_NAME = 'run'
SUBPACKAGE_PREFIX = 'part'


class Importer:
    def __init__(self, subpackage_serial: str):
        # user may provide a subpackage_serial.
        self.subpackage_serial = subpackage_serial

        # name is the package name, but we don't sure that it exists.
        self.name = f"{SUBPACKAGE_PREFIX}{self.subpackage_serial}"

        # because we don't sure that the package is actually exists, so we set the target package to None.
        self.package = None

    def __enter__(self):
        try:
            # try to load the package using the name provided when constructing.
            self.package = importlib.import_module(self.name)
        except ModuleNotFoundError:
            pass  # we ignore this exception because it will be handled when we call the 'run' method.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # module resources will be automatically released after used.

    def __str__(self):
        return str(self.name)

    def run(self, data_: tuple[CryptoRecord]):
        # if package is truly exists,
        if self.package:
            # if user provide the sub package entry function suffix serial number,
            if self.subpackage_serial:
                try:
                    # try to call the sub package entry function.
                    getattr(self.package, PACKAGE_ENTRY_POINT_NAME)(data_)
                except Exception as e:
                    with ConsoleColorWrapper(ConsoleColors.RED):
                        print(f'Exceptions found when running exercise {self.subpackage_serial}.')
                        print(e)
                finally:
                    sys.exit(0)

        else:
            with ConsoleColorWrapper(ConsoleColors.RED):
                print(self.name, 'not found. Only (a, b, c or d)')
            sys.exit(1)


def main(data_: tuple[CryptoRecord]):
    # if using cli arguments to specify target function,
    if len(sys.argv) > 1:
        # get exercise name.
        exercise_name: str = sys.argv[1]

    # if cli arguments not specified, try to ask user after running.
    else:
        # get everything from user input and split into a list.
        requested_exercise_name = input(
            'Please tell me which exercise you want to run, '
            '(a, b, c or d) ?: '
        ).split()

        # if user not provide the name of exercise to be run, show error message.
        if len(requested_exercise_name) == 0:
            with ConsoleColorWrapper(ConsoleColors.YELLOW):
                print('exercise name not provided, aborted.')
            sys.exit(0)

        exercise_name = requested_exercise_name[0]

    # use initialized self-defined contextmanager 'Importer' to execute the target function.
    with Importer(exercise_name) as pkg:
        # call the pre-defined entry interface method of the contextmanager.
        pkg.run(data_)
        sys.exit(0)


if __name__ == '__main__':
    data = use_default_crypto_data_set()

    try:
        main(data)
    except KeyboardInterrupt:
        with ConsoleColorWrapper(ConsoleColors.CYAN):
            print('\nProgram interrupted.')
        sys.exit(0)
