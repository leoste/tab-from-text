from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.RhythmicChordSpanList import RhythmicChordSpanList
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.Chord import Chord
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.Segment import Segment
from tabfromtext.song.GuitarString import E6, A5, D4, G3, B2, E1
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.RepeatingChordSpan import RepeatingChordSpan
from tabfromtext.song.Song import Song

RHYTHM = "Rhythm"
BASS = "Bass"
LEAD = "Lead"

CHORD_8_F = Chord.power_chord(A5, 8)
CHORD_8_F_DOUBLE = Chord(None, None, 10, 10, 8, 8)
CHORD_13_F = Chord.power_chord(E6, 13)
CHORD_12_E = Chord.power_chord(E6, 12)
CHORD_10_D = Chord.power_chord(E6, 10)
CHORD_5_D = Chord.power_chord(A5, 5)
CHORD_8_C = Chord.power_chord(E6, 8)
CHORD_6_A_SHARP = Chord.power_chord(E6, 6)
CHORD_5_A = Chord.power_chord(E6, 5)

NOTE_8_F = Chord.single_note(A5, 8)
NOTE_13_F = Chord.single_note(E6, 13)
NOTE_12_E = Chord.single_note(E6, 12)
NOTE_10_D = Chord.single_note(E6, 10)
NOTE_5_D = Chord.single_note(A5, 5)
NOTE_8_C = Chord.single_note(E6, 8)
NOTE_6_A_SHARP = Chord.single_note(E6, 6)
NOTE_5_A = Chord.single_note(E6, 5)

DURATIONS_26 = [ 2,1,1,1,1,1,1 ]
DURATIONS_323 = [ 1,1,1,2,1,1,1 ]
DURATIONS_3212 = [ 1,1,1,2,1,2 ]
DURATIONS_8 = [ 1,1,1,1,1,1,1,1 ]

intro_base_span = RhythmicChordSpanList(
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

rhythm_first_intro_parts = [
    intro_base_span,
    RhythmicChordSpanList(
        eight_beat_rhythm,
        [ ChordSpan(16, CHORD_5_A) ]
    )
]

rhythm_second_intro_parts = [
    intro_base_span,
    RhythmicChordSpanList(
        eight_beat_rhythm,
        [ ChordSpan(8, CHORD_5_A) ]
    )
]

rhythm_third_intro_parts = [ intro_base_span ] * 2

bass_intro_base = [
    RepeatingChordSpan(1, NOTE_8_F, 9),
    RepeatingChordSpan(1, NOTE_8_C, 7),
    RepeatingChordSpan(1, NOTE_6_A_SHARP, 8),
    RepeatingChordSpan(1, NOTE_5_A, 8)
] * 2

bass_first_intro_parts = bass_intro_base + [ RepeatingChordSpan(1, NOTE_5_A, 16) ]
bass_second_intro_parts = bass_intro_base + [ RepeatingChordSpan(1, NOTE_5_A, 8) ]
bass_third_intro_parts = bass_intro_base * 2

rhythm_salm_parts = [
    RhythmicChordSpanList(
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
    RhythmicChordSpanList(
        Rhythm(
            DURATIONS_3212,
            [StrumStyle.NORMAL] * 8
        ),
        [ ChordSpan(8, CHORD_10_D) ]
    )
]

rhythm_viimane_salm_parts = [
    RhythmicChordSpanList(
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

bass_salm_firster = [
    RepeatingChordSpan(1, NOTE_10_D, 9),
    RepeatingChordSpan(1, NOTE_6_A_SHARP, 7),
    RepeatingChordSpan(1, NOTE_8_C, 8),
    RepeatingChordSpan(1, NOTE_10_D, 6),
    RepeatingChordSpan(1, Chord.single_note(A5, 12)),
    RepeatingChordSpan(1, NOTE_10_D),
    RepeatingChordSpan(1, NOTE_10_D, 9),
    RepeatingChordSpan(1, NOTE_6_A_SHARP, 7),
    RepeatingChordSpan(1, NOTE_8_C, 8),
    RepeatingChordSpan(1, NOTE_10_D, 5),
]

bass_salm_parts = (
    bass_salm_firster +
    [
        RepeatingChordSpan(1, Chord.single_note(E6, 12)),
        RepeatingChordSpan(2, Chord.single_note(E6, 13))
    ] +
    bass_salm_firster +
    [ RepeatingChordSpan(1, NOTE_10_D, 3) ]
)

# bass_viimane_salm_parts shares the same notes as bass_salm_parts
bass_viimane_salm_parts = bass_salm_parts

# --- Rhythm guitar chorus parts ---

rhythm_chorus_parts = [ 
    RepeatingChordSpan(3, Chord.power_chord(E6, 10)),
    RepeatingChordSpan(3, Chord.power_chord(E6, 6)),
    RepeatingChordSpan(2, Chord.power_chord(E6, 8)),
    RepeatingChordSpan(3, Chord.power_chord(A5, 8)),
    RepeatingChordSpan(3, Chord.power_chord(E6, 8)),
    RepeatingChordSpan(2, Chord.power_chord(E6, 9)),
    RepeatingChordSpan(2, Chord.power_chord(E6, 10)),
    RepeatingChordSpan(1, Chord.power_chord(E6, 10), 14, StrumStyle.PALM_MUTED)
] * 2

rhythm_viimane_chorus_parts = [
    RhythmicChordSpanList(
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
    RhythmicChordSpanList(
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

bass_chorus_parts = [ 
    RepeatingChordSpan(3, Chord.single_note(E6, 10)),
    RepeatingChordSpan(3, Chord.single_note(E6, 6)),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),
    RepeatingChordSpan(3, Chord.single_note(A5, 8)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 10)),
    RepeatingChordSpan(1, Chord.single_note(E6, 10), 14)
] * 2

bass_viimane_chorus_parts = (
    [ 
        RepeatingChordSpan(3, Chord.single_note(A5, 8)),
        RepeatingChordSpan(3, Chord.single_note(E6, 8)),
        RepeatingChordSpan(2, Chord.single_note(E6, 9)),
        RepeatingChordSpan(3, Chord.single_note(E6, 10)),
        RepeatingChordSpan(3, Chord.single_note(E6, 8)),
        RepeatingChordSpan(2, Chord.single_note(E6, 6)),
        RepeatingChordSpan(2, Chord.single_note(E6, 5)),
        RepeatingChordSpan(1, Chord.single_note(E6, 5), 14),

        RepeatingChordSpan(3, Chord.single_note(A5, 8)),
        RepeatingChordSpan(3, Chord.single_note(E6, 8)),
        RepeatingChordSpan(2, Chord.single_note(E6, 9)),
        RepeatingChordSpan(3, Chord.single_note(E6, 10)),
        RepeatingChordSpan(3, Chord.single_note(E6, 6)),
        RepeatingChordSpan(2, Chord.single_note(E6, 5)),
        RepeatingChordSpan(2, Chord.single_note(E6, 5)),
        RepeatingChordSpan(1, Chord.single_note(E6, 5), 14)
    ] * 2 +
    [
        RepeatingChordSpan(3, Chord.single_note(E6, 5)),
        RepeatingChordSpan(3, Chord.single_note(A5, 8)),
        RepeatingChordSpan(2, Chord.single_note(E6, 5)),
        RepeatingChordSpan(2, Chord.single_note(A5, 5)),        
        RepeatingChordSpan(6, None)
    ]
)

salm_1_lyrics = Lyrics("""\
on kätte jõudnud aeg
kus maksma ma pean
ja ühte ma nean
on korvamata vaev
pingutatud sai
ülemääragi
ei ole midagi
käes hoida vaid
""", [
1, 1.5,0.5,1,1,11,
1, 2,1,1,11,
1, 2,1,1,11,
1, 1.5,0.5,1,1,12,
1,1,1,1,12,
1,1,1,1,11,
1, 1,1,1,1,12,
2,1.5,0.5,12
], -1)

salm_2_lyrics = Lyrics("""\
silme ees on mul
mingi viirastus
mingi vastutus
ei tea kas olen hull
silmad lahti teen
pilt mu ees siis kaob
kuid kõrvus ikka taob
kaja ülipeen\
""", [
1,1,1,1,12,
1.5,0.5,1,1,12,
1.5,0.5,1,1,11,
1, 1,1,0.5,1.5,12,
1,1,1.5,0.5,12,
1.5,0.5,1,1,11,
1, 1,1,1.5,0.5,12,
1,1,1,1,12
],)

salm_3_lyrics = Lyrics("""\
on kätte jõudnud aeg
ja maksnud olen ma
ei jää siin pidama
maksan eluaeg
pingutatud sai
ülemääragi
ja teada sedagi
jätkub see vaid\
""", [
1, 1.5,0.5,1,1,11,
1, 1.5,0.5,1,1,11,
1, 1.5,0.5,1,1,12,
1,1,1,1,12,
1,1,1,1,12,
1,1,1,1,11,
1, 1.5,0.5,1,1,12,
2,1,1,12
], -1)

ref_lyrics = Lyrics("""\
kas saaksin proovida veel
või ongi läbi mu tee\
""", [
3,3,2,3,3,2,16,
3,3,2,3,3,2,16
])

final_ref_lyrics = Lyrics("""\
ei saagi proovida veel
ongi nüüd läbi mu tee
ei saagi proovida veel
ongi nüüd läbi mu tee
""", [
4,2,2,4,2,2,16,
4,2,2,4,2,2,16,
4,2,2,4,2,2,16,
4,2,2,4,2,2,16
])

first_lead_spans_without_last = [
    ChordSpan(8, Chord.single_note(E6, 8)),
    ChordSpan(2, Chord.single_note(A5, 7)),
    ChordSpan(4, Chord.single_note(A5, 8)),
    ChordSpan(2, Chord.single_note(A5, 7)),
    ChordSpan(8, Chord.single_note(E6, 6)),    
]

first_lead_melody = [
    RhythmicChordSpanList(
        Rhythm([2,1,1,1,1,1,1, 2,2,2,2]),
        first_lead_spans_without_last + [
            ChordSpan(2, Chord.single_note(E6, 8)),
            ChordSpan(2, Chord.single_note(A5, 5)),
            ChordSpan(4, Chord.single_note(E6, 5))
        ] + first_lead_spans_without_last + [
            ChordSpan(2, Chord.single_note(A5, 5)),
            ChordSpan(2, Chord.single_note(E6, 8)),
            ChordSpan(2, Chord.single_note(E6, 5))
        ]
    ),
    RepeatingChordSpan(1, Chord.single_note(E6, 5), 10),
    RepeatingChordSpan(2, Chord.single_note(E6, 5)),
    RepeatingChordSpan(1, Chord.single_note(E6, 5), 2),
    RepeatingChordSpan(2, Chord.single_note(E6, 5), 2)
]

second_lead_melody = [
    RhythmicChordSpanList(
        Rhythm([
            2,1,1,1,1,1,1, 2,2,2,2,
            2,1,1,1,1,1,1, 2,1,1,2,2
        ]),
        [
            ChordSpan(8, Chord.single_note(E6, 8)),
            ChordSpan(2, Chord.single_note(A5, 5)),
            ChordSpan(4, Chord.single_note(A5, 7)),
            ChordSpan(2, Chord.single_note(A5, 5)),
            ChordSpan(8, Chord.single_note(E6, 6)),
            ChordSpan(4, Chord.single_note(A5, 7)),
            ChordSpan(2, Chord.single_note(A5, 8)),
            ChordSpan(2, Chord.single_note(A5, 7)),
        ] * 2
    ),
    RepeatingChordSpan(8, Chord.single_note(A5, 7))
]

third_lead_melody = [
    RhythmicChordSpanList(
        Rhythm([1]),
        [
            ChordSpan(8, Chord.single_note(E6, 8)),
            ChordSpan(8, Chord.single_note(A5, 10)),
            ChordSpan(8, Chord.single_note(A5, 8)),
            ChordSpan(8, Chord.single_note(A5, 7)),
        ] * 2 + [
            ChordSpan(4, Chord.single_note(A5, 10)),
            ChordSpan(2, Chord.single_note(A5, 8)),
            ChordSpan(2, Chord.single_note(A5, 10)),
            ChordSpan(8, Chord.single_note(E6, 8)),
            ChordSpan(4, Chord.single_note(A5, 8)),
            ChordSpan(2, Chord.single_note(A5, 7)),
            ChordSpan(2, Chord.single_note(A5, 8)),
            ChordSpan(8, Chord.single_note(E6, 5)),
        ] * 2
    )
]

esimene_salm_lead = [
    RhythmicChordSpanList(
        Rhythm(
            [7, 0.5,0.5, 1,0.5,0.5, 1,0.5,0.5, 4],
            [StrumStyle.NO_HIT] * 7 + [StrumStyle.PALM_MUTED] * 9
        ),
        [
            ChordSpan(8, Chord.single_note(B2, 3)),
            ChordSpan(8, Chord.single_note(G3, 3)),
            ChordSpan(8, Chord.single_note(B2, 1)),
            ChordSpan(8, Chord.single_note(B2, 3)),
            ChordSpan(9, Chord.single_note(B2, 3)),
            ChordSpan(7, Chord.single_note(G3, 3)),
            ChordSpan(8, Chord.single_note(B2, 1)),
        ]
    ),
    RhythmicChordSpanList(
        Rhythm(
            [1,2,2,1,2],
            [StrumStyle.PALM_MUTED] * 8
        ),
        [
            ChordSpan(1, Chord.single_note(B2, 1)),
            ChordSpan(5, Chord.single_note(B2, 3)),
            ChordSpan(2, Chord.single_note(B2, 6)),
        ]
    ),
    RhythmicChordSpanList(
        Rhythm(
            [7, 0.5,0.5, 1,2,2,1,2],
            [StrumStyle.NO_HIT] * 7 + [StrumStyle.PALM_MUTED] * 9
        ),
        [
            ChordSpan(9, Chord.single_note(B2, 3)),
            ChordSpan(7, Chord.single_note(G3, 3)),
            ChordSpan(9, Chord.single_note(B2, 1)),
            ChordSpan(7, Chord.single_note(B2, 3)),
        ] * 2
    )
]

CHORD_GB_23 = Chord(None, 3, 2, None, None, None)
CHORD_GB_33 = Chord(None, 3, 3, None, None, None)
CHORD_GB_01 = Chord(None, 1, 0, None, None, None)

teine_salm_lead_chordspans = [
    ChordSpan(9, CHORD_GB_23),
    ChordSpan(7, CHORD_GB_33),
    ChordSpan(9, CHORD_GB_01),
    ChordSpan(7, CHORD_GB_23)
] * 2

teine_salm_lead = [
    RhythmicChordSpanList(
        Rhythm(
            [8, 1, 2, 2, 1, 2] * 3 +
            [8, 1, 2, 1, 1, 1, 2],
            [StrumStyle.NO_HIT] * 8 + [StrumStyle.PALM_MUTED] * 8
        ),
        teine_salm_lead_chordspans
    ),
    RhythmicChordSpanList(
        Rhythm(
            [
                7, 0.5,0.5, 1, 1, 1, 1, 1, 1, 2,
                7, 0.5,0.5, 1, 2, 2, 1, 2,
                7, 0.5,0.5, 1, 2, 2, 1, 2,
                7, 0.5,0.5, 1, 1, 1, 1, 1, 1, 2
            ],
            [StrumStyle.NO_HIT] * 7 + [StrumStyle.PALM_MUTED] * 9
        ),
        teine_salm_lead_chordspans
    )
]

CHORD_GBE_231 = Chord(1, 3, 2, None, None, None)
CHORD_GBE_331 = Chord(1, 3, 3, None, None, None)
CHORD_GBE_010 = Chord(0, 1, 0, None, None, None)

kolmas_salm_lead_chordspans = [
    ChordSpan(9, CHORD_GBE_231),
    ChordSpan(7, CHORD_GBE_331),
    ChordSpan(9, CHORD_GBE_010),
    ChordSpan(7, CHORD_GBE_231)
] * 2

kolmas_salm_lead = [
    RhythmicChordSpanList(
         Rhythm(
            [7, 1, 1, 2, 2, 1, 2] * 3 +
            [7, 1, 1, 2, 1, 1, 1, 2],
            [StrumStyle.NO_HIT] * 7 + [StrumStyle.PALM_MUTED] * 9
        ),
        kolmas_salm_lead_chordspans * 2
    )
]

last_chorus_lead = [
    RepeatingChordSpan(3, Chord.single_note(A5, 8)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(3, Chord.single_note(E6, 10)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(16, Chord.single_note(E6, 5)),
    RepeatingChordSpan(3, Chord.single_note(A5, 8)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(3, Chord.single_note(E6, 10)),
    RepeatingChordSpan(3, Chord.single_note(E6, 6)),
    RepeatingChordSpan(2, Chord.single_note(E6, 5)),
    RepeatingChordSpan(16, Chord.single_note(E6, 5)),
] * 2 + [
    RepeatingChordSpan(3, Chord.single_note(A5, 8)),
    RepeatingChordSpan(5, Chord.single_note(E6, 5)),
    RepeatingChordSpan(2, Chord.single_note(A5, 5)),
    RepeatingChordSpan(6, Chord.no_strings_hit_chord())
]

FIRST_INTRO = Segment("INTRO PIKA LÕPUGA", {
    RHYTHM: rhythm_first_intro_parts,
    BASS:   bass_first_intro_parts,
    LEAD: first_lead_melody
})

SECOND_INTRO = Segment("INTRO LÜHEMA LÕPUGA", {
    RHYTHM: rhythm_second_intro_parts,
    BASS:   bass_second_intro_parts,
    LEAD: second_lead_melody
})

THIRD_INTRO = Segment("DOUBLE INTRO", {
    RHYTHM: rhythm_third_intro_parts,
    BASS:   bass_third_intro_parts,
    LEAD: third_lead_melody
})

SALM_1 = Segment("ESIMENE SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS:   bass_salm_parts,
    LEAD: esimene_salm_lead
}, lyrics=salm_1_lyrics)

SALM_2 = Segment("TEINE SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS:   bass_salm_parts,
    LEAD: teine_salm_lead
}, lyrics=salm_2_lyrics)

VIIMANE_SALM = Segment("VIIMANE SALM", {
    RHYTHM: rhythm_viimane_salm_parts,
    BASS:   bass_viimane_salm_parts,
    LEAD: kolmas_salm_lead
}, lyrics=salm_3_lyrics)

CHORUS_1 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
    LEAD: None
}, lyrics=ref_lyrics)

CHORUS_2 = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus_parts,
    BASS:   bass_chorus_parts,
    LEAD: None
}, lyrics=ref_lyrics)

VIIMANE_CHORUS = Segment("VIIMANE REFRÄÄN", {
    RHYTHM: rhythm_viimane_chorus_parts,
    BASS:   bass_viimane_chorus_parts,
    LEAD: last_chorus_lead
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