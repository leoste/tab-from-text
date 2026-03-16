from abc import ABC, abstractmethod
from typing import List
from tabfromtext.song.Note import Note


class NoteProvider(ABC):
    @abstractmethod
    def getNotes(self) -> List[Note]:
        pass