from typing import List
from object.Instrument import Instrument
from object.SongSection import SongSection


class Song:
    def __init__(self, title: str, instruments: List[Instrument],
                 structure: List[SongSection] | None = None):
        self.title = title
        self.instruments = instruments
        self.structure: List[SongSection] = structure or []