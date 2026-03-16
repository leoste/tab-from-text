from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.RhythmicChordSpan import RhythmicChordSpan
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.Chord import Chord
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.Segment import Segment
from tabfromtext.song.GuitarString import GuitarString
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.StrummedChordSpan import StrummedChordSpan
from tabfromtext.song.Song import Song

RHYTHM = "Rhythm"
BASS = "Bass"

NOTE_6_A_SHARP = Chord.single_note(GuitarString.E6, 6)
NOTE_9_C_SHARP = Chord.single_note(GuitarString.E6, 9)
NOTE_7_B = Chord.single_note(GuitarString.E6, 7)
NOTE_6_D_SHARP = Chord.single_note(GuitarString.A5, 6)

CHORD_9_C_SHARP = Chord.power_chord(GuitarString.E6, 9)
CHORD_7_B = Chord.power_chord(GuitarString.E6, 7)
CHORD_6_A_SHARP = Chord.power_chord(GuitarString.E6, 6)

CHORD_6_D_SHARP = Chord.power_chord(GuitarString.A5, 6)
CHORD_4_C_SHARP = Chord.power_chord(GuitarString.A5, 4)

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
        [6,2],
        [StrumStyle.NO_HIT] * 6 + [StrumStyle.NORMAL] * 2
    ),
    [
        ChordSpan(8, CHORD_6_D_SHARP)
    ]
)

rhythm_intro_parts = [
    *[intro_first_three, intro_last] * 2,
    *[intro_first_three_power, intro_last] * 2,
    intro_pause,
]

bass_intro_parts = [
    *[intro_first_three, intro_last] * 4,
    intro_pause,
]

DURATIONS_8 = [ 1,1,1,1,1,1,1,1 ]
DURATIONS_323 = [ 1,1,1,2,1,1,1 ]
DURATIONS_122 = [ 1,2,2,1,1,1 ]
DURATIONS_WEIRD = [ 1.5, 1.5, 2, 1,1,1 ]
DURATIONS_WEIRD_AND_END = [ 1.5, 1.5, 2, 1,2 ]
DURATIONS_2121 = [ 2,1,1,2,1,1 ]

riff_end_chordspan = RhythmicChordSpan(
    Rhythm(
        DURATIONS_122 + DURATIONS_8 +
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
        riff_end_chordspan
    ]

bass_riff_cool_part = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 7)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 15),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 7), 8),
    StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 9)),
    StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 7)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 3),
]

bass_riff_main = ([
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 8),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 8), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 9), 5),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 9), 16)    
] + bass_riff_cool_part)

wait_chord_span = RhythmicChordSpan(
    Rhythm(
        [ 16 ]
    ),
    [
        ChordSpan(16, CHORD_6_A_SHARP)
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

rhythm_riff_salmiga_parts = (
    riff_chordspans * 2 +
    [
        RhythmicChordSpan(
            Rhythm(DURATIONS_8),
            [
                ChordSpan(7, CHORD_6_A_SHARP),
                ChordSpan(1, NOTE_6_A_SHARP)
            ]
        )
    ]
)

bass_riff_salmiga_parts = (
    bass_riff_main * 2 +
    [ 
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 7),
        StrummedChordSpan(1, Chord.no_strings_hit_chord())
    ]
)

rhythm_riff_endiga_parts = (
    riff_chordspans * 2 +
    [
        riff_end_chordspan,
        RhythmicChordSpan(
            Rhythm(
                DURATIONS_WEIRD + DURATIONS_8 +
                DURATIONS_8 + DURATIONS_WEIRD_AND_END
            ),
            [
                ChordSpan(1, CHORD_7_B),
                ChordSpan(15, CHORD_6_A_SHARP),
                ChordSpan(8, CHORD_7_B),
                ChordSpan(1.5, CHORD_9_C_SHARP),
                ChordSpan(1.5, CHORD_7_B),
                ChordSpan(5, CHORD_6_A_SHARP)
            ]
        ),
        wait_chord_span,
        RhythmicChordSpan(
            Rhythm([2,6]),
            [
                ChordSpan(2, CHORD_6_A_SHARP),
                ChordSpan(6, Chord.no_strings_hit_chord())
            ]
        )
    ]
)

bass_riff_endiga_parts = (
    bass_riff_main * 2 +
    bass_riff_cool_part +
    [
        StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 3),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(20, Chord.single_note(GuitarString.E6, 6))
    ]
)

bass_chorus_cool_part = [
    StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 9)),
    StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 7)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 3)
]

bass_chorus_near_end = ([    
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 8)
] +
bass_chorus_cool_part)

rhythm_chorus_parts = [
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
            DURATIONS_8 + DURATIONS_WEIRD_AND_END
        ),
        [
            ChordSpan(8, CHORD_6_A_SHARP),
            ChordSpan(1.5, CHORD_9_C_SHARP),
            ChordSpan(1.5, CHORD_7_B),
            ChordSpan(5, CHORD_7_B)
        ]
    ),
    wait_chord_span
]

bass_chorus_parts = (
    [
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 3),
        StrummedChordSpan(1, None),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6)),
        StrummedChordSpan(1, None),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6)),
        StrummedChordSpan(1, None),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 2),
        StrummedChordSpan(1, None),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(4, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(4, Chord.single_note(GuitarString.E6, 6))
    ] +
    bass_chorus_cool_part +
    [
        StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 6)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 2),
        StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 6)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 2),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 3),
        StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 6), 1),
        StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 6), 3)
    ] +
    bass_chorus_near_end * 2 +
    [
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 6), 8),
        StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 9)),
        StrummedChordSpan(1.5, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 7)),
        StrummedChordSpan(12, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(4, None)
    ]
)

salm_1_lyrics = Lyrics("""\
väärtushinnangutesse ei ole mõtet laskuda
see on salalik tee, kuskil ei või astuda
ainult üks on oluline ja ka kõige peamine
kas on õhtul rõõmus meel või siis oled nutune\
""", [
1,1,1,1,1,1,1,1, 1,1,1,1,1,1,2,
1,1,1,1,2,2, 1,1,1,1,1,1,2,
1,1,1,1,1,1,1,1, 1,1,1,1,1,1,2,
1,1,1,1,1,1,2, 1,1,1,1,1,1,2
], 64)

salm_2_lyrics = Lyrics("""\
loota võid et inimene muudab ennast nagu tahad
aga katse kinnitab et muutus see on väga paha
suvaline küll ei sobi, vaid üks viis on õiglane
valituks saab osutuda enda moodi kaaslane\
""", [
1,1,1,1,1,1,1,1, 1,1,1,1,0.5,1.5,0.5,1.5,
1,1,1,1,1,1,1,0.5, 1.5,1,1,1,0.5,1.5,0.5,1.5,
1,1,1,1,1,1,1,1, 1,1,1,1,1,1,2,
1,1,1,1,1,1,1,1, 1,1,1,1,1,1,2
], 64)

ref_lyrics = Lyrics("""\
mida võib tahta iga mees
peitub südames
kui oled kinni sügaval sees
ära saad vaid kaevates 
ära saad vaid kaevates
ära saad vaid kaevate e e es\
""", [
1,1,2,2,2,1,2,5,
4,4,1.5,1.5,5,
2,1,1,2,2,1,1,1,5,
1,3,2,2,1.5,1.5,5,
1,3,2,2,1.5,1.5,5,
1,3,2,2,1.5,1.5,2,1,2,8
])

INTRO = Segment("INTRO", {
    RHYTHM: rhythm_intro_parts,
    BASS:   bass_intro_parts,
})

RIFF_SALM_1 = Segment("RIFF + SALM", {
    RHYTHM: rhythm_riff_salmiga_parts,
    BASS:   bass_riff_salmiga_parts,
}, lyrics=salm_1_lyrics)

RIFF_SALM_2 = Segment("RIFF + SALM", {
    RHYTHM: rhythm_riff_salmiga_parts,
    BASS:   bass_riff_salmiga_parts,
}, lyrics=salm_2_lyrics)

CHORUS_1 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
}, lyrics=ref_lyrics)

CHORUS_2 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
}, lyrics=ref_lyrics)

RIFF_ENDIGA = Segment("RIFF 2x + LÕPP", {
    RHYTHM: rhythm_riff_endiga_parts,
    BASS:   bass_riff_endiga_parts,
})

SONG = Song("4243", [
    INTRO,
    RIFF_SALM_1,
    CHORUS_1,
    RIFF_SALM_2,
    CHORUS_2,
    RIFF_ENDIGA,
])