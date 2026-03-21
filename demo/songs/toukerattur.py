from tabfromtext.song.Chord import Chord
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.GuitarString import GuitarString
from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.RhythmicChordSpan import RhythmicChordSpan
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.StrummedChordSpan import StrummedChordSpan


RHYTHM = "Rhythm"
BASS = "Bass"
LEAD = "Lead"

CHORD_E6 = Chord.power_chord(GuitarString.E6, 6)
CHORD_A9 = Chord.power_chord(GuitarString.A5, 9)
CHORD_A8 = Chord.power_chord(GuitarString.A5, 8)

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
    RhythmicChordSpan(
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
    RhythmicChordSpan(
        hard_rhythm,
        riff_chords
    )
] + [
    RhythmicChordSpan(
        leebe_rhythm,
        riff_chords
    )
] * 2 + riff_end

chorus_riff = [
    RhythmicChordSpan(
        leebe_rhythm,
        riff_chords
    )
] * 3 + riff_end

long_chorus_riff = [
    RhythmicChordSpan(
        leebe_rhythm,
        riff_chords
    )
] * 3 + [
    RhythmicChordSpan(
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
    RhythmicChordSpan(
        Rhythm(
            [1,1,1,1,1,1,1,1],
            [StrumStyle.NORMAL, StrumStyle.NO_HIT] +
            [StrumStyle.NORMAL] * 6
        ),
        [ ChordSpan(32, CHORD_E6)]
    ),
    StrummedChordSpan(2, CHORD_E6),
    StrummedChordSpan(6, Chord.no_strings_hit_chord()),
    StrummedChordSpan(8, Chord.no_strings_hit_chord(), 3),
]

salm = [
    StrummedChordSpan(1, CHORD_E6, 24),
    StrummedChordSpan(1, CHORD_A9, 2),
    StrummedChordSpan(1, CHORD_A9, 1, StrumStyle.MUTED),
    StrummedChordSpan(3, CHORD_A8),
    StrummedChordSpan(2, CHORD_A8)
] * 4

break_and_solo = [
    StrummedChordSpan(1, CHORD_E6, 16),
    StrummedChordSpan(1, CHORD_A8, 4),
    StrummedChordSpan(1, CHORD_A9, 4),
    StrummedChordSpan(1, CHORD_A8, 4),
    StrummedChordSpan(1, CHORD_A9, 4)
] * 4 + [
    StrummedChordSpan(1, CHORD_E6, 64),
    StrummedChordSpan(64, CHORD_E6, 1, StrumStyle.VIBRATO),
    StrummedChordSpan(2, CHORD_E6, 1, StrumStyle.MUTED),
    StrummedChordSpan(6, Chord.no_strings_hit_chord())
]

main_riff_bass_piece = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 9),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 1, StrumStyle.NO_HIT),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 1),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 1, StrumStyle.NO_HIT),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1), 2),

    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 2), 8),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E6, 1), 8),
]

main_riff_bass = main_riff_bass_piece * 3 + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 24),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3), 5),
]

long_riff_bass = main_riff_bass_piece * 4 + [
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 6),
] * 4 + [    
    StrummedChordSpan(14, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),

    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
]

salm_bass = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3), 24),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 4), 3),
    StrummedChordSpan(3, Chord.single_note(GuitarString.D4, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.D4, 3))
] * 3 + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3), 24),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 4), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1), 1, StrumStyle.NO_HIT),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 1, StrumStyle.NO_HIT)
]

end_bass = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 16),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 3), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 4), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 3), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 4), 4)
] * 4 + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 64),

    StrummedChordSpan(6, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(4, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.D4, 3), 2),
    
    StrummedChordSpan(3, Chord.single_note(GuitarString.D4, 4)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.D4, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.D4, 4)),
    StrummedChordSpan(6, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),

    StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 2)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.E6, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E6, 2)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(14, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.no_strings_hit_chord()),
]

intro_lead_main_thing = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E1, 1), 5),
] * 2 + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 1), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2), 3),
]

intro_lead = intro_lead_main_thing + [
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 4)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3)),
] + intro_lead_main_thing + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.B2, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 4)),
] + intro_lead_main_thing + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.B2, 4)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 1)),

    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2), 4),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 1), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 3)),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 3), 5),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 2), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 1)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.B2, 1), 1, StrumStyle.VIBRATO),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 3))
]

chorus_lead_main_part_first = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 3),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
] * 2
#+ [
#    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1)),
#    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 1, StrumStyle.NO_HIT),
#] * 4

chorus_lead_main_part = chorus_lead_main_part_first + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 8),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3), 8),
]

chorus_lead = chorus_lead_main_part * 2 + chorus_lead_main_part_first + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 8),
    StrummedChordSpan(8, Chord.single_note(GuitarString.A5, 3)),
] + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 1), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),

    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(4, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
]

long_chorus_lead = chorus_lead_main_part * 3 + chorus_lead_main_part_first + [
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 8),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 6),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3), 2),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3), 5),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1), 7),

    StrummedChordSpan(6, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 3),
    StrummedChordSpan(3, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 1)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 4), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.A5, 3), 2, StrumStyle.VIBRATO),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 3)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.A5, 4)),
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
    BASS: salm_bass
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
    2,2,2,2,3,1,3,1,
    4,1,3,2,1,3,2,
    2,2,2,2,1,3,3,1,
    2,2,2,2,2,1,3,2
]))

TEINE_SALM = Segment("SALM", {
    RHYTHM: salm,
    BASS: salm_bass
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
    BASS: end_bass
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