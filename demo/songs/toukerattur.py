from tabfromtext.song.Chord import Chord
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.GuitarString import E6, A5, D4, G3, B2, E1
from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.RhythmicChordSpanList import RhythmicChordSpanList
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.RepeatingChordSpan import RepeatingChordSpan


RHYTHM = "Rhythm"
BASS = "Bass"
LEAD = "Lead"

CHORD_E6 = Chord.power_chord(E6, 6)
CHORD_A9 = Chord.power_chord(A5, 9)
CHORD_A8 = Chord.power_chord(A5, 8)

leebe_rhythm = Rhythm(
    [
        1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,
    ],
    [StrumStyle.NORMAL] * 8 +
    [StrumStyle.NORMAL, StrumStyle.NO_HIT] * 4 +            
    [StrumStyle.NORMAL] * 8 +
    [StrumStyle.NORMAL] * 8
)

hard_rhythm = Rhythm(
    [
        1,1,1,2,1,1,1,
        1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,
    ],
    [StrumStyle.NORMAL] * 2 + [StrumStyle.MUTED] + [StrumStyle.NORMAL] * 5 +
    [StrumStyle.NORMAL, StrumStyle.NO_HIT] * 4 +            
    [StrumStyle.NORMAL] * 8 +
    [StrumStyle.NORMAL] * 8
)

riff_end = [
    RhythmicChordSpanList(
        Rhythm(
            [
                1,1,1,2,1,1,1,
                1,1,1,2,1,1,1,
                1,1,1,2,1,1,1,
                1,1,1,2,1,1,1
            ],
            [StrumStyle.NORMAL] * 2 + [StrumStyle.MUTED] + [StrumStyle.NORMAL] * 5 +
            [StrumStyle.NORMAL] * 24
        ),
        [
            ChordSpan(32, CHORD_E6),
        ]
    )
]

riff_chords = [
    ChordSpan(16, CHORD_E6),
    ChordSpan(8, CHORD_A9),
    ChordSpan(8, CHORD_A8)
]

intro_riff = [
    RhythmicChordSpanList(
        hard_rhythm,
        riff_chords
    )
] + [
    RhythmicChordSpanList(
        leebe_rhythm,
        riff_chords
    )
] * 2 + riff_end

chorus_riff = [
    RhythmicChordSpanList(
        leebe_rhythm,
        riff_chords
    )
] * 3 + riff_end

long_chorus_riff = [
    RhythmicChordSpanList(
        leebe_rhythm,
        riff_chords
    )
] * 3 + [
    RhythmicChordSpanList(
        Rhythm(
            [
                1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,
                2,2,1,1,1,1
            ],
            [StrumStyle.NORMAL] * 8 +
            [StrumStyle.NORMAL, StrumStyle.NO_HIT] * 4 +            
            [StrumStyle.NORMAL] * 8 +
            [StrumStyle.NORMAL] * 4 +
            [StrumStyle.MUTED] + [StrumStyle.NORMAL] * 3
        ),
        riff_chords
    ),
    RhythmicChordSpanList(
        Rhythm(
            [1,1,1,1,1,1,1,1],
            [StrumStyle.NORMAL, StrumStyle.NO_HIT] +
            [StrumStyle.NORMAL] * 6
        ),
        [ ChordSpan(32, CHORD_E6)]
    ),
    RepeatingChordSpan(2, CHORD_E6),
    RepeatingChordSpan(6, Chord.no_strings_hit_chord()),
    RepeatingChordSpan(8, Chord.no_strings_hit_chord(), 3),
]

salm = [
    RepeatingChordSpan(1, CHORD_E6, 24),
    RepeatingChordSpan(1, CHORD_A9, 2),
    RepeatingChordSpan(1, CHORD_A9, 1, StrumStyle.MUTED),
    RepeatingChordSpan(3, CHORD_A8),
    RepeatingChordSpan(2, CHORD_A8)
] * 4

break_and_solo = [
    RepeatingChordSpan(1, CHORD_E6, 16),
    RepeatingChordSpan(1, CHORD_A8, 4),
    RepeatingChordSpan(1, CHORD_A9, 4),
    RepeatingChordSpan(1, CHORD_A8, 4),
    RepeatingChordSpan(1, CHORD_A9, 4)
] * 4 + [
    RepeatingChordSpan(1, CHORD_E6, 64),
    RepeatingChordSpan(64, CHORD_E6, 1, StrumStyle.VIBRATO),
    RepeatingChordSpan(2, CHORD_E6, 1, StrumStyle.MUTED),
    RepeatingChordSpan(6, Chord.no_strings_hit_chord())
]

main_riff_bass_piece = [
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 9),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 1, StrumStyle.NO_HIT),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 1),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 1, StrumStyle.NO_HIT),
    RepeatingChordSpan(2, Chord.single_note(A5, 1), 2),

    RepeatingChordSpan(1, Chord.single_note(E6, 2), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 1), 8),
]

main_riff_bass = main_riff_bass_piece * 3 + [
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 24),
    RepeatingChordSpan(1, Chord.single_note(A5, 4), 3),
    RepeatingChordSpan(1, Chord.single_note(A5, 3), 5),
]

long_riff_bass = main_riff_bass_piece * 4 + [
    RepeatingChordSpan(2, Chord.single_note(A5, 1)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 6),
] * 4 + [    
    RepeatingChordSpan(14, Chord.single_note(A5, 1)),
    RepeatingChordSpan(2, Chord.single_note(A5, 1)),

    RepeatingChordSpan(3, Chord.single_note(A5, 4)),
    RepeatingChordSpan(3, Chord.single_note(A5, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 4)),
    RepeatingChordSpan(2, Chord.single_note(A5, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 4)),
    RepeatingChordSpan(2, Chord.single_note(A5, 3)),
]

salm_bass = [
    RepeatingChordSpan(1, Chord.single_note(G3, 3), 24),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 3),
    RepeatingChordSpan(3, Chord.single_note(D4, 3)),
    RepeatingChordSpan(2, Chord.single_note(D4, 3))
] * 3 + [
    RepeatingChordSpan(1, Chord.single_note(G3, 3), 24),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 3),
    RepeatingChordSpan(1, Chord.single_note(D4, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 1), 1, StrumStyle.NO_HIT),
    RepeatingChordSpan(1, Chord.single_note(D4, 3)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 1, StrumStyle.NO_HIT)
]

end_bass = [
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 16),
    RepeatingChordSpan(1, Chord.single_note(D4, 3), 4),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 4),
    RepeatingChordSpan(1, Chord.single_note(D4, 3), 4),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 4)
] * 4 + [
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 64),

    RepeatingChordSpan(6, Chord.single_note(A5, 1)),
    RepeatingChordSpan(2, Chord.single_note(A5, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 4)),
    RepeatingChordSpan(4, Chord.single_note(A5, 3)),
    RepeatingChordSpan(1, Chord.single_note(D4, 3), 2),
    
    RepeatingChordSpan(3, Chord.single_note(D4, 4)),
    RepeatingChordSpan(3, Chord.single_note(D4, 3)),
    RepeatingChordSpan(2, Chord.single_note(D4, 4)),
    RepeatingChordSpan(6, Chord.single_note(A5, 1)),
    RepeatingChordSpan(2, Chord.single_note(A5, 1)),

    RepeatingChordSpan(3, Chord.single_note(E6, 2)),
    RepeatingChordSpan(3, Chord.single_note(E6, 1)),
    RepeatingChordSpan(2, Chord.single_note(E6, 2)),
    RepeatingChordSpan(3, Chord.single_note(A5, 1)),
    RepeatingChordSpan(3, Chord.single_note(A5, 3)),
    RepeatingChordSpan(2, Chord.single_note(A5, 4)),
    
    RepeatingChordSpan(3, Chord.single_note(A5, 3)),
    RepeatingChordSpan(3, Chord.single_note(A5, 4)),
    RepeatingChordSpan(2, Chord.single_note(A5, 3)),
    RepeatingChordSpan(14, Chord.single_note(A5, 1)),
    RepeatingChordSpan(2, Chord.no_strings_hit_chord()),
]

intro_lead_main_thing = [
    RepeatingChordSpan(1, Chord.single_note(D4, 8), 3),
    RepeatingChordSpan(1, Chord.single_note(B2, 6), 5),
] * 2 + [
    RepeatingChordSpan(1, Chord.single_note(G3, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(G3, 5), 4),
    RepeatingChordSpan(1, Chord.single_note(G3, 6), 3),
]

intro_lead = intro_lead_main_thing + [
    RepeatingChordSpan(2, Chord.single_note(G3, 8)),
    RepeatingChordSpan(1, Chord.single_note(G3, 6)),
    RepeatingChordSpan(1, Chord.single_note(G3, 5)),
    RepeatingChordSpan(1, Chord.single_note(D4, 8)),
] + intro_lead_main_thing + [
    RepeatingChordSpan(3, Chord.single_note(G3, 8)),
    RepeatingChordSpan(2, Chord.single_note(G3, 8)),
] + intro_lead_main_thing + [
    RepeatingChordSpan(3, Chord.single_note(G3, 8)),
    RepeatingChordSpan(2, Chord.single_note(B2, 6)),

    RepeatingChordSpan(1, Chord.single_note(G3, 6)),
    RepeatingChordSpan(1, Chord.single_note(D4, 8), 3),
    RepeatingChordSpan(1, Chord.single_note(G3, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(G3, 5), 2),
    RepeatingChordSpan(1, Chord.single_note(G3, 6)),
    RepeatingChordSpan(3, Chord.single_note(D4, 8)),
    RepeatingChordSpan(2, Chord.single_note(D4, 8)),
    
    RepeatingChordSpan(2, Chord.single_note(D4, 8)),
    RepeatingChordSpan(1, Chord.single_note(D4, 8), 5),
    RepeatingChordSpan(1, Chord.single_note(G3, 5)),
    RepeatingChordSpan(1, Chord.single_note(G3, 6), 2),
    RepeatingChordSpan(1, Chord.single_note(G3, 5)),
    RepeatingChordSpan(3, Chord.single_note(G3, 5), 1, StrumStyle.VIBRATO),
    RepeatingChordSpan(2, Chord.single_note(D4, 8))
]

chorus_lead_main_part_first = [
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
] * 2
#+ [
#    RepeatedChordSpan(1, Chord.single_note(E6, 6)),
#    RepeatedChordSpan(1, Chord.single_note(E6, 6), 1, StrumStyle.NO_HIT),
#] * 4

chorus_lead_main_part = chorus_lead_main_part_first + [
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 8), 8),
]

chorus_lead = chorus_lead_main_part * 2 + chorus_lead_main_part_first + [
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 8),
    RepeatingChordSpan(8, Chord.single_note(E6, 8)),
] + [
    RepeatingChordSpan(3, Chord.single_note(E6, 6), 2),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(3, Chord.single_note(E6, 9)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),

    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(4, Chord.single_note(E6, 6)),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(3, Chord.single_note(E6, 9)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
]

long_chorus_lead = chorus_lead_main_part * 3 + chorus_lead_main_part_first + [
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 8),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),
    
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 6),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 8), 2),
    
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 8), 5),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 7),

    RepeatingChordSpan(6, Chord.single_note(E6, 6)),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),
    
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 8), 2, StrumStyle.VIBRATO),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
]

end_lead = (chorus_lead_main_part_first + [
    RepeatingChordSpan(1, Chord.single_note(E6, 8), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 4),
] * 2) * 4 + [
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.power_chord(E6, 6), 3),
    RepeatingChordSpan(2, Chord.power_chord(E6, 6)),
    RepeatingChordSpan(1, Chord.power_chord(E6, 6), 3),
] * 4 + [
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 1, StrumStyle.SLIDE),
    RepeatingChordSpan(1, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),    
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),

    RepeatingChordSpan(6, Chord.single_note(E6, 8)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    RepeatingChordSpan(4, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 2),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    
    RepeatingChordSpan(3, Chord.single_note(E6, 9)),
    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(2, Chord.single_note(E6, 9)),

    RepeatingChordSpan(2, Chord.single_note(E6, 9)),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 2),
    
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 9), 3),

    RepeatingChordSpan(3, Chord.single_note(E6, 8)),
    RepeatingChordSpan(3, Chord.single_note(E6, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 8)),
    RepeatingChordSpan(8, Chord.single_note(E6, 6)),

    RepeatingChordSpan(2, Chord.single_note(E6, 6), 1, StrumStyle.MUTED),
    RepeatingChordSpan(6, Chord.no_strings_hit_chord()),
]

first_salm_lead = [
    RepeatingChordSpan(8, Chord.no_strings_hit_chord(), 3),
    RepeatingChordSpan(3, Chord.single_note(E1, 9)),
    RepeatingChordSpan(3, Chord.single_note(E1, 8)),
    RepeatingChordSpan(2, Chord.single_note(E1, 9)),
] * 2 + [
    RhythmicChordSpanList(
        Rhythm([2,2,2,2,2,1,3,2]),
        [
            ChordSpan(24, Chord.single_note(E1, 6)),
            ChordSpan(3, Chord.single_note(E1, 9)),
            ChordSpan(3, Chord.single_note(E1, 8)),
            ChordSpan(2, Chord.single_note(E1, 9)),
        ] * 2
    )
]

teine_salm_lead = [
    RepeatingChordSpan(8, Chord.no_strings_hit_chord()),
    RepeatingChordSpan(3, Chord.single_note(E1, 8)),
    RepeatingChordSpan(3, Chord.single_note(E1, 9)),
    RepeatingChordSpan(2, Chord.single_note(E1, 8)),

    RepeatingChordSpan(8, Chord.single_note(E1, 6)),
    RepeatingChordSpan(2, Chord.single_note(E1, 8)),
    RepeatingChordSpan(1, Chord.single_note(E1, 9), 1, StrumStyle.SLIDE),
    RepeatingChordSpan(3, Chord.single_note(E1, 8)),
    RepeatingChordSpan(2, Chord.single_note(E1, 9)),
] * 2 + [
    RhythmicChordSpanList(
        Rhythm([2,2,1,1,1,1,2,1,3,2]),
        [
            ChordSpan(24, Chord.single_note(E1, 6)),
            ChordSpan(3, Chord.single_note(E1, 9)),
            ChordSpan(3, Chord.single_note(E1, 8)),
            ChordSpan(2, Chord.single_note(E1, 9)),
        ] * 2
    )
]


INTRO = Segment("INTRO", {
    RHYTHM: intro_riff,
    BASS: main_riff_bass,
    LEAD: intro_lead
})

CHORUS = Segment("REFRÄÄN", {
    RHYTHM: chorus_riff,
    BASS: main_riff_bass,
    LEAD: chorus_lead

}, Lyrics(
"""\
tõukerattur
tõukerattur
tõukerattur\
""", [
    2,2,2,2 + 3*8,
    2,2,2,2 + 3*8,
    2,2,2,2
], 8))

PIKK_CHORUS = Segment("REFRÄÄN PIKA LÕPUGA", {
    RHYTHM: long_chorus_riff,
    BASS: long_riff_bass,
    LEAD: long_chorus_lead
}, Lyrics(
"""\
tõukerattur
tõukerattur
tõukerattur
tõukerattur\
""", [
    2,2,2,2 + 3*8,
    2,2,2,2 + 3*8,
    2,2,2,2 + 3*8,
    2,2,2,2
], 8))

ESIMENE_SALM = Segment("SALM", {
    RHYTHM: salm,
    BASS: salm_bass,
    LEAD: first_salm_lead
}, Lyrics(
    """\
jalutasin ma ükskord mööda linna
vastu tuli tõuke-e-
ratas millega andis minna
mees kelle joogiseis oli
mätas, kaldus siia sinna
löök-august päike koitis
mind ei näind sain löögi ninna
kui mees mulle otsa sõitis\
""", [
    1,1,1,1, 2,1,1, 3,1,3,1,
    2,2,1,3, 3,3,2,
    2,2,1,1,2, 3,1,3,1,
    2,2,2,1,1, 3,3,2,
    2,2,2,2,2,1,3,2,
    4,1,3,2,1,3,2,
    2,2,2,2,1,2,3,2,
    2,2,2,2,2,1,3,2
]))

TEINE_SALM = Segment("SALM", {
    RHYTHM: salm,
    BASS: salm_bass,
    LEAD: teine_salm_lead
}, Lyrics(
    """\
linnavalitsuse mehed
vaatasin tulid meile vastu
kuid pettumus on minul ehe
asjal ongi minna lastud
mees sai vabalt otsejoones
oma koju sõita-a
ent ülbe jalakäija toores
pandi kohe paika-a\
""", [
    1,1,1,1,2,2, 1,7,
    2,1,1,1,3, 2,1,3,2,
    2,1.5,0.5,2,2, 1,2,1,4,
    2,2,2,2, 2,1,3,2,
    2,2,1,3,2,1,3,2,
    1,3,1,3,3,3,2,
    2,1.5,0.5,1,3,3,1,3,1,
    2,2,1,3, 3,3,2
]))

BREAK_AND_END = Segment("SOOLO + LÕPP", {
    RHYTHM: break_and_solo,
    BASS: end_bass,
    LEAD: end_lead
}, Lyrics(
    """\
hehe vaata mind ma sõidan tõukerattaga, hahaha
ma olen nii lahe, ma libisen mööda maad, haha!\
""", None, 64))

SONG = Song("Tõukerattur", [
    INTRO,
    ESIMENE_SALM,
    CHORUS, # sama mis intro
    TEINE_SALM,
    PIKK_CHORUS,
    BREAK_AND_END
], """\
kuradi värdjad jätavad oma rattaid igale poole vedelema nahhui
putsi raisk ja siis nad veel ülbitsevad nagu nad omaksid liiklust vä
fucking värdjad ajuhälvikud ma räägin, mingid munnitürapead kõik koos
haiged elukad need kuradi... tõukeratturid
""")