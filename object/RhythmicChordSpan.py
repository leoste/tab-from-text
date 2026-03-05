from typing import List
from object.ChordSpan import ChordSpan
from object.Rhythm import Rhythm
from object.Note import Note
from object.Chord import Chord
from object.StrumStyle import StrumStyle

class RhythmicChordSpan:
    def __init__(self, rhythm: Rhythm, chordSpans: List[ChordSpan]) -> None:
        self.rhythm: Rhythm = rhythm
        self.chordSpans: List[ChordSpan] = chordSpans

    def GetNotesFromRhythmicChordSpan(self) -> 'List[Note]':
        notes = []
        chords = self.flattenChordSpans()
        durations = self.flattenRhythmDurations()
        styles = self.flattenStyles()
        
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
            
    def flattenChordSpans(self) -> 'List[Chord]':
        chords = []
        for chordSpan in self.chordSpans:
            chords += [chordSpan.chord] * Note.convertTimeToTicks(chordSpan.duration)
        return chords
    
    def flattenRhythmDurations(self) -> 'List[int]':
        durations = []
        for duration in self.rhythm.durations:
            ticks = Note.convertTimeToTicks(duration)
            durations += [ticks] + [None] * (ticks - 1)
        return durations

    def flattenStyles(self) -> 'List[StrumStyle]':
        styles = []
        for style in self.rhythm.styles:
            ticks = Note.convertTimeToTicks(1)  # each style entry covers one eighth note = TIME_RESOLUTION ticks
            styles += [style] * ticks
        return styles