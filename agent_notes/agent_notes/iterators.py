from .format import HEADER

class AgentNotesIterator:
    def __init__(self, notes):
        self.__notes = notes

    def __iter__(self):
        data = list(self.__notes.data.values())
        print(HEADER)
        for i in range(0, len(data)):
            yield data[i]

class PaginatedAgentNotesIterator:
    def __init__(self, notes, page_count: int = 1):
        self.__page_count = page_count
        self.__notes = notes

    @property
    def page_count(self):
        return self.__page_count

    @page_count.setter
    def page_count(self, page_count):
        if page_count < 1:
            raise ValueError("Page count have to be greater than 0")
        self.__page_count = page_count

    def __iter__(self):
        data = list(self.__notes.data.values())
        page_number = 1
        for i in range(0, len(data), self.__page_count):
            print(f'\nPage {page_number}:', HEADER)
            page_number += 1
            yield data[i:i+self.__page_count]