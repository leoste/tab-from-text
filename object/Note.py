from object.Chord import Chord
from object.StrumStyle import StrumStyle

# Important! While Segment durations are in 1/8th notes, Note durations are in ticks
TIME_RESOLUTION = 2

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
        return round(duration * TIME_RESOLUTION)