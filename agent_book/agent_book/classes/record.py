from .book_fields import CallSign, Phone, Birthday, Email
from .address_fields import Address


class Record:

    def __init__(self, call_sign):
        self.__call_sign = CallSign(call_sign)
        self._birthday = None
        self._email = None
        self._address = None
        self.phones = []

    @property
    def call_sign(self) -> CallSign:
        return self.__call_sign

    def update_name(self, call_sign: str):
        self.__call_sign = CallSign(call_sign)

    @property
    def email(self) -> Email:
        return self._email

    @email.setter
    def email(self, email: Email):
        self._email = Email(email)

    @property
    def birthday(self) -> Birthday:
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self._birthday = Birthday(birthday)

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, address: Address):
        self._address = address

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
        return self

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError('Phone not found')

    def edit_phone(self, phone, new_phone):
        self.remove_phone(phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        found_phone = list(filter(lambda ph: ph.value == phone, self.phones))
        return found_phone[0] if len(found_phone) else None

    def is_query_in_phones(self, query) -> bool:
        found_phone = list(filter(lambda ph: query in ph.value, self.phones))
        return bool(len(found_phone))

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()

    def __str__(self):
        ret = f"Agent call sign: {self.call_sign.value}"
        if self.email:
            ret += f", email: {self.email}"
        if self.birthday:
            ret += f", birthday: {str(self.birthday)}, days to birth: {self.days_to_birthday()}"
        if len(self.phones):
            ret += f", {'phones' if len(self.phones) > 1 else 'phone'}: {'; '.join(p.value for p in self.phones)}"
        if self.address:
            ret += f", address: {str(self.address)}"
        return ret
