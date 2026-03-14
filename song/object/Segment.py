from typing import List, TYPE_CHECKING
from song.object.NoteProvider import NoteProvider
from song.object.Note import Note

if TYPE_CHECKING:
    from song.object.Lyrics import Lyrics


class Segment:
    def __init__(self, title: str, parts: dict[str, list[NoteProvider]],
                 lyrics: "Lyrics | None" = None):
        self.title = title
        self.parts = parts
        self.lyrics = lyrics

    def GetNotesFromSegment(self, instrument_name: str) -> List[Note]:
        notes = []
        for part in self.parts[instrument_name]:
            notes += part.getNotes()
        return notes

    def instrument_names(self) -> list[str]:
        return list(self.parts.keys())