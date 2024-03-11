from faker import Faker
from random import randint, choice
from datetime import date, timedelta
from agent_book import (AgentBook, Record, PaginatedAgentBookIterator, Address, DATE_FORMAT,
                        AgentBookException, UKRAINIAN_REGIONS, CallSignNotFoundException,
                        AgentBookIterator, ComingUpBirthdayAgentBookIterator)

book = AgentBook()


def test_change_call_sign():
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

    iterate_book()


def iterate_book():
    print(f'Iterate AgentBook items:')
    for i, record in enumerate(AgentBookIterator(book)):
        print(f'{i}: {record}')


def paginate_book(count_of_elements=3):
    # Iterate by 3 items per page
    print(f'\nIterate by {count_of_elements} items per page:')
    for i, records in enumerate(PaginatedAgentBookIterator(book, count_of_elements)):
        print(f"Portion {i + 1}: ")
        for pi in range(len(records)):
            print(f"{records[pi]}")


def generate_call_sign(temp_fake, search_in_book=True, call_sign=None):
    try:
        if not call_sign:
            call_sign = temp_fake.first_name_female() if choice([True, False]) else temp_fake.first_name_male()
        if search_in_book:
            book.find_record(call_sign)
        else:
            return call_sign
    except CallSignNotFoundException:
        return call_sign
    return generate_call_sign(temp_fake, search_in_book)


def generate_agent_book(count_of_elements, required_birthday=False):
    if count_of_elements == '':
        count_of_elements = 10
    print(f'Generate random phone book with {count_of_elements} elements ...')
    today = date.today()
    def_date = date(year=1990, month=today.month, day=1)
    for _ in range(int(count_of_elements)):
        rec = create_fake_record(def_date, required_birthday=required_birthday)
        book.add_record(rec)
        def_date += timedelta(days=1)


def create_fake_record(def_date, search_in_book=True, required_birthday=False):
    country = choice(['Україна', 'USA'])
    temp_fake = Faker('uk_UA') if country == 'Україна' else Faker('en_US')
    call_sign = generate_call_sign(temp_fake, search_in_book)
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


def birthday_iterate_book(days: int = 5):
    print(f'Iterate coming up birthday AgentBook items:')
    for i, record in enumerate(ComingUpBirthdayAgentBookIterator(book, days)):
        print(f'{i}: {record}')


if __name__ == '__main__':
    test_change_call_sign()
    generate_agent_book(30, required_birthday=True)
    generate_agent_book(30, required_birthday=True)
    generate_agent_book(40)
    paginate_book(12)
    birthday_iterate_book()
