from collections import UserDict
from pathlib import Path
from .format import colors, wrap, splitted_text, HEADER, SEPARATOR
from .iterators import AgentNotesIterator
from .exceptions import WrongNoteIDException, WrongNoteTextException, WrongNoteTagException
import copy
import pickle


def validate_id(value):
    if isinstance(value, str) and value.isnumeric():
        return True


def validate_note(value):
    if isinstance(value, str) and len(value) >= 3:
        return True


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def validate(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class NoteID(Field):
    def __init__(self, value):
        if not validate_id(value):
            raise WrongNoteIDException(value)
        else:
            super().__init__(value)


class NoteText(Field):
    def __init__(self, value):
        if not validate_note(value):
            raise WrongNoteTextException(value)
        else:
            super().__init__(value)


class NoteTags(Field):
    def __init__(self, value):
        if not validate_note(value):
            raise WrongNoteTagException(value)
        else:
            super().__init__(value)


class Note:
    def __init__(self, note_id: str, note_text: str, *tags: str):
        self.note_text = NoteText(note_text)
        self.note_id = NoteID(note_id)
        if tags:
            self.tags = [NoteTags(tag) for tag in tags]
        else:
            self.tags = []

    def add_tag(self, *tags):
        for tag in tags:
            if not any(obj.value == tag for obj in self.tags):
                tag_obj = NoteTags(tag)
                self.tags.append(tag_obj)

    def find_in_tag(self, string):
        for t in self.tags:
            if string in t.value:
                return ', '.join(t.value for t in self.tags)

    def find_in_text(self, string: str):
        if string in self.note_text.value:
            return self.note_text.value

    def remove_tag(self, tag):
        for t in self.tags:
            if tag == t.value:
                self.tags.remove(t)
            else:
                raise ValueError('Tag not found')

    def edit_tag(self, tag, new_tag):
        self.remove_tag(tag)
        self.add_tag(new_tag)

    def __str__(self):
        txt = wrap(self.note_text.value, 38)
        list = splitted_text(txt)
        colored_id = [colors.RED + str(self.note_id.value) + colors.END]
        colored_tags = ', '.join(colors.GREEN + t.value + colors.END for t in self.tags)
        return f'{colored_id[0]:^14}| {txt[0]:40}| {colored_tags:>20}' + ''.join(list[1:]) + SEPARATOR


class AgentNotes(UserDict):
    def __init__(self, filename=Path(__file__).parent / 'notes.pkl'):
        super().__init__()
        self.filename = filename

    def serialize(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        try:
            with open(self.filename, "rb") as file:
                notes = pickle.load(file)
            return notes
        except FileNotFoundError:
            return self

    def add_note(self, note_text: str, *tags: str):
        id = len(self.data) + 1
        self.data[id] = Note(str(id), note_text, *tags)
        self.serialize()

    def remove_note(self, id):
        self.data.pop(int(id))
        new_data = {}
        for note in self.data.values():
            note.note_id.value = len(new_data) + 1  # change id of note
            new_data[len(new_data) + 1] = note  # change id in self.data.key
        self.data = copy.deepcopy(new_data)
        self.serialize()

    def edit_note(self, id, note_text: str, *tags):
        self.data[int(id)] = Note(id, note_text, *tags)
        self.serialize()

    def edit_note_tag(self, id, tag, *new_tag):
        self.data[int(id)].edit_tag(tag, *new_tag)
        self.serialize()

    def add_note_tag(self, id, *new_tag):
        self.data[int(id)].add_tag(*new_tag)
        self.serialize()

    def find_notes(self, text: str):
        print(HEADER)
        for note in self.data.values():
            tag_obj = note.find_in_tag(text)
            text_obj = note.find_in_text(text)
            if tag_obj:
                txt = wrap(note.note_text.value, 39)
                list = splitted_text(txt)
                t = tag_obj.partition(text)
                colored_tag = t[0] + colors.RED + t[1] + colors.END + t[2]
                print('{0:^5}| {1:40}| {2:20}'.format(note.note_id.value, txt[0], colored_tag) + ''.join(
                    list[1:]) + SEPARATOR)
            elif text_obj:
                txt = wrap(note.note_text.value, 39)
                colored_note = []
                for item in txt:
                    n = item.partition(text)
                    colored_note.append(n[0] + colors.RED + n[1] + colors.END + n[2])
                list = splitted_text(colored_note)
                print('{0:^5}| {1:49}| {2:20}'.format(note.note_id.value, colored_note[0],
                                                      ', '.join(t.value for t in note.tags)) + \
                      ''.join(list[1:]) + SEPARATOR)

    def show_all_notes(self):
        for item in AgentNotesIterator(self):
            print(item)
