class WrongNoteIDException(Exception):
    def __init__(self, value, message="ID should be a numeric string"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongNoteTextException(Exception):
    def __init__(self, value, message="NOTE should be string with at least 3 symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongNoteTagException(Exception):
    def __init__(self, value, message="TAG should be string with at least 3 symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)