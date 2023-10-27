from datetime import datetime, timezone


def date_str_to_utc_number(date_str: str) -> int:
    """
    Convert a date string to utc number.
    :param date_str: string in "dd/mm/yyyy" format
    :return: utc number
    """

    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError as e:
        # FIXME: this is not a good practice. We should put the error message in the exception.
        print("Error: invalid date value")
        raise e

    return int(date_obj.replace(tzinfo=timezone.utc).timestamp())


def utc_number_to_date_str(utc_number: int) -> str:
    """
    Convert a utc number to date string.
    :param utc_number: utc number
    :return: string in "dd/mm/yyyy" format
    """

    return datetime.fromtimestamp(utc_number, tz=timezone.utc).strftime("%d/%m/%Y")
