"""Small Unicode helper utilities used throughout FDCT."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

# Approximate Unicode block ranges for scripts that commonly appear
# among confusable characters for Latin letters. This is intentionally
# a small, targeted table (not a full Unicode script database) since
# FDCT only needs to label the scripts of characters it actually uses.
_SCRIPT_RANGES: list[tuple[int, int, str]] = [
    (0x0041, 0x007A, "Latin"),
    (0x00C0, 0x024F, "Latin Extended"),
    (0x0370, 0x03FF, "Greek"),
    (0x0400, 0x04FF, "Cyrillic"),
    (0x0500, 0x052F, "Cyrillic Supplement"),
    (0x0530, 0x058F, "Armenian"),
    (0x2100, 0x214F, "Letterlike Symbols"),
    (0x2150, 0x218F, "Number Forms"),
    (0x1D00, 0x1D7F, "Phonetic Extensions"),
    (0xFF00, 0xFFEF, "Halfwidth and Fullwidth Forms"),
]


def get_script(char: str) -> str:
    """Return a human-readable script/block name for a single character.

    Falls back to "Unknown" if the character does not fall into one of
    the ranges FDCT knows about.
    """
    codepoint = ord(char)
    for start, end, name in _SCRIPT_RANGES:
        if start <= codepoint <= end:
            return name
    return "Unknown"


def get_codepoint(char: str) -> str:
    """Return the Unicode code point of a character as 'U+XXXX'."""
    return f"U+{ord(char):04X}"


def get_unicode_name(char: str) -> str:
    """Return the official Unicode name of a character, or a placeholder."""
    try:
        return unicodedata.name(char)
    except ValueError:
        return "UNKNOWN CHARACTER NAME"


@dataclass(frozen=True)
class CharInfo:
    """Metadata describing a single character used in FDCT."""

    char: str
    codepoint: str
    name: str
    script: str
    is_original: bool

    def __str__(self) -> str:
        origin = "Original Latin" if self.is_original else "Replacement"
        return (
            f"Character: {self.char}\n"
            f"Code Point: {self.codepoint}\n"
            f"Unicode Name: {self.name}\n"
            f"Script: {self.script}\n"
            f"Type: {origin}"
        )


def build_char_info(char: str, is_original: bool) -> CharInfo:
    """Build a CharInfo record for a character, computing metadata live."""
    return CharInfo(
        char=char,
        codepoint=get_codepoint(char),
        name=get_unicode_name(char),
        script=get_script(char),
        is_original=is_original,
    )
