from dataclasses import dataclass, field


@dataclass
class SongSection:
    """One structural section of a song, with optional lyrics.

    title   – the canonical section name shown on the title page
    lyrics  – the lyrics for this section, or None if instrumental
    """
    title:  str
    lyrics: str | None = None