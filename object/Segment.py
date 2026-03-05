from typing import List
from object.RhythmicChordSpan import RhythmicChordSpan
from object.Note import Note


class Segment:
    def __init__(self, title: str, parts: List[RhythmicChordSpan]):
        self.title = title
        self.parts = parts

    def GetNotesFromSegment(self) -> 'List[Note]':        
        notes = []
        for part in self.parts:
            notes += part.GetNotesFromRhythmicChordSpan()
        return notes