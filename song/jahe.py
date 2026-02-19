from object.RhythmicChordSpan import RhythmicChordSpan
from object.ChordSpan import ChordSpan
from object.Chord import Chord
from object.Rhythm import Rhythm
from object.Segment import Segment
from object.GuitarString import GuitarString
from object.StrumStyle import StrumStyle

CHORD_13_F = Chord.get_power_chord(GuitarString.E6, 13)
CHORD_11_D_SHARP = Chord.get_power_chord(GuitarString.E6, 11)
CHORD_9_C_SHARP = Chord.get_power_chord(GuitarString.E6, 9)
CHORD_8_C = Chord.get_power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.get_power_chord(GuitarString.E6, 6)
CHORD_4_G_SHARP = Chord.get_power_chord(GuitarString.E6, 4)
CHORD_2_F_SHARP = Chord.get_power_chord(GuitarString.E6, 2)
CHORD_1_F = Chord.get_power_chord(GuitarString.E6, 1)

DURATIONS_232 = [1,1,1,2,1,1,1]

intro_rhythm_durations = [2,1,1,2,1,1] + DURATIONS_232
INTRO_RHYTHM = Rhythm(
    intro_rhythm_durations,
    [StrumStyle.NORMAL] * 16
)

INTRO = Segment(
    "INTRO",
    [
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
)

SALM_RHYTHM = Rhythm(
    [1] * 16,
    [StrumStyle.PALM_MUTED] * 16
)

salm_half_end_durations = DURATIONS_232 + [1] * 8
SALM_HALF_END_RHYTHM = Rhythm(
    salm_half_end_durations,
    [StrumStyle.NORMAL] * 16
)

salm_end_durations =  DURATIONS_232 * 2
SALM_END_RHYTHM = Rhythm(
    salm_end_durations,
    [StrumStyle.NORMAL] * 16
)

SALM = Segment(
    "SALM",
    [
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
)

chorus_first_measure_durations = [2] + [1] * 14
CHORUS_FIRST_MEASURE_RHYTHM = Rhythm(
        chorus_first_measure_durations,
        [StrumStyle.NORMAL] * 16
)

CHORUS_THIRD_MEASURE_RHYTHM = Rhythm(
        [1] * 16,
        [StrumStyle.NORMAL] * 16
)

chorus_seventh_measure_durations = [3,3,2,1,1,1,1,1,1,1,1]
CHORUS_SEVENTH_MEASURE_RHYTHM = Rhythm(
    chorus_seventh_measure_durations,
    [StrumStyle.NORMAL] * 16
)


CHORUS = Segment(
    "REFRÄÄN",
    [
        RhythmicChordSpan(
            CHORUS_FIRST_MEASURE_RHYTHM,
            [ ChordSpan(16, CHORD_9_C_SHARP) ]
        ),
        RhythmicChordSpan(
            CHORUS_THIRD_MEASURE_RHYTHM,
            [
                ChordSpan(16, CHORD_6_A_SHARP),
                ChordSpan(16, CHORD_4_G_SHARP)
            ],
        ),
        RhythmicChordSpan(
            CHORUS_SEVENTH_MEASURE_RHYTHM,
            [
                ChordSpan(9, CHORD_9_C_SHARP),
                ChordSpan(7, CHORD_8_C)
            ]
        )
    ] * 2
)

# TODO: make same style duration calculation for rhythm strumstyle and chord span.
# right now chord span is counting halfbeats, but strumstyle actual array members.
# make both halfbeats. also make it universally understood everywhere that its halfbeats.
# this gets rid of all the *len() or most of them

break_last_measure_durations = [1] * 8 + DURATIONS_232
BREAK_LAST_MEASURE_RHYTHM = Rhythm(
    break_last_measure_durations,
    [StrumStyle.NORMAL] * 16
)

BREAK = Segment(
    "BREAKDOWN",
    [
        RhythmicChordSpan(
            Rhythm(
                [1] * 16,
                [StrumStyle.NORMAL] * 16
            ),
            [
                ChordSpan(16, CHORD_13_F),
                ChordSpan(4, CHORD_9_C_SHARP),
                ChordSpan(4, CHORD_8_C),
                ChordSpan(8, CHORD_9_C_SHARP),
                ChordSpan(16, CHORD_6_A_SHARP),
                ChordSpan(16, CHORD_8_C),
                ChordSpan(16, CHORD_13_F),
                ChordSpan(4, CHORD_9_C_SHARP),
                ChordSpan(4, CHORD_8_C),
                ChordSpan(8, CHORD_9_C_SHARP),
                ChordSpan(16, CHORD_6_A_SHARP)
            ]
        ),
        RhythmicChordSpan(
            BREAK_LAST_MEASURE_RHYTHM,
            ChordSpan(16, CHORD_8_C)
        )
        # TODO: add 2 measures of silence that has 4 halfbeats long upwards bend
        # TODO: add support for bends
    ]
)

END = [
    # TODO: add end tabs
]

SONG = [
    INTRO,
    SALM,
    CHORUS,
    INTRO,
    SALM,
    CHORUS,
    BREAK,
    CHORUS,
    CHORUS,
    END
]