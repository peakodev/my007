from pathlib import Path

from agent_notes import AgentNotes, SEPARATOR
from agent_book import AgentBook, AgentBookIterator, ComingUpBirthdayAgentBookIterator, SimpleConsoleView
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
            self.__notes = AgentNotes(Path(__file__).parent.parent / 'notes.pkl').deserialize()
        return self.__notes

    @property
    def book(self) -> AgentBook:
        if self.__book is None:
            self.__book = AgentBook(Path(__file__).parent.parent / 'book.pkl').deserialize()
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
        SimpleConsoleView(AgentBookIterator(self.book)).render()

    def birthday_iterate_book(self, days: int = 7):
        print(f'Targets in next {days} days:')
        SimpleConsoleView(ComingUpBirthdayAgentBookIterator(self.book, days)).render()

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
