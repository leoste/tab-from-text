from typing import List
from song.object.NoteProvider import NoteProvider
from song.object.Note import Note


class Segment:
    def __init__(self, title: str, parts: dict[str, list[NoteProvider]], lyrics: str | None = None):
        self.title = title
        self.parts = parts          # instrument name → list of NoteProviders
        self.lyrics = lyrics

    def GetNotesFromSegment(self, instrument_name: str) -> List[Note]:
        notes = []
        for part in self.parts[instrument_name]:
            notes += part.getNotes()
        return notes

    def instrument_names(self) -> list[str]:
        return list(self.parts.keys())