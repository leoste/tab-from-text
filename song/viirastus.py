from object.RhythmicChordSpan import RhythmicChordSpan
from object.ChordSpan import ChordSpan
from object.Chord import Chord
from object.Rhythm import Rhythm
from object.Segment import Segment
from object.GuitarString import GuitarString
from object.StrumStyle import StrumStyle
from object.Instrument import Instrument
from object.StrummedChordSpan import StrummedChordSpan
from object.Song import Song
from object.SongSection import SongSection

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
)

CHORUS = Segment(
    "REFRÄÄN",
    [
        RhythmicChordSpan(
            Rhythm([8]),
            [ ChordSpan(64, Chord.no_strings_hit_chord()) ]
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
)

# --- BASS ---

bass_intro_base = [
    StrummedChordSpan(1, NOTE_8_F, 9),
    StrummedChordSpan(1, NOTE_8_C, 7),
    StrummedChordSpan(1, NOTE_6_A_SHARP, 8),
    StrummedChordSpan(1, NOTE_5_A, 8)
] * 2

BASS_FIRST_INTRO = Segment(
    "INTRO WITH 2x END",
    bass_intro_base +
    [ StrummedChordSpan(1, NOTE_5_A, 16) ]
)

BASS_SECOND_INTRO = Segment(
    "INTRO WITH 1x END",
    bass_intro_base +
    [ StrummedChordSpan(1, NOTE_5_A, 8) ]
)

BASS_THIRD_INTRO = Segment(
    "DOUBLE INTRO",
    bass_intro_base * 2
)

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

BASS_SALM = Segment(
    "SALM",
    bass_salm_firster +
    [
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 12)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 13))
    ] +
    bass_salm_firster +
    [StrummedChordSpan(1, NOTE_10_D, 3)]
) 

BASS_CHORUS = Segment(
    "REFRÄÄN",
    [ 
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 10)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 6)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 8)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 8)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 8)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 9)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 10)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 10), 14)
    ] * 2
)

BASS_VIIMANE_CHORUS = Segment(
    "VIIMANE REFRÄÄN",
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

RHYTHM = Instrument(
    "Rhythm",
    [
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
)

BASS = Instrument(
    "Bass",
    [
        BASS_FIRST_INTRO,
        BASS_SALM,
        BASS_CHORUS,
        BASS_SECOND_INTRO,
        BASS_SALM,
        BASS_CHORUS,
        BASS_THIRD_INTRO,
        BASS_SALM,
        BASS_VIIMANE_CHORUS
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

SONG = Song("Viirastus", [RHYTHM, BASS], structure=[
    SongSection("INTRO WITH 2x END"),
    SongSection("SALM", salm_1_lyrics),
    SongSection("REFRÄÄN", ref_lyrics),
    SongSection("INTRO WITH 1x END"),
    SongSection("SALM", salm_2_lyrics),
    SongSection("REFRÄÄN", ref_lyrics),
    SongSection("DOUBLE INTRO"),
    SongSection("VIIMANE SALM", salm_3_lyrics),
    SongSection("VIIMANE REFRÄÄN", final_ref_lyrics),
])