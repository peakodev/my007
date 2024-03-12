from .main_book import AgentBook
from abc import ABC, abstractmethod


class AbstractBookIterator(ABC):
    def __init__(self, book: AgentBook):
        self._book = book

    @abstractmethod
    def __iter__(self):
        pass


class AgentBookIterator(AbstractBookIterator):
    def __iter__(self):
        records = list(self._book.data.values())
        for i in range(0, len(records)):
            yield records[i]


class PaginatedAgentBookIterator(AbstractBookIterator):
    def __init__(self, book: AgentBook, page_count: int = 2, page: int = 1):
        super().__init__(book)
        self._page_count = page_count
        self._page = page
        self._validate_page_count()
        self._validate_page()

    def _validate_page_count(self):
        if self._page_count < 1:
            raise ValueError("Page count must be greater than 0")

    def _validate_page(self):
        if self._page < 1:
            raise ValueError("Page number must be greater than 0")
        total_pages = (len(self._book.data) + self._page_count - 1) // self._page_count
        if self._page > total_pages:
            raise ValueError(f"Page number exceeds the total number of pages: {total_pages}")

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        self._page_count = page_count
        self._validate_page_count()

    def __iter__(self):
        records = list(self._book.data.values())
        start_index = self._page_count * (self._page - 1)
        end_index = start_index + self._page_count
        for record in records[start_index:end_index]:
            yield record


class ComingUpBirthdayAgentBookIterator(AbstractBookIterator):
    def __init__(self, book: AgentBook, after_days: int = 0):
        super().__init__(book)
        self.__after_days = after_days

    def __iter__(self):
        records = list(self._book.data.values())
        for i in range(0, len(records)):
            if records[i].birthday and records[i].birthday.days_to_birthday() == self.__after_days:
                yield records[i]
