from datetime import date, timedelta
from random import randint, choice

from .enums import DATE_FORMAT, UKRAINIAN_REGIONS
from .exceptions import AgentBookException, CallSignNotFoundException
from .views import PrintView, SimpleConsoleView
from faker import Faker

from .classes import (AgentBook, Record, Address, ComingUpBirthdayAgentBookIterator, AgentBookIterator,
                      PaginatedAgentBookIterator)


def test_change_call_sign(book):
    book.add('nazariy')
    book.add('nazar')

    try:
        book.add('nazar')
    except AgentBookException as inst:
        print(str(inst))

    book.change_call_sign('nazar', 'nazarko')

    try:
        book.change_call_sign('nazarko', 'nazariy')
    except AgentBookException as inst:
        print(str(inst))

    book.add('Вʼячеслав')

    iterate_book_print_view(book)


def iterate_book_print_view(book):
    print(f'Iterate AgentBook items (PrintView):')
    PrintView(AgentBookIterator(book)).render()


def iterate_book_simple_view(book):
    print(f'Iterate AgentBook items (SimpleConsoleView):')
    SimpleConsoleView(AgentBookIterator(book)).render()


def paginate_book(book, count_of_elements=10, page_number=1):
    print(f'\nIterate by {count_of_elements} items per {page_number} page:')
    view = SimpleConsoleView(PaginatedAgentBookIterator(book, count_of_elements, page_number))
    view.render()


def generate_call_sign(book, temp_fake, search_in_book=True, call_sign=None):
    try:
        if not call_sign:
            call_sign = temp_fake.first_name_female() if choice([True, False]) else temp_fake.first_name_male()
        if search_in_book:
            book.find_record(call_sign)
        else:
            return call_sign
    except CallSignNotFoundException:
        return call_sign
    return generate_call_sign(book, temp_fake, search_in_book)


def generate_agent_book(book, count_of_elements, required_birthday=False):
    if count_of_elements == '':
        count_of_elements = 10
    print(f'Generate random phone book with {count_of_elements} elements ...')
    today = date.today()
    def_date = date(year=1990, month=today.month, day=1)
    for _ in range(int(count_of_elements)):
        rec = create_fake_record(book, def_date, required_birthday=required_birthday)
        book.add_record(rec)
        def_date += timedelta(days=1)


def create_fake_record(book, def_date, search_in_book=True, required_birthday=False):
    country = choice(['Україна', 'USA'])
    temp_fake = Faker('uk_UA') if country == 'Україна' else Faker('en_US')
    call_sign = generate_call_sign(book, temp_fake, search_in_book)
    rec = Record(call_sign)
    if required_birthday or choice([True, False]):
        rec.birthday = def_date.strftime(DATE_FORMAT)
    if choice([True, False]):
        rec.email = temp_fake.email()
    rec.add_phone(str(randint(1000000000, 9999999999)))
    if choice([True, False]):
        rec.add_phone(str(randint(1000000000, 9999999999)))
    if choice([True, False]):
        rec.address = Address(
            country,
            choice(UKRAINIAN_REGIONS) if country == 'Україна' else temp_fake.state(),
            temp_fake.city(),
            temp_fake.postcode() if country == 'Україна' else temp_fake.zipcode_plus4(),
            temp_fake.street_address()
        )
    return rec


def birthday_iterate_book(book, days: int = 5):
    print(f'Iterate coming up birthday AgentBook items:')
    PrintView(ComingUpBirthdayAgentBookIterator(book, days)).render()


if __name__ == '__main__':
    mybook = AgentBook()
    test_change_call_sign(mybook)
    generate_agent_book(mybook, 30, required_birthday=True)
    generate_agent_book(mybook, 30, required_birthday=True)
    generate_agent_book(mybook, 40)
    iterate_book_print_view(mybook)
    iterate_book_simple_view(mybook)
    paginate_book(mybook, 12, 1)
    birthday_iterate_book(mybook)
