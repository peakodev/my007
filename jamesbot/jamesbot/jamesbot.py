from jamesbot.bot_class import Bot
from xfiles_sorter import organize_files
from prompt_toolkit import prompt
from jamesbot.toolbar import style, bottom_toolbar, rprompt
from jamesbot.completer import completer, completer_books, completer_files
from colorama import init
from agent_book import Address, generate_agent_book

from colorama import Fore, Back, Style

init()


def show_help():  # separated help command for different modes
    available_commands_notes = {
        'add note': "add new note , you can specify tags with #",
        'show notes all': "display all notes",
        'note add tag': 'add a tag to existing note by id',
        'edit note': 'edit existing note by id',
        'remove note': "remove existing note by id",
        'find notes': 'find notes by any matches in text or id',
        'exit': "for exit",
        'help': "show help",
        'return': 'returns you to previous menu'
    }
    available_commands_book = {
        'contact': 'Add a new contact',
        'change contact': 'Change contact name',
        'delete': 'remove contact by name',
        'target': 'Find contact',
        'all targets': 'List all contacts',
        'coming targets': 'Show contact with birthday in next week or specified number of days',
        'address': 'Add address',
        'return': 'returns you to previous menu'
    }
    available_commands_xfiles = {
        'organize files': 'organize files',
        'exit': "for exit",
        'help': "show help",
        'return': 'returns you to previous menu'

    }
    if Bot().mode == '1':
        for key, description in available_commands_book.items():
            print("{:<20} -> {:>}".format(key, description))
    if Bot().mode == '2':
        for key, description in available_commands_notes.items():
            print("{:<20} -> {:>}".format(key, description))
    if Bot().mode == '3':
        for key, description in available_commands_xfiles.items():
            print("{:<20} -> {:>}".format(key, description))


def bot_exit():
    print("Good bye")
    Bot().notes.serialize()
    Bot().book.serialize()
    Bot().running = False


def check_param(num_of_param, plus='+'):
    def check(func):
        if num_of_param >= 10:
            beg = num_of_param // 10
            end = num_of_param % 10
        else:
            beg = num_of_param
            end = beg

        def wrapper(*arg):
            param = tuple(filter(lambda x: x, ' '.join(arg).split(' ')))
            if len(param) < beg or len(param) > end:
                raise ValueError(Fore.LIGHTRED_EX + 'Помилка у кількості параметрів ' + Fore.LIGHTBLUE_EX + \
                                 f'Очікувалося {beg} отримано {len(param)}')

            record = None
            if plus == '+':
                record = Bot().book.find_record(param[0])
                if record == None:
                    raise ValueError('Користувач ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RED + \
                                     "відсутній в телефонній книзі")

            return func(param, record)

        return wrapper

    return check


@check_param(24, '-')
def add_user(param, empty):
    name_user = param[0]
    num_phone = param[1]
    if len(param) == 3:
        birthday = param[2].replace('.', '-')
    else:
        birthday = None

    Bot().book.add(name_user, num_phone, birthday)
    return 'Користувач ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + ' додан до телефонної книги'


@check_param(1)
def del_user(param, empty):
    Bot().book.delete(param[0])
    return 'Користувач ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' вилучен з телефонної книги '


@check_param(3)
def change_phone(param, record):
    record.edit_phone(param[1], param[2])
    return 'Користувачеві ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' телефонний номер ' + Fore.LIGHTBLUE_EX + f' {param[1]} ' + Fore.RESET + \
        ' замінено на ' + Fore.LIGHTBLUE_EX + f' {param[2]} ' + Fore.RESET


@check_param(6)
def add_address(param, record):
    record.address = Address(country=param[1], region=param[2], city=param[3], zip_code=param[4], address_line=param[5])
    return 'Користувачеві ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' додана адреса ' + Fore.LIGHTBLUE_EX + f' {str(record.address)} ' + Fore.RESET


@check_param(2)
def add_phone(param, record):
    record.add_phone(param[1])
    return f'Телефонний номер ' + Fore.LIGHTBLUE_EX + f' {param[1]} ' + Fore.RESET + \
        ' доданий користувачеві ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET


@check_param(2)
def del_phone(param, record):
    record.remove_phone(param[1])
    return f'Телефонний номер ' + Fore.LIGHTBLUE_EX + f'{param[1]}' + Fore.RESET + \
        ' вилучено у користувача ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET


@check_param(2)
def add_birthday(param, record):
    Bot().book.add_birthday(param[0], param[1].replace('.', '-'))
    return 'Користувачеві ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' встановлено день народження ' + Fore.LIGHTBLUE_EX + f' {param[1]} ' + Fore.RESET


@check_param(2)
def add_email(param, record):
    Bot().book.add_email(param[0], param[1])
    return 'Користувачеві ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' встановлено Emall ' + Fore.LIGHTBLUE_EX + f' {param[1]} ' + Fore.RESET


@check_param(1)
def next_birthday(param, record):
    next_day = record.days_to_birthday()
    return 'У користувача ' + Fore.LIGHTBLUE_EX + f' {param[0]} ' + Fore.RESET + \
        ' день народження через ' + Fore.LIGHTBLUE_EX + f' {next_day} днів' + Fore.RESET


@check_param(1, '-')
def find_users(param, record):
    list_user = Bot().book.find(param[0])
    if len(list_user) == 0:
        return Fore.LIGHTYELLOW_EX + 'Користувачів із зазначеними параметрами не знайдено'

    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\n\n')
    for name_user in list_user:
        print(name_user)
    print(Fore.RESET + Style.RESET_ALL + '\n')


'''----- Не доработано ----------------------------------------------------------------'''


def show_all():
    ''' Друк інформації про всіх користувачів'''
    pass


@check_param(1)
def find_phone(param, record):
    phones = Bot().book.get_phones(param[0])

    print(', '.join([str(phone) for phone in phones]))


def input_handler(input_string):
    # separated = input_string.split()
    entered_command = ''
    for i in input_string:
        entered_command += ''.join(i)
        # print(entered_command)
        if entered_command in Bot().commands.keys():
            return entered_command, input_string[len(entered_command):].strip()
    raise ValueError


def command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    if input_string:
        text, *tag = input_string.strip().split('#')
        if text.strip().split(' ', 1)[0].isdigit():
            ids, *text = text.strip().split(' ', 1)  # Does not pars tags for edit note
            user_command(ids, *text)
            return
        user_command(text, *tag)
    else:
        user_command()


def book_command_handler(command, input_string):
    user_command = Bot().commands.get(command)
    if input_string:
        return user_command(*input_string.strip().split(' '))
    else:
        return user_command()


def generate_test_book():
    generate_agent_book(Bot().book, 30, required_birthday=True)
    generate_agent_book(Bot().book, 30, required_birthday=True)
    generate_agent_book(Bot().book, 40)


def bot_start():
    bot = Bot()
    COMMANDS = {
        'help': show_help,
        'exit': bot_exit,
        'return': bot.change_mode,

        'add': add_user,  # 22.02.24
        'usr_del': del_user,
        'phone_add': add_phone,
        'del_phone': del_phone,
        'get_phone': find_phone,
        'upd_phone': change_phone,
        'show_all': bot.iterate_book,
        'user_del': del_user,
        'birthday': add_birthday,
        'email': add_email,
        'bday': next_birthday,
        'find': find_users,
        'contact_address': add_address,

        'new_note': bot.notes.add_note,
        'show_note_all': bot.notes.show_all_notes,
        'tag_add': bot.notes.add_note_tag,
        'edit_note': bot.notes.edit_note,
        'remove_note': bot.notes.remove_note,
        'notes_find': bot.notes.find_notes,

        'organize_files': organize_files,
        'generate_test_book': generate_test_book
    }
    bot.commands = COMMANDS
    bot.change_mode()  # Asking user to choose mode
    while bot.running:
        if bot.mode == '2':  # Notes loop
            try:
                user_input = prompt(">>", completer=completer, bottom_toolbar=bottom_toolbar, style=style,
                                    complete_while_typing=True)  # Removed right toolbar
                user_command, input_string = input_handler(str(user_input))
                # print(len(input_string))
                command_handler(user_command, input_string)
            except Exception as e:
                print(e)
        elif bot.mode == '1':  # Books loop
            # try:
            user_input = prompt(">>", completer=completer_books, bottom_toolbar=bottom_toolbar, style=style,
                                complete_while_typing=True)
            user_command, input_string = input_handler(str(user_input))
            # print('You entered command:', user_command, "with such params", input_string)
            result = book_command_handler(user_command, input_string)
            if result:
                print(result)

        # except Exception as e:
        #     print(e)
        elif bot.mode == '3':
            try:
                user_input = prompt(">>", completer=completer_files, bottom_toolbar=bottom_toolbar, style=style,
                                    complete_while_typing=True)  # Removed right toolbar
                user_command, input_string = input_handler(str(user_input))
                # print(len(input_string))
                command_handler(user_command, input_string)
            except Exception as e:
                print(e)
        elif bot.mode == '4':
            bot_exit()
        else:
            bot.change_mode()


if __name__ == "__main__":
    bot_start()
