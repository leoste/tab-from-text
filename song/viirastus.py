from song.object.RhythmicChordSpan import RhythmicChordSpan
from song.object.ChordSpan import ChordSpan
from song.object.Chord import Chord
from song.object.Rhythm import Rhythm
from song.object.Segment import Segment
from song.object.GuitarString import GuitarString
from song.object.StrumStyle import StrumStyle
from song.object.StrummedChordSpan import StrummedChordSpan
from song.object.Song import Song

RHYTHM = "Rhythm"
BASS = "Bass"

CHORD_8_F = Chord.power_chord(GuitarString.A5, 8)
CHORD_8_F_DOUBLE = Chord(None, None, 10, 10, 8, 8)
CHORD_13_F = Chord.power_chord(GuitarString.E6, 13)
CHORD_12_E = Chord.power_chord(GuitarString.E6, 12)
CHORD_10_D = Chord.power_chord(GuitarString.E6, 10)
CHORD_5_D = Chord.power_chord(GuitarString.A5, 5)
CHORD_8_C = Chord.power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.power_chord(GuitarString.E6, 6)
CHORD_5_A = Chord.power_chord(GuitarString.E6, 5)

NOTE_8_F = Chord.single_note(GuitarString.A5, 8)
NOTE_13_F = Chord.single_note(GuitarString.E6, 13)
NOTE_12_E = Chord.single_note(GuitarString.E6, 12)
NOTE_10_D = Chord.single_note(GuitarString.E6, 10)
NOTE_5_D = Chord.single_note(GuitarString.A5, 5)
NOTE_8_C = Chord.single_note(GuitarString.E6, 8)
NOTE_6_A_SHARP = Chord.single_note(GuitarString.E6, 6)
NOTE_5_A = Chord.single_note(GuitarString.E6, 5)

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

# --- Rhythm guitar intro parts ---

rhythm_first_intro_parts = [
    intro_base_span,
    RhythmicChordSpan(
        eight_beat_rhythm,
        [ ChordSpan(16, CHORD_5_A) ]
    )
]

rhythm_second_intro_parts = [
    intro_base_span,
    RhythmicChordSpan(
        eight_beat_rhythm,
        [ ChordSpan(8, CHORD_5_A) ]
    )
]

rhythm_third_intro_parts = [ intro_base_span ] * 2

# --- Bass intro parts ---

bass_intro_base = [
    StrummedChordSpan(1, NOTE_8_F, 9),
    StrummedChordSpan(1, NOTE_8_C, 7),
    StrummedChordSpan(1, NOTE_6_A_SHARP, 8),
    StrummedChordSpan(1, NOTE_5_A, 8)
] * 2

bass_first_intro_parts = bass_intro_base + [ StrummedChordSpan(1, NOTE_5_A, 16) ]
bass_second_intro_parts = bass_intro_base + [ StrummedChordSpan(1, NOTE_5_A, 8) ]
bass_third_intro_parts = bass_intro_base * 2

# --- Rhythm guitar salm parts ---

rhythm_salm_parts = [
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

rhythm_viimane_salm_parts = [
    RhythmicChordSpan(
        Rhythm(
            DURATIONS_8 + DURATIONS_3212,
            [StrumStyle.PALM_MUTED] * 11 + [StrumStyle.NORMAL] * 5
        ),
        [
            ChordSpan(8, CHORD_10_D),
            ChordSpan(8, CHORD_6_A_SHARP),
            ChordSpan(8, CHORD_8_C),
            ChordSpan(8, CHORD_10_D)
        ] * 4
    )
]

# --- Bass salm parts ---
# bass_salm_parts is reused for all three salm segments (including viimane salm);
# the rhythm guitar differs on the third but the bass line is identical.

bass_salm_firster = [
    StrummedChordSpan(1, NOTE_10_D, 9),
    StrummedChordSpan(1, NOTE_6_A_SHARP, 7),
    StrummedChordSpan(1, NOTE_8_C, 8),
    StrummedChordSpan(1, NOTE_10_D, 6),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 12)),
    StrummedChordSpan(1, NOTE_10_D),
    StrummedChordSpan(1, NOTE_10_D, 9),
    StrummedChordSpan(1, NOTE_6_A_SHARP, 7),
    StrummedChordSpan(1, NOTE_8_C, 8),
    StrummedChordSpan(1, NOTE_10_D, 5),
]

bass_salm_parts = (
    bass_salm_firster +
    [
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 12)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 13))
    ] +
    bass_salm_firster +
    [ StrummedChordSpan(1, NOTE_10_D, 3) ]
)

# bass_viimane_salm_parts shares the same notes as bass_salm_parts
bass_viimane_salm_parts = bass_salm_parts

# --- Rhythm guitar chorus parts ---

rhythm_chorus_parts = [
    RhythmicChordSpan(
        Rhythm([8]),
        [ ChordSpan(64, Chord.no_strings_hit_chord()) ]
    )
]

rhythm_viimane_chorus_parts = [
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
            [3,3,2,2,6],
            [StrumStyle.NORMAL] * 16
        ),
        [
            ChordSpan(3, CHORD_8_F),
            ChordSpan(5, CHORD_5_A),
            ChordSpan(2, CHORD_5_D),
            ChordSpan(6, Chord.no_strings_hit_chord())
        ]
    )
]

# --- Bass chorus parts ---

bass_chorus_parts = [ 
    StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 10)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 6)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 8)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 8)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 8)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 9)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 10)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 10), 14)
] * 2

bass_viimane_chorus_parts = (
    [ 
        StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 8)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 8)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 9)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 10)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 8)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 5)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 5), 14),

        StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 8)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 8)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 9)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 10)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 5)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 5)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 5), 14)
    ] * 2 +
    [
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 5)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 8)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 5)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 5)),        
        StrummedChordSpan(6, None)
    ]
)

salm_1_lyrics = """\
On kätte jõudnud aeg
Ja maksma ma pean
Ei jää siin pidama
Maksan eluaeg

Pingutatud sai
ülemääragi
Ei ole midagi
Käes hoida vaid\
"""

salm_2_lyrics = """\
silme ees on mul
mingi viirastus
mingi vastutus
ei tea kas olen hull

silmad lahti teen
pilt mu ees siis kaob
kuid kõrvus ikka taob
kaja ülipeen\
"""

salm_3_lyrics = """\
on kätte jõudnud aeg
ja maksnud olen ma
ei jää siin pidama
maksan eluaeg

pingutatud sai
ülemääragi
ja teada sedagi
jätkub see vaid\
"""

ref_lyrics = """\
kas saaksin proovida veel
või ongi läbi mu tee\
"""

final_ref_lyrics = """\
ei saagi proovida veel
ongi nüüd läbi mu tee
ei saagi proovida veel
ongi nüüd läbi mu tee
"""

FIRST_INTRO = Segment("INTRO WITH 2x END", {
    RHYTHM: rhythm_first_intro_parts,
    BASS:   bass_first_intro_parts,
})

SECOND_INTRO = Segment("INTRO WITH 1x END", {
    RHYTHM: rhythm_second_intro_parts,
    BASS:   bass_second_intro_parts,
})

THIRD_INTRO = Segment("DOUBLE INTRO", {
    RHYTHM: rhythm_third_intro_parts,
    BASS:   bass_third_intro_parts,
})

SALM_1 = Segment("SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS:   bass_salm_parts,
}, lyrics=salm_1_lyrics)

SALM_2 = Segment("SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS:   bass_salm_parts,
}, lyrics=salm_2_lyrics)

VIIMANE_SALM = Segment("VIIMANE SALM", {
    RHYTHM: rhythm_viimane_salm_parts,
    BASS:   bass_viimane_salm_parts,   # same notes as bass_salm_parts
}, lyrics=salm_3_lyrics)

CHORUS_1 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
}, lyrics=ref_lyrics)

CHORUS_2 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
}, lyrics=ref_lyrics)

VIIMANE_CHORUS = Segment("VIIMANE REFRÄÄN", {
    RHYTHM: rhythm_viimane_chorus_parts,
    BASS:   bass_viimane_chorus_parts,
}, lyrics=final_ref_lyrics)

SONG = Song("Viirastus", [
    FIRST_INTRO,
    SALM_1,
    CHORUS_1,
    SECOND_INTRO,
    SALM_2,
    CHORUS_2,
    THIRD_INTRO,
    VIIMANE_SALM,
    VIIMANE_CHORUS,
])