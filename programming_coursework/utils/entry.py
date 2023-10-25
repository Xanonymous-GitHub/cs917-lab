import subprocess
import sys

from .colors import ConsoleColorWrapper, ConsoleColors


def redirect_to_main(origin_module_identifier: str) -> None:
    """
    Redirect process entry to main.py
    :param origin_module_identifier: the module identifier of the origin module
    :return: None
    """

    with ConsoleColorWrapper(ConsoleColors.YELLOW):
        print("=" * 60)
        print(f"Warning: Please run main.py and specify '{origin_module_identifier}' to run this part.")
        print(f"For example, 'python3 main.py {origin_module_identifier}'")
        print("DO NOT directly run this file.")
        print("=" * 60)

    command = [sys.executable, 'main.py', origin_module_identifier]

    # Start the program in a secure way.
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command: {e}", file=sys.stderr)
