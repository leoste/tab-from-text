from object.RhythmicChordSpan import RhythmicChordSpan
from object.ChordSpan import ChordSpan
from object.Chord import Chord
from object.Rhythm import Rhythm
from object.Segment import Segment
from object.GuitarString import GuitarString
from object.StrumStyle import StrumStyle

NOTE_6_A_SHARP = Chord.get_single_note(GuitarString.E6, 6)
NOTE_9_C_SHARP = Chord.get_single_note(GuitarString.E6, 9)
NOTE_7_B = Chord.get_single_note(GuitarString.E6, 7)
NOTE_6_D_SHARP = Chord.get_single_note(GuitarString.A5, 6)

CHORD_9_C_SHARP = Chord.get_power_chord(GuitarString.E6, 9)
CHORD_7_B = Chord.get_power_chord(GuitarString.E6, 7)
CHORD_6_A_SHARP = Chord.get_power_chord(GuitarString.E6, 6)

CHORD_6_D_SHARP = Chord.get_power_chord(GuitarString.A5, 6)
CHORD_4_C_SHARP = Chord.get_power_chord(GuitarString.A5, 4)

intro_first_three_rhythm = Rhythm(
    [1,1,1,3,2],
    [StrumStyle.NORMAL] * 8
)

intro_first_three = RhythmicChordSpan(
    intro_first_three_rhythm,
    [
        ChordSpan(3, NOTE_6_A_SHARP),
        ChordSpan(3, NOTE_9_C_SHARP),
        ChordSpan(2, NOTE_7_B)
    ] * 3
)

intro_first_three_power = RhythmicChordSpan(
    intro_first_three_rhythm,
    [
        ChordSpan(3, NOTE_6_A_SHARP),
        ChordSpan(3, CHORD_9_C_SHARP),
        ChordSpan(2, CHORD_7_B)
    ] * 3
)

intro_last = RhythmicChordSpan(
    Rhythm(
        [2,2,2,2],
        [StrumStyle.NORMAL] * 8
    ),
    [
        ChordSpan(2, NOTE_6_D_SHARP),
        ChordSpan(2, NOTE_6_A_SHARP),
        ChordSpan(2, NOTE_7_B),
        ChordSpan(2, NOTE_6_A_SHARP)
    ]
)

intro_pause = RhythmicChordSpan(
    Rhythm(
        [2,2,2,2],
        [StrumStyle.NO_HIT] * 6 + [StrumStyle.NORMAL] * 2
    ),
    [
        ChordSpan(8, CHORD_6_D_SHARP)
    ]
)

INTRO = Segment(
    "INTRO",
    [
        intro_first_three,
        intro_last
    ] * 2 + [
        intro_first_three_power,
        intro_last
    ] * 2 + [
        intro_pause
    ]
)

SONG = [
    INTRO,
    #RIFF,
    #SALM,
    #CHORUS,
    #RIFF,
    #SALM,
    #CHORUS,
    #RIFF,
    #END
]