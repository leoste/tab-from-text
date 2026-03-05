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
    [1,1,1,3,2]
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
        [2,2,2,2]
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

DURATIONS_8 = [ 1,1,1,1,1,1,1,1 ]
DURATIONS_323 = [ 1,1,1,2,1,1,1 ]
DURATIONS_122 = [ 1,2,2,1,1,1 ]
DURATIONS_WEIRD = [ 1.5, 1.5, 2, 1,1,1 ]
DURATIONS_2121 = [ 2,1,1,2,1,1 ]

riff_chordspans = [
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8 + DURATIONS_323
            ),
            [
                ChordSpan(16, CHORD_6_D_SHARP),
                ChordSpan(16, CHORD_4_C_SHARP) 
            ]
        ),
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_WEIRD + DURATIONS_8 +
                DURATIONS_8 + DURATIONS_WEIRD
            ),
            [
                ChordSpan(1, CHORD_7_B),
                ChordSpan(15, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_7_B),
                ChordSpan(1.5, CHORD_9_C_SHARP),
                ChordSpan(1.5, CHORD_7_B),
                ChordSpan(5, CHORD_6_A_SHARP)
            ]
        )
    ]

RIFF_SALMIGA = Segment(
    "RIFF + SALM",
    riff_chordspans * 2 +
    [
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8
            ),
            [
                ChordSpan(7, CHORD_6_A_SHARP),
                ChordSpan(1, NOTE_6_A_SHARP)
            ]
        )
    ]
)

chorus_first_rhytm = Rhythm(
    DURATIONS_2121 + DURATIONS_323
)

chorus_second_chords = [
    ChordSpan(8, CHORD_6_A_SHARP),
    ChordSpan(1.5, CHORD_9_C_SHARP),
    ChordSpan(1.5, CHORD_7_B),
    ChordSpan(5, CHORD_6_A_SHARP)
]

CHORUS = Segment(
    "REFRÄÄN",
    [
        RhythmicChordSpan(
            chorus_first_rhytm,
            [
                ChordSpan(8, CHORD_6_D_SHARP),
                ChordSpan(8, CHORD_6_A_SHARP)
            ]
        ),
        RhythmicChordSpan(
            Rhythm(
                [4, 4] + DURATIONS_WEIRD
            ),
            [
                ChordSpan(4, CHORD_7_B),
                ChordSpan(4, CHORD_6_A_SHARP),
                ChordSpan(1.5, CHORD_9_C_SHARP),
                ChordSpan(1.5, CHORD_7_B),
                ChordSpan(4, CHORD_6_A_SHARP),
                ChordSpan(1, NOTE_6_A_SHARP)
            ]
        ),
        RhythmicChordSpan(
            chorus_first_rhytm,
            [ ChordSpan(16, CHORD_6_D_SHARP) ]
        ),
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_2121 + DURATIONS_WEIRD
            ),
            chorus_second_chords
        ),
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8 + DURATIONS_WEIRD
            ),
            chorus_second_chords
        ),
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8 + [ 1.5, 1.5, 2, 1,2 ]
            ),
            [
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(1.5, CHORD_9_C_SHARP),
                ChordSpan(1.5, CHORD_7_B),
                ChordSpan(5, CHORD_7_B)
            ]
        ),
        RhythmicChordSpan(
            Rhythm(
                [ 16 ]
            ),
            [
                ChordSpan(16, CHORD_6_A_SHARP)
            ]
        )
    ]
)

SONG = [
    INTRO,
    RIFF_SALMIGA,
    CHORUS
    #RIFF_SALMIGA,
    #SALM,
    #CHORUS,
    #RIFF_TOPELT,
    #END
]