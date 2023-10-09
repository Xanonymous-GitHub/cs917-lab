import secrets
import sys

__all__ = ["randint_safe"]


def randint_safe(a: int, b: int) -> int:
    """
    Generate a secure random integer in the range [a, b], inclusive.

    If 'a' is greater than 'b', the function will automatically swap the two values.

    This function uses the secrets module's randbelow function to generate a
    secure random integer. The generated number is within the half-open range [0, n).
    To provide a number within the range [a, b], we adjust the output of randbelow accordingly.

    Parameters:
    a (int): The lower or upper bound for the range, inclusive.
    b (int): The upper or lower bound for the range, inclusive.

    Returns:
    int: A securely generated random integer within the range [a, b].
    """
    # If 'a' is greater than 'b', swap them
    if a > b:
        a, b = b, a

    # Calculate the length of the range
    range_length = b - a + 1

    # Check if range_length is too large for the system
    if range_length > sys.maxsize:
        raise OverflowError("Range is too large.")

    # Generate a random number in the range 0 to range_length
    random_num = secrets.randbelow(range_length)

    # Adjust the random number to be in the range a to b
    secure_rand_num = a + random_num

    return secure_rand_num
