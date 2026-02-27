from object.RhythmicChordSpan import RhythmicChordSpan
from object.ChordSpan import ChordSpan
from object.Chord import Chord
from object.Rhythm import Rhythm
from object.Segment import Segment
from object.GuitarString import GuitarString
from object.StrumStyle import StrumStyle

CHORD_8_F = Chord.get_power_chord(GuitarString.A5, 8)
CHORD_8_F_DOUBLE = Chord(None, None, 10, 10, 8, 8)
CHORD_13_F = Chord.get_power_chord(GuitarString.E6, 13)
CHORD_12_E = Chord.get_power_chord(GuitarString.E6, 12)
CHORD_10_D = Chord.get_power_chord(GuitarString.E6, 10)
CHORD_5_D = Chord.get_power_chord(GuitarString.A5, 5)
CHORD_8_C = Chord.get_power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.get_power_chord(GuitarString.E6, 6)
CHORD_5_A = Chord.get_power_chord(GuitarString.E6, 5)

DURATIONS_26 = [ 2,1,1,1,1,1,1 ]
DURATIONS_323 = [ 1,1,1,2,1,1,1 ]
DURATIONS_3212 = [ 1,1,1,2,1,2 ]
DURATIONS_8 = [ 1,1,1,1,1,1,1,1 ]

intro_base_span = RhythmicChordSpan(
    Rhythm(
        DURATIONS_26 + DURATIONS_323,
        [StrumStyle.NORMAL] * 16
    ),
    [
        ChordSpan(9, CHORD_8_F),
        ChordSpan(7, CHORD_8_C),
        ChordSpan(9, CHORD_6_A_SHARP),
        ChordSpan(7, CHORD_5_A),
        ChordSpan(9, CHORD_8_F_DOUBLE),
        ChordSpan(7, CHORD_8_C),
        ChordSpan(8, CHORD_6_A_SHARP),
        ChordSpan(8, CHORD_5_A)
    ]
)

eight_beat_rhythm = Rhythm(
    DURATIONS_8,
    [StrumStyle.NORMAL] * 8
)

FIRST_INTRO = Segment(
    "INTRO WITH 2x END",
    [
        intro_base_span,
        RhythmicChordSpan(
            eight_beat_rhythm,
            [
                ChordSpan(16, CHORD_5_A)
            ]
        )        
    ]
)

SECOND_INTRO = Segment(
    "INTRO WITH 1x END",
    [
        intro_base_span,
        RhythmicChordSpan(
            eight_beat_rhythm,
            [
                ChordSpan(8, CHORD_5_A)
            ]
        )        
    ]
)

THIRD_INTRO = Segment(
    "DOUBLE INTRO",
    [ intro_base_span ] * 2
)

SALM = Segment(
    "SALM",
    [
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8,
                [StrumStyle.PALM_MUTED] * 8
            ),
            [
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_8_C),
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_8_C),
                ChordSpan(6, CHORD_10_D),
                ChordSpan(1, CHORD_13_F),
                ChordSpan(1, CHORD_12_E),
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_8_C),
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_8_C)
            ]
        ),
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_3212,
                [StrumStyle.NORMAL] * 8
            ),
            [ ChordSpan(8, CHORD_10_D) ]
        )
    ]
)

VIIMANE_SALM = Segment(
    "VIIMANE SALM",
    [
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_8 + DURATIONS_3212,
                [StrumStyle.PALM_MUTED] * 8 + [StrumStyle.NORMAL] * 8
            ),
            [
                ChordSpan(8, CHORD_10_D),
                ChordSpan(8, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_8_C),
                ChordSpan(8, CHORD_10_D)
            ] * 4
        )
    ]
)

CHORUS = Segment(
    "REFRÄÄN",
    [
        RhythmicChordSpan(
            eight_beat_rhythm,
            [ ChordSpan(64, Chord.get_no_strings_hit_chord()) ]
        )
    ]
)

VIIMANE_CHORUS = Segment(
    "VIIMANE REFRÄÄN",
    [
        RhythmicChordSpan(
            eight_beat_rhythm,
            [
                ChordSpan(8, CHORD_5_A),
                ChordSpan(3, CHORD_5_D),
                ChordSpan(3, CHORD_8_C),
                ChordSpan(2, CHORD_6_A_SHARP),
                ChordSpan(16, CHORD_5_A),
                ChordSpan(8, CHORD_8_F),
                ChordSpan(3, CHORD_5_D),
                ChordSpan(3, CHORD_6_A_SHARP),
                ChordSpan(2, CHORD_5_A),
                ChordSpan(16, CHORD_5_A),
            ] * 2
        ),
        RhythmicChordSpan(
            Rhythm(
                [3,3,2,2],
                [StrumStyle.NORMAL] * 10
            ),
            [
                ChordSpan(3, CHORD_8_F),
                ChordSpan(5, CHORD_5_A),
                ChordSpan(2, CHORD_5_D)
            ]
        )
    ]
)

SONG = [
    FIRST_INTRO,
    SALM,
    CHORUS,
    SECOND_INTRO,
    SALM,
    CHORUS,
    THIRD_INTRO,
    VIIMANE_SALM,
    VIIMANE_CHORUS
]