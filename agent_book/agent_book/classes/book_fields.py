import re
from datetime import date, datetime

from .field import Field, validator
from ..exceptions import WrongBirthdayException, WrongCallSignException, WrongPhoneException, WrongEmailException
from ..enums import DATE_FORMAT


class CallSign(Field):
    def _validate(self, value):
        # Regular expression to match a string with only English or Ukrainian letters, at least 3 characters long
        # English letters: a-zA-Z
        # Ukrainian letters range: \u0400-\u04FF
        pattern = r'^[a-zA-Z\u0400-\u04FFʼ\']{3,}$'
        if not bool(re.search(pattern, value)):
            raise WrongCallSignException(value)


class Phone(Field):
    def _validate(self, value):
        if not bool(re.search(r'\b\d{10}\b', value)):
            raise WrongPhoneException(value)


class Email(Field):
    def _validate(self, value):
        if not bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value)):
            raise WrongEmailException(value)


class Birthday(Field):

    @staticmethod
    def __convert_to_date(date_str: str):
        return datetime.strptime(date_str, DATE_FORMAT).date()

    @Field.value.setter
    @validator
    def value(self, value):
        self._value = self.__convert_to_date(value)

    def _validate(self, value: str):
        try:
            birthday = self.__convert_to_date(value)
        except ValueError:
            raise WrongBirthdayException(value)

        if birthday > date.today():
            raise WrongBirthdayException(value, "Birthday have to be in the past")

    def days_to_birthday(self) -> int:
        today = date.today()
        this_year_birth = date(today.year, self.value.month, self.value.day)
        if this_year_birth < today:
            next_year_birth = date(today.year + 1, self.value.month, self.value.day)
            days_until_birth = (next_year_birth - today).days
        else:
            days_until_birth = (this_year_birth - today).days

        return days_until_birth

    def __str__(self):
        return self._value.strftime(DATE_FORMAT)
