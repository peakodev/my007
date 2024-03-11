import pickle
from collections import UserDict
from pathlib import Path
from .record import Record
from .book_fields import Phone
from .address_fields import Address
from ..exceptions import TooSmallQueryException, CallSignNotFoundException, CallSignAlreadyExistException


class AgentBook(UserDict):

    def __init__(self, dump_file_name=Path(__file__).parent / 'book.pkl'):
        super().__init__()
        self.dump_file_name = dump_file_name

    def serialize(self):
        with open(self.dump_file_name, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        try:
            with open(self.dump_file_name, "rb") as file:
                obj = pickle.load(file)
            return obj
        except FileNotFoundError:
            return AgentBook(self.dump_file_name)

    def add(self, call_sign, phone: str = None, email: str = None, birthday: str = None) -> Record:
        if self.data.get(call_sign, None):
            raise CallSignAlreadyExistException(call_sign)
        record = Record(call_sign)
        if birthday:
            record.birthday = birthday
        if email:
            record.email = email
        if phone:
            record.add_phone(phone)
        self.add_record(record)
        return record

    def change_call_sign(self, call_sign, new_call_sign):
        record = self.find_record(call_sign)
        if self.data.get(new_call_sign, None):
            msg = f"You cant change call sign '{call_sign}' to '{new_call_sign}', because the last one is exist in book"
            raise CallSignAlreadyExistException(value=new_call_sign, msg=msg)
        self.data.pop(call_sign, None)
        record.update_name(new_call_sign)
        self.add_record(record)

    def add_record(self, record: Record) -> None:
        if self.data.get(record.call_sign.value):
            raise CallSignAlreadyExistException(value=record.call_sign.value)
        self.data[record.call_sign.value] = record

    def delete(self, call_sign):
        self.find_record(call_sign)
        self.data.pop(call_sign, None)

    def add_phone(self, call_sign, phone):
        record = self.find_record(call_sign)
        record.add_phone(str(phone))

    def add_birthday(self, call_sign: str, birthday: str):
        record = self.find_record(call_sign)
        record.birthday = str(birthday)

    def add_email(self, call_sign: str, email: str):
        record = self.find_record(call_sign)
        record.email = str(email)

    def add_address(self, call_sign: str, address: Address):
        record = self.find_record(call_sign)
        record.address = address

    def get_phones(self, call_sign) -> list[Phone]:
        record = self.find_record(call_sign)
        return record.phones

    def find_record(self, call_sign) -> Record:
        record = self.data.get(call_sign, None)
        if not record:
            raise CallSignNotFoundException(call_sign)
        return record

    def find(self, query):
        if len(query) < 3:
            raise TooSmallQueryException(query)
        in_call_signs = [call_sign for call_sign in self.data.keys() if query.lower() in call_sign.lower()]
        in_phones = [record.call_sign.value for record in self.data.values() if record.is_query_in_phones(query)]
        all_call_signs = list(set(in_call_signs + in_phones))
        return [self.data.get(key) for key in all_call_signs] if len(all_call_signs) > 0 else []
