from .main_exception import AgentBookException


class EnumValueNotExist(AgentBookException):
    pass


class WrongCountryException(AgentBookException):
    def __init__(self, value):
        super().__init__("Please provide right country name. We support only Україна and USA", value)


class WrongCallSignException(AgentBookException):
    def __init__(self, value):
        super().__init__(
            "Please provide agent call sign with at least 3 characters and without special characters",
            value
        )


class WrongNameLengthException(AgentBookException):
    def __init__(self, field, value=None, max_len=50):
        super().__init__(
            f'Please provide {field} with at least 3 characters and no more than {max_len} characters',
            value
        )


class WrongPhoneException(AgentBookException):
    def __init__(self, value):
        super().__init__("Please provide valid phone number", value)


class WrongEmailException(AgentBookException):
    def __init__(self, value):
        super().__init__("Please provide valid email address", value)


class WrongBirthdayException(AgentBookException):
    def __init__(self, value: str, msg: str = "Please enter birthday in valid format like '1990-12-20'"):
        super().__init__(msg, value)


class CallSignNotFoundException(AgentBookException):
    def __init__(self, value=None):
        super().__init__("Can't find agent call sign in agent book", value)


class TooSmallQueryException(AgentBookException):
    def __init__(self, value):
        super().__init__("Please provide query with at least 3 characters", value)


class CallSignAlreadyExistException(AgentBookException):
    def __init__(self, value, msg: str = "Agent call sign already exist in book, please try to add another call sign"):
        super().__init__(msg, value)
