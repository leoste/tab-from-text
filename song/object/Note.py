from song.object.Chord import Chord
from song.object.StrumStyle import StrumStyle
from object.TimeUtils import convertTimeToTicks

# Important! While Segment durations are in 1/8th notes, Note durations are in ticks
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