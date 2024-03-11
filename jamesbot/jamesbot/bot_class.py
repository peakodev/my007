from agent_notes import AgentNotes, SEPARATOR
from agent_book import AgentBook, AgentBookIterator, ComingUpBirthdayAgentBookIterator
from prompt_toolkit import prompt


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Bot:
    def __init__(self):
        self.__isRunning = True
        self.__book = None
        self.__notes = None
        self.__mode = None
        self.__commands = dict()

    @property
    def running(self):
        return self.__isRunning

    @running.setter
    def running(self, value):
        self.__isRunning = value

    @property
    def notes(self):  # deserialize notes
        if self.__notes is None:
            self.__notes = AgentNotes().deserialize()
        return self.__notes

    @property
    def book(self) -> AgentBook:
        if self.__book is None:
            self.__book = AgentBook().deserialize()
        return self.__book

    @property
    def commands(self) -> dict:
        return self.__commands

    @commands.setter
    def commands(self, commands: dict):
        self.__commands = commands

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    def iterate_book(self):
        max_key_length = max(len(key) for key in self.book.keys())
        print(max_key_length)

        max_name = 0
        max_phone = 0
        max_emai = 0
        for value in self.book.data.items():
            Name = str(value[1].call_sign)
            email = str(value[1].email) if value[1].email is not None else 'Не вказано'
            phones = ', '.join([str(phone) for phone in value[1].phones])
            birthday = str(value[1].days_to_birthday()) if value[1].birthday is not None else "Не вказано"
            max_name = len(max(Name, key=lambda x: len(x))) if len(
                max(Name, key=lambda x: len(x))) > max_name else max_name
            max_phone = len(max(phones, key=lambda x: len(x))) if len(
                max(Name, key=lambda x: len(x))) > max_phone else max_phone
            max_emai = len(max(email, key=lambda x: len(x))) if len(
                max(Name, key=lambda x: len(x))) > max_emai else max_emai

        print(" | {:15} | {:15} | {:15} | {:15} |".format('Agent call sign'.ljust(max_name),
                                                          'Email'.ljust(max_emai),
                                                          'Phones'.ljust(max_phone), 'Days to birthday', 'Address'))
        for value in self.book.data.items():
            Name = str(value[1].call_sign)
            email = str(value[1].email) if value[1].email is not None else 'Не вказано'
            phones = ', '.join([str(phone) for phone in value[1].phones])
            birthday = str(value[1].days_to_birthday()) if value[1].birthday is not None else "Не вказано"

            print(" | {:15} | {:15} | {:15} | {:15} |".format(Name.ljust(max_name), email.ljust(max_emai),
                                                              phones, birthday) + SEPARATOR)

    def birthday_iterate_book(self, days: int = 7):
        print(f'Targets in next {days} days:')
        for i, record in enumerate(ComingUpBirthdayAgentBookIterator(self.book, days)):
            print(f'{i}: {record}')

    def change_mode(self):
        print("Please select:\n")
        print("1. Work with Contacts book")
        print("2. Work with Notes")
        print("3. Sort files")
        print("4. Exit")
        try:
            mode = prompt('>>')
            if mode in ['1', '2', '3', '4']:
                self.mode = mode
                print("Welcome agent, please enter your command, or press Tab to display options")
        except Exception as e:
            print(e)
