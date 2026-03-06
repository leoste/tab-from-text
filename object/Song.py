from typing import List
from object.Instrument import Instrument


class Song:
    def __init__(self, title: str, instruments: List[Instrument]):
        self.title = title
        self.instruments = instruments