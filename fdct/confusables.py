"""Loading and lookup of the Unicode confusables database used by FDCT.

The database (data/confusables.json) maps each lowercase Latin letter
to a curated list of Unicode characters that are visually confusable
with it. Metadata (code point, Unicode name, script) is computed live
via fdct.utils rather than hard-coded, so it can never drift out of
sync with the actual character.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from fdct.utils import CharInfo, build_char_info

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "confusables.json"


class ConfusablesDatabaseError(RuntimeError):
    """Raised when the confusables database cannot be loaded or is invalid."""


@lru_cache(maxsize=1)
def _load_raw_database(path: Path = _DATA_PATH) -> dict[str, list[str]]:
    if not path.exists():
        raise ConfusablesDatabaseError(f"Confusables database not found at: {path}")
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ConfusablesDatabaseError(f"Confusables database is not valid JSON: {exc}") from exc

    for letter in "abcdefghijklmnopqrstuvwxyz":
        if letter not in data or not isinstance(data[letter], list):
            raise ConfusablesDatabaseError(
                f"Confusables database is missing or malformed for letter '{letter}'."
            )
    return data


def get_alternatives(letter: str) -> list[CharInfo]:
    """Return all available alternatives for a single lowercase letter.

    The list always starts with the original Latin letter itself,
    followed by its curated Unicode confusables (deduplicated).
    """
    if len(letter) != 1 or not ("a" <= letter <= "z"):
        raise ValueError(f"get_alternatives expects a single lowercase a-z letter, got: {letter!r}")

    raw = _load_raw_database()
    seen: set[str] = {letter}
    alternatives: list[CharInfo] = [build_char_info(letter, is_original=True)]

    for confusable_char in raw.get(letter, []):
        if confusable_char in seen:
            continue
        seen.add(confusable_char)
        alternatives.append(build_char_info(confusable_char, is_original=False))

    return alternatives


def all_letters_with_confusables() -> dict[str, list[CharInfo]]:
    """Return the full alternatives mapping for every letter a-z."""
    return {letter: get_alternatives(letter) for letter in "abcdefghijklmnopqrstuvwxyz"}
