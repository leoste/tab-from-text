from song.object.RhythmicChordSpan import RhythmicChordSpan
from song.object.ChordSpan import ChordSpan
from song.object.Chord import Chord
from song.object.Rhythm import Rhythm
from song.object.Segment import Segment
from song.object.GuitarString import GuitarString
from song.object.StrumStyle import StrumStyle
from song.object.Song import Song

RHYTHM = "Rhythm"

CHORD_13_F = Chord.power_chord(GuitarString.E6, 13)
CHORD_13_C = Chord(None, None, None, 15, 13, 13)
CHORD_11_D_SHARP = Chord.power_chord(GuitarString.E6, 11)
CHORD_9_C_SHARP = Chord.power_chord(GuitarString.E6, 9)
CHORD_8_C = Chord.power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.power_chord(GuitarString.E6, 6)
CHORD_4_G_SHARP = Chord.power_chord(GuitarString.E6, 4)
CHORD_2_F_SHARP = Chord.power_chord(GuitarString.E6, 2)
CHORD_1_F = Chord.power_chord(GuitarString.E6, 1)

DURATIONS_232 = [1,1,1,2,1,1,1]
INTRO_RHYTHM = Rhythm(
    [2,1,1,2,1,1] + DURATIONS_232,
    [StrumStyle.NORMAL] * 16
)

intro_parts = [
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

SALM_RHYTHM = Rhythm(
    [1] * 16,
    [StrumStyle.PALM_MUTED] * 16
)

SALM_HALF_END_RHYTHM = Rhythm(
    DURATIONS_232 + [1] * 8,
    [StrumStyle.NORMAL] * 16
)

SALM_END_RHYTHM = Rhythm(
    DURATIONS_232 * 2,
    [StrumStyle.NORMAL] * 16
)

salm_parts = [
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

CHORUS_FIRST_MEASURE_RHYTHM = Rhythm(
    [2] + [1] * 14,
    [StrumStyle.NORMAL] * 16
)

CHORUS_THIRD_MEASURE_RHYTHM = Rhythm(
        [1] * 16,
        [StrumStyle.NORMAL] * 16
)

CHORUS_SEVENTH_MEASURE_RHYTHM = Rhythm(
    [3,3,2,1,1,1,1,1,1,1,1],
    [StrumStyle.NORMAL] * 16
)

chorus_parts = [
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

BREAK_LAST_MEASURE_RHYTHM = Rhythm(
    [1] * 8 + DURATIONS_232,
    [StrumStyle.NORMAL] * 16
)

breakdown_parts = [
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
        [ ChordSpan(16, CHORD_8_C) ]
    ),
    RhythmicChordSpan(
        Rhythm(
            [ 
                2,
                2,
                4,
                8
            ],
            [
                StrumStyle.SLIDE,
                StrumStyle.SLIDE,
                StrumStyle.NORMAL,
                StrumStyle.NORMAL                
            ] +
            [ StrumStyle.NO_HIT ] * 12
        ),
        [
            ChordSpan(2, CHORD_8_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(12, Chord.no_strings_hit_chord())
        ]
    )
]

end_parts = [
    RhythmicChordSpan(
        Rhythm(
            [1] * 8 + DURATIONS_232,
            [StrumStyle.NORMAL] * 16
        ),
        [
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(1, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(1, CHORD_13_F),
            ChordSpan(1, CHORD_13_C),
            ChordSpan(1, CHORD_13_C)
        ] * 3
    ),
    RhythmicChordSpan(
        Rhythm(
            [1] * 8 + [2,6],
            [ StrumStyle.NORMAL ] * 10 +
            [ StrumStyle.NO_HIT ] * 6
        ),
        [
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(6, CHORD_13_F),
            ChordSpan(6, Chord.no_strings_hit_chord())
        ]
    )
]

salm_1_lyrics = """\
sõpradena võime ju koos
minna sinna kuhu tahtnud hoos
aga tulla sealt ära me
vaid võhivõõrastena või-me\
"""

salm_2_lyrics = """\
tuulega mul kõrvus kõlab noot
pilvedega toob ta miskit uut
aimasingi et nii minna võib
selguse see mulle pähe tõi\
"""

chorus_lyrics = """\
siiski ootan mina sinu järel
järgnen sulle kasvõi kui oleks hambad sul verel
tahan teada vaid et mis on su tahe
suhtlus tundub pikimööda täitsa meil jahe\
"""

INTRO = Segment("INTRO", {RHYTHM: intro_parts})
SALM_1 = Segment("SALM", {RHYTHM: salm_parts}, lyrics=salm_1_lyrics)
SALM_2 = Segment("SALM", {RHYTHM: salm_parts}, lyrics=salm_2_lyrics)
CHORUS = Segment("REFRÄÄN", {RHYTHM: chorus_parts}, lyrics=chorus_lyrics)
INSTRUMENTAL_CHORUS = Segment("INSTRUMENTAALNE REFRÄÄN", {RHYTHM: chorus_parts})
BREAKDOWN = Segment("BREAKDOWN", {RHYTHM: breakdown_parts})
END = Segment("LÕPP", {RHYTHM: end_parts})

SONG = Song("Jahe", [
    INTRO,
    SALM_1,
    CHORUS,
    INTRO,
    SALM_2,
    CHORUS,
    BREAKDOWN,
    CHORUS,
    INSTRUMENTAL_CHORUS,
    END,
])