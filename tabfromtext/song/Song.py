from typing import List
from tabfromtext.song.Instrument import Instrument


class Song:
    def __init__(self, title: str, segments: list, description: str | None = None):
        self.title = title
        self.description = description
        self.segments = segments

    @property
    def instruments(self) -> List[Instrument]:
        seen = {}
        for segment in self.segments:
            for name in segment.instrument_names():
                if name not in seen:
                    seen[name] = []
                seen[name].append(segment)

        return [Instrument(name, segs) for name, segs in seen.items()]