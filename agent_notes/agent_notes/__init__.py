#import sys
#sys.path.insert(1,'C:\\Work\\team007\\team007\\agent_notes\\agent_notes')

from .entities import AgentNotes, Note
from .iterators import AgentNotesIterator, PaginatedAgentNotesIterator
from .format import colors, HEADER, SEPARATOR
from .exceptions import WrongNoteIDException, WrongNoteTextException, WrongNoteTagException
from .test_notes import generate_notes, test_output

__all__ = ['AgentNotes', 'Note', 'colors', 'HEADER', 'SEPARATOR', 'AgentNotesIterator', 'PaginatedAgentNotesIterator',
           'generate_notes', 'test_output', 'WrongNoteIDException', 'WrongNoteTextException', 'WrongNoteTagException']