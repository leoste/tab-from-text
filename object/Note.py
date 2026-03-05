from typing import List
from object.Chord import Chord
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.RhythmicChordSpan import RhythmicChordSpan
TIME_RESOLUTION = 2
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
    def GetNotesFromSegment(segment: Segment) -> 'List[Note]':        
        notes = []
        for part in segment.parts:
            notes += Note.GetNotesFromRhythmicChordSpan(part)
        return notes
    
    @staticmethod
    def GetNotesFromRhythmicChordSpan(part: RhythmicChordSpan) -> 'List[Note]':
        notes = []
        chords = Note.flattenChordSpans(part)
        durations = Note.flattenRhythmDurations(part)
        styles = Note.flattenStyles(part)
        
        for index, chord in enumerate(chords):
            duration = durations[index % len(durations)]
            if duration is not None:
                style = styles[index % len(styles)]
                
                if style == StrumStyle.NO_HIT:
                    notes += [Note(None, duration, style)]
                else:
                    notes += [Note(chord, duration, style)]
            else:
                notes += [Note(None, None, None)]
        return notes
            
    @staticmethod
    def flattenChordSpans(part: RhythmicChordSpan) -> 'List[Chord]':
        chords = []
        for chordSpan in part.chordSpans:
            chords += [chordSpan.chord] * Note.convertTimeToTicks(chordSpan.duration)
        return chords
    
    @staticmethod
    def flattenRhythmDurations(part: RhythmicChordSpan) -> 'List[int]':
        durations = []
        for duration in part.rhythm.durations:
            ticks = Note.convertTimeToTicks(duration)
            durations += [ticks] + [None] * (ticks - 1)
        return durations

    @staticmethod
    def flattenStyles(part: RhythmicChordSpan) -> 'List[StrumStyle]':
        styles = []
        for style in part.rhythm.styles:
            ticks = Note.convertTimeToTicks(1)  # each style entry covers one eighth note = TIME_RESOLUTION ticks
            styles += [style] * ticks
        return styles

    @staticmethod
    def convertTimeToTicks(duration) -> int:
        return round(duration * TIME_RESOLUTION)