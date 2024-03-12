from .main_view import AbstractMainView
from ..classes import Record

SEPARATOR = '\n{0:-^70s}'.format('-')


class SimpleConsoleView(AbstractMainView):
    def _render_line(self, record: Record) -> None:
        name = str(record.call_sign)
        email = str(record.email) if record.email is not None else 'Not specified'
        phones = ', '.join([str(phone) for phone in record.phones])
        birthday = str(record.days_to_birthday()) if record.birthday is not None else "Not specified"
        print(" | {:15} | {:15} | {:15} | {:15} |".format(name, email, phones, birthday) + SEPARATOR)

    def _render_header(self) -> None:
        print(" | {:15} | {:15} | {:15} | {:15} |".format(
            'Agent call sign',
            'Email',
            'Phones',
            'Days to birthday',
            'Address')
        )

    def _render_footer(self) -> None:
        pass
