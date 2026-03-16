from tabfromtext.song.Chord import Chord
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.util.TimeUtils import convertTimeToTicks

class Note:
    def __init__(self, chord: Chord, duration: int, style: StrumStyle):
        self.chord = chord
        self.duration = duration
        self.style = style

    def __str__(self):
        return f"\n({self.chord}, {self.duration}, {self.style})"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def convertTimeToTicks(duration) -> int:
        return convertTimeToTicks(duration)

    @staticmethod
    def flattenDuration(duration) -> list:
        ticks = convertTimeToTicks(duration)
        return [ticks] + [None] * (ticks - 1)