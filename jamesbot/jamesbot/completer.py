from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({  # autocompleter for Notes mode
    'show_note_all': None,
    'new_note': None,
    'edit_note': None,
    'remove_note': None,
    'notes_find': None,
    'tag_add':None,
    'help': None,
    'exit': None,
    'generate': None,
    'return': None
})
completer_books = NestedCompleter.from_nested_dict({  # autocompleter for Contacts books mode
    'add': {'Вкажіть ім''я користувача телефон та (не обов''язково) Email та дату народження': None},
    'usr_del': {'Вкажіть "ім''я користувача" (для вилучення)': None},
    'phone_add': {'Вкажіть "ім''я користувача" та номер телефону (для додавання)': None},
    'del_phone': {'Вкажіть "ім''я користувача" та номер телефону (для вилучення)': None},
    'get_phone': {'Вкажіть "ім''я користувача" (для отримання номеру телефону)': None},
    'email': {'Вкажіть "ім''я користувача" та Email (для додавання адреси)': None},
    'upd_phone': {'Вкажіть "ім''я користувача" старий та новый номер телефону': None},
    'show_all': {'Щоб отримати інформацію всіеї телефонної книги, натисніть Enter': None},
    'user_del': {'Вкажіть "ім''я користувача" (для вилучення)': None},
    'birthday': {'Вкажіть "ім''я користувача" та день народження': None},
    'add_address': {"Вкажіть країну, регіон, місто, zip code, адресу": None},
    'bday': {'Вкажіть "ім''я користувача" ': None},
    'find': {'Вкажіть декілька (не меньше 3-х) літер із імені або цифр із номера телефону ': None},
    'help': {'Щоб отримати довідку про команди, натисніть Enter': None},
    'contact_address': {'Вкажіть імя користувача, країну, регіон, потштовий індекс (ZIP), місто та вулицю':None},
    'exit': None
})
completer_files = NestedCompleter.from_nested_dict({  # autocompleter for Contacts books mode
    'organize_files': None,
    'exit': None,
    'help': None,
    'return': None
})