from typing import List
from object.NoteProvider import NoteProvider
from object.Note import Note


class Segment:
    def __init__(self, title: str, parts: List[NoteProvider]):
        self.title = title
        self.parts = parts

    def GetNotesFromSegment(self) -> List[Note]:        
        notes = []
        for part in self.parts:
            notes += part.getNotes()
        return notes