from typing import List
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.Note import Note
from tabfromtext.song.Chord import Chord
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.NoteProvider import NoteProvider


class RhythmicChordSpan(NoteProvider):
    def __init__(self, rhythm: Rhythm, chordSpans: List[ChordSpan]) -> None:
        self.rhythm: Rhythm = rhythm
        self.chordSpans: List[ChordSpan] = chordSpans

    def getNotes(self) -> List[Note]:
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
            
    def flattenChordSpans(self) -> List[Chord]:
        chords = []
        for chordSpan in self.chordSpans:
            chords += chordSpan.flattenChordSpan()
        return chords
    
    def flattenRhythmDurations(self) -> List:
        durations = []
        for duration in self.rhythm.durations:
            durations += Note.flattenDuration(duration)
        return durations

    def flattenStyles(self) -> List[StrumStyle]:
        styles = []
        for style in self.rhythm.styles:
            styles += StrumStyle.flattenStyle(style)
        return styles