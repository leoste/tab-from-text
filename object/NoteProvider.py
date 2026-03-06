from abc import ABC, abstractmethod
from typing import List
from object.Note import Note


class NoteProvider(ABC):
    @abstractmethod
    def getNotes(self) -> List[Note]:
        pass