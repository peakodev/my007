from abc import ABC, abstractmethod
from ..classes import Record, AbstractBookIterator


class AbstractMainView(ABC):
    def __init__(self, iterator: AbstractBookIterator):
        self.iterator = iterator

    def render(self):
        self._render_header()
        for record in self.iterator:
            self._render_line(record)
        self._render_footer()

    @abstractmethod
    def _render_line(self, record: Record) -> None:
        pass

    @abstractmethod
    def _render_header(self) -> None:
        pass

    @abstractmethod
    def _render_footer(self) -> None:
        pass


class PrintView(AbstractMainView):
    def _render_line(self, record: Record) -> None:
        print(str(record))

    def _render_header(self) -> None:
        pass

    def _render_footer(self) -> None:
        pass

