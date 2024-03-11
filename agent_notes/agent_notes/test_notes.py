# import sys
# sys.path.insert(1,'C:\\Work\\team007\\team007\\agent_notes')

from .entities import AgentNotes
from .iterators import PaginatedAgentNotesIterator


# notes1 = AgentNotes()

# notes1.add_note('Ненавижу чай. Это же просто грязная жижа. Больше того, чай — одна из главных причин падения Британской империи.', 'чай', 'причина')
# notes1.add_note('Я обычно замечаю всякие мелочи — например, блондинка девушка или брюнетка.', 'мелочи', 'блондинка')
# notes1.add_note('Почему люди, которые не слушают чужих советов, так любят давать собственные?', 'советы', 'люди')
# notes1.add_note('Власть меняется — ложь остается.', 'власть', 'ложь')
# notes1.add_note('Ради женщины с ножом я готов на все.', 'женщина', 'нож')

# notes1.show_all_notes()
# notes1.serialize()

# notes2 = AgentNotes().deserialize()
# print('\nshow deserialized notes')
# notes2.show_all_notes()

# print('\nremove note by id 4')
# notes2.remove_note('4')
# notes2.show_all_notes()

# print('\nadd note without tag')
# notes2.add_note('Власть меняется — ложь остается.')
# notes2.show_all_notes()

# print('\nadding tags to note, one wrong')
# notes2.add_note_tag('5', 'jhjhgg', 'ложь')
# notes2.show_all_notes()

# print('\nedit note 5 tag')
# notes2.edit_note_tag('5', 'jhjhgg', 'власть')
# notes2.show_all_notes()

# print('\nedit note 4 text and tag')
# notes2.edit_note('4', 'Ради девушки с ножом я готов на все.', 'девушка', 'нож')
# notes2.show_all_notes()

# print('\nprint 2 items per page:')
# for pages in PaginatedAgentNotesIterator(notes2,2):
#     for item in pages:
#         print(item)

# print('\nfind note by tag "девушка"')
# notes2.find_notes('девушка')

def generate_notes():
    notes = AgentNotes()
    notes.add_note(
        'Ненавижу чай. Это же просто грязная жижа. Больше того, чай — одна из главных причин падения Британской империи.',
        'чай', 'причина')
    notes.add_note('Я обычно замечаю всякие мелочи — например, блондинка девушка или брюнетка.', 'мелочи', 'блондинка')
    notes.add_note('Почему люди, которые не слушают чужих советов, так любят давать собственные?', 'советы', 'люди')
    notes.add_note('Власть меняется — ложь остается.', 'власть', 'ложь')
    notes.add_note('Ради женщины с ножом я готов на все.', 'женщина', 'нож')


def test_output():
    notes = AgentNotes().deserialize()
    print('\nshow deserialized notes')
    notes.show_all_notes()

    print('\nremove note by id 4')
    notes.remove_note('4')
    notes.show_all_notes()

    print('\nadd note without tag')
    notes.add_note('Власть меняется — ложь остается.')
    notes.show_all_notes()

    print('\nadding tags to note, one wrong')
    notes.add_note_tag('5', 'jhjhgg', 'ложь')
    notes.show_all_notes()

    print('\nedit note 5 tag')
    notes.edit_note_tag('5', 'jhjhgg', 'власть')
    notes.show_all_notes()

    print('\nedit note 4 text and tag')
    notes.edit_note('4', 'Ради девушки с ножом я готов на все.', 'девушка', 'нож')
    notes.show_all_notes()

    print('\nprint 2 items per page:')
    for pages in PaginatedAgentNotesIterator(notes, 2):
        for item in pages:
            print(item)

    print('\nfind note by tag "девушка"')
    notes.find_notes('девушка')

# bot.notes.commands = {
#     'show_all_notes': bot.notes.show_all_notes, # show all notes
#     'add note': bot.notes.add_note,             # add note with\without tag (note_text: str, *tags: str)
#     'edit note': bot.notes.edit_note,           # edit note (id: Any, note_text: str, *tags: str)
#     'remove note': bot.notes.remove_note,       # remove note by ID  (id: Any)
#     'add note tag': bot.notes.add_note_tag,     # add note tag by ID (id: Any, *new_tag: str)
#     'edit note tag': bot.notes.edit_note_tag,   # edit note tag by ID and tag (id: Any, tag: str, *new_tag: str)
#     'serialize': bot.notes.serialize,           # save notes to file notes.pkl
#     'find_notes': bot.notes.find_notes,         # find text in all notes tags and in notes texts (text: str)
# }
