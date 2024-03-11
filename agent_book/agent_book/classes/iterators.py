from .main_book import AgentBook


class AgentBookIterator:
    def __init__(self, book: AgentBook):
        self._book = book

    def __iter__(self):
        records = list(self._book.data.values())
        for i in range(0, len(records)):
            yield records[i]


class PaginatedAgentBookIterator:
    def __init__(self, book: AgentBook, page_count: int = 2):
        self._page_count = page_count
        self._book = book

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        if page_count <= 2:
            raise ValueError("Page count have to be greater than 1")
        self._page_count = page_count

    def __iter__(self):
        records = list(self._book.data.values())
        for i in range(0, len(records), self._page_count):
            yield records[i:i + self._page_count]


class ComingUpBirthdayAgentBookIterator(AgentBookIterator):
    def __init__(self, book: AgentBook, after_days: int = 0):
        self.__after_days = after_days
        super().__init__(book)

    def __iter__(self):
        records = list(self._book.data.values())
        for i in range(0, len(records)):
            if records[i].birthday and records[i].birthday.days_to_birthday() == self.__after_days:
                yield records[i]
