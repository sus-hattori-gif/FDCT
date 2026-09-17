"""Input validation for FDCT.

FDCT only accepts words made of lowercase English letters (a-z). This
module enforces that rule strictly and never silently normalizes or
transforms user input.
"""

from __future__ import annotations

import re

_VALID_WORD_PATTERN = re.compile(r"^[a-z]+$")


class InvalidInputError(ValueError):
    """Raised when the user-supplied word fails validation."""


def validate_word(word: str) -> str:
    """Validate that `word` consists solely of lowercase English letters.

    Returns the word unchanged if valid. Raises InvalidInputError with a
    clear, specific message otherwise. Input is never modified, stripped
    of case, or normalized here.
    """
    if word is None or len(word) == 0:
        raise InvalidInputError("Input cannot be empty.")

    if _VALID_WORD_PATTERN.match(word):
        return word

    # Give the most specific, helpful error message we can.
    if any(ch.isspace() for ch in word):
        raise InvalidInputError("Input must not contain spaces.")
    if any(ch.isdigit() for ch in word):
        raise InvalidInputError("Input must not contain numbers.")
    if any(ch.isupper() for ch in word):
        raise InvalidInputError(
            "Input must be lowercase only (uppercase letters are not allowed)."
        )

    # Anything else (punctuation, Persian/Arabic, or any other Unicode
    # character) is rejected with a generic but clear message.
    bad_chars = sorted({ch for ch in word if not ("a" <= ch <= "z")})
    raise InvalidInputError(
        "Input must contain only lowercase English letters (a-z). "
        f"Invalid character(s) found: {', '.join(repr(c) for c in bad_chars)}"
    )
