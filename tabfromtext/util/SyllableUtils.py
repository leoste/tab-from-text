from enum import Enum
from typing import Union


class Language(Enum):
    ESTONIAN = "estonian"


ESTONIAN_VOWELS = set("aeiouõäöü")

# Vowel pairs that always split into separate syllables.
# Add new pairs here as edge cases are discovered.
# For irregular words, manually hyphenate in the lyrics string instead.
ESTONIAN_VOWEL_SPLITS = {"ua", "ia", "iu", "ie"}


def _split_estonian(word: str) -> list[str]:
    """
    Split a single Estonian word into syllables.

    Rules applied:
      1. A syllable must contain at least one vowel.
      2. Splitting happens so that the next syllable starts with a consonant.
      3. If multiple consonants sit between two vowel groups, only the LAST
         consonant belongs to the next syllable; all preceding consonants
         stay in the current syllable.
         e.g. "korst-na" not "kors-tna", "püh-ki-ja" not "pü-hki-ja"
      4. Adjacent vowel pairs listed in ESTONIAN_VOWEL_SPLITS always split,
         e.g. "ua" -> u|a, "ia" -> i|a.
         Other adjacent vowel pairs (diphthongs) stay in the same syllable.

    Dashes are NOT added here — the caller (split_syllables) appends them.
    """
    word = word.lower()
    if not word:
        return []

    # Find indices of all vowels
    vowel_positions = [i for i, ch in enumerate(word) if ch in ESTONIAN_VOWELS]

    # No vowel → treat entire token as one syllable (e.g. "brr", abbreviations)
    if not vowel_positions:
        return [word]

    syllables = []
    start = 0

    for v_idx in range(len(vowel_positions) - 1):
        current_vowel_pos = vowel_positions[v_idx]
        next_vowel_pos    = vowel_positions[v_idx + 1]

        between = list(range(current_vowel_pos + 1, next_vowel_pos))
        consonants_between = [i for i in between if word[i] not in ESTONIAN_VOWELS]

        if not consonants_between:
            # Adjacent vowels — split only if the pair is in ESTONIAN_VOWEL_SPLITS
            pair = word[current_vowel_pos] + word[next_vowel_pos]
            if pair in ESTONIAN_VOWEL_SPLITS:
                split_at = next_vowel_pos
                syllables.append(word[start:split_at])
                start = split_at
            continue

        # Split point: last consonant in the gap starts the new syllable
        split_at = consonants_between[-1]
        syllables.append(word[start:split_at])
        start = split_at

    syllables.append(word[start:])
    syllables = [s for s in syllables if s]

    return syllables


def split_syllables(text: str, language: Union[Language, None] = None) -> list[str]:
    """
    Split *text* into syllables, inserting a trailing dash after each syllable
    that is followed by another syllable within the same word.

    Example (Estonian):
        "automation"  -> ["au-", "to-", "mati-", "on"]
        "keermelatt"  -> ["keer-", "me-", "latt"]
        "korstnapühkija" -> ["korst-", "na-", "püh-", "ki-", "ja"]

    Words are delimited by whitespace; spaces between words produce a plain
    space token so that the caller can tell word boundaries apart.

    :param text:     Input string (may be multi-word, may contain newlines).
    :param language: Language enum value. Defaults to Language.ESTONIAN.
                     Only Estonian is implemented; add new branches here for
                     other languages.
    :raises NotImplementedError: If a Language value other than ESTONIAN is
                                 passed (future-proofing for new languages).
    """
    if language is None:
        language = Language.ESTONIAN

    if language != Language.ESTONIAN:
        raise NotImplementedError(
            f"Syllable splitting is not yet implemented for {language}. "
            "Add a splitting function and a branch in split_syllables()."
        )

    result: list[str] = []

    for word in text.split():
        raw_syllables = _split_estonian(word)

        for i, syl in enumerate(raw_syllables):
            is_last_in_word = (i == len(raw_syllables) - 1)
            if is_last_in_word:
                result.append(syl)
            else:
                result.append(syl + "-")

    return result