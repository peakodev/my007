from ..exceptions import AgentBookException
from abc import ABC, abstractmethod


def validator(setter_func):
    def wrapper(self, value):
        try:
            is_valid = self._validate(value)
        except AgentBookException as e:
            raise e
        # if raise exception is not realized in validate function lets raise it
        if isinstance(is_valid, bool) and not is_valid:
            raise ValueError(f"{self.__class__.__name__}: Invalid value: {value}")

        return setter_func(self, value)

    return wrapper


class Field(ABC):
    def __init__(self, value):
        self._value = None
        self.value = value

    @abstractmethod
    def _validate(self, value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    @validator
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)
