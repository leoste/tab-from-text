from typing import List
from tabfromtext.song.Note import Note
from tabfromtext.song.StrumStyle import StrumStyle

class Rhythm:
    def __init__(self, durations: List[int], styles: List[StrumStyle] = [StrumStyle.NORMAL]):
        self.durations = durations
        self.styles = styles

    def flattenDurations(self) -> List:
        durations = []
        for duration in self.durations:
            durations += Note.flattenDuration(duration)
        return durations
    
    def flattenStyles(self) -> List[StrumStyle]:
        styles = []
        for style in self.styles:
            styles += StrumStyle.flattenStyle(style)
        return styles