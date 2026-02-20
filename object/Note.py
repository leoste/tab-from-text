from typing import List
from object.Chord import Chord
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.RhythmicChordSpan import RhythmicChordSpan
from typing import Optional

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

        # part is RhythmicChordSpan
        for part in segment.parts:
            notes += Note.GetNotesFromRhythmicChordSpan(part)

        return notes
    
    @staticmethod
    def GetNotesFromRhythmicChordSpan(part: RhythmicChordSpan) -> 'List[Note]':
        notes = []
        chords = Note.flattenChordSpans(part)
        durations = Note.flattenRhythmDurations(part)
        
        note_counter = 0
        for index, chord in enumerate(chords):
            duration = durations[index % len(durations)]

            if duration is not None:
                style = part.rhythm.styles[note_counter % len(part.rhythm.styles)]
                
                notes += [Note(chord, duration, style)]
                
                note_counter += 1
            else:
                notes += [Note(None, None, None)]

        return notes
            

    @staticmethod
    def flattenChordSpans(part: RhythmicChordSpan) -> 'List[Chord]':
        chords = []

        for chordSpan in part.chordSpans:
            chords += [chordSpan.chord] * chordSpan.duration

        return chords
    
    @staticmethod
    def flattenRhythmDurations(part: RhythmicChordSpan) -> 'List[int]':
        durations = []

        for duration in part.rhythm.durations:
            durations += [duration] + [None] * (duration - 1)

        return durations
