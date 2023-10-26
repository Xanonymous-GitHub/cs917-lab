class __CustomErrorBase(Exception):
    __msg: str

    def __init__(self, msg: str):
        self.__msg = msg

    def __str__(self):
        return self.__msg

    def __repr__(self):
        return self.__msg


class DateOutOfRangeError(__CustomErrorBase):
    def __init__(self, msg: str | None = None):
        super().__init__(
            'Error: date value is out of range'
            f"{'\n' + msg if msg is not None else ''}"
        )


class StartDateAfterEndDateError(__CustomErrorBase):
    def __init__(self, msg: str | None = None):
        super().__init__(
            'Error: end date must be larger than start date'
            f"{'\n' + msg if msg is not None else ''}"
        )
