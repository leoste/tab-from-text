from object.RhythmicChordSpan import RhythmicChordSpan
from object.ChordSpan import ChordSpan
from object.Chord import Chord
from object.Rhythm import Rhythm
from object.GuitarString import GuitarString
from object.StrumStyle import StrumStyle

intro_rhythm_durations = [2,1,1,2,1,1,1,1,1,2,1,1,1]
INTRO_RHYTHM = Rhythm(
    intro_rhythm_durations,
    [StrumStyle.NORMAL] * len(intro_rhythm_durations)
)

SALM_RHYTHM = Rhythm(
    [1] * 16,
    [StrumStyle.PALM_MUTED] * 16
)

SALM_HALF_END_RHYTHM = Rhythm(
    [1,1,1,2,1,1,1] + [1] * 8,
    [StrumStyle.NORMAL] * 16
)

SALM_END_RHYTHM = Rhythm(
    [1,1,1,2,1,1,1] * 2,
    [StrumStyle.NORMAL] * 16
)

CHORD_11_D_SHARP = Chord.get_power_chord(GuitarString.E6, 11)
CHORD_9_C_SHARP = Chord.get_power_chord(GuitarString.E6, 9)
CHORD_8_C = Chord.get_power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.get_power_chord(GuitarString.E6, 6)
CHORD_4_G_SHARP = Chord.get_power_chord(GuitarString.E6, 4)
CHORD_2_F_SHARP = Chord.get_power_chord(GuitarString.E6, 2)
CHORD_1_F = Chord.get_power_chord(GuitarString.E6, 1)

INTRO = [
    RhythmicChordSpan(
        INTRO_RHYTHM,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_1_F),
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
            ChordSpan(16, CHORD_11_D_SHARP),
            ChordSpan(32, CHORD_1_F)
        ]
    )
]

SALM = [
    RhythmicChordSpan(
        SALM_RHYTHM,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
        ]
    ),
    RhythmicChordSpan(
        SALM_HALF_END_RHYTHM,
        [ ChordSpan(16, CHORD_1_F) ]
    ),
    RhythmicChordSpan(
        SALM_RHYTHM,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
        ]
    ),
    RhythmicChordSpan(
        SALM_END_RHYTHM,
        [ ChordSpan(16, CHORD_1_F) ]
    )
]