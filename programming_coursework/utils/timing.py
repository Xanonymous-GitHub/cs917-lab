from datetime import datetime, timezone


def date_str_to_utc_number(date_str: str) -> int:
    """
    Convert a date string to utc number.
    :param date_str: string in "dd/mm/yyyy" format
    :return: utc number
    """

    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    return int(date_obj.replace(tzinfo=timezone.utc).timestamp())
