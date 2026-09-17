"""Combination generation for FDCT, with explosion protection."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from fdct.confusables import get_alternatives
from fdct.utils import CharInfo

DEFAULT_MAX_COMBINATIONS = 100_000


class CombinationLimitExceeded(Exception):
    """Raised when the theoretical combination count exceeds the safety limit.

    Carries the theoretical count so the caller (e.g. the CLI) can inform
    the user and decide whether to proceed anyway.
    """

    def __init__(self, theoretical_count: int, limit: int):
        self.theoretical_count = theoretical_count
        self.limit = limit
        super().__init__(
            f"Theoretical combination count ({theoretical_count:,}) exceeds "
            f"the safety limit ({limit:,})."
        )


@dataclass
class GenerationPlan:
    """The per-letter alternatives and theoretical size for a word."""

    word: str
    letter_alternatives: list[list[CharInfo]]

    @property
    def theoretical_count(self) -> int:
        count = 1
        for alternatives in self.letter_alternatives:
            count *= len(alternatives)
        return count


def build_plan(word: str) -> GenerationPlan:
    """Build a GenerationPlan for `word` without generating combinations yet.

    This lets the caller inspect the theoretical combination count before
    committing to generation, which is required for explosion protection.
    """
    letter_alternatives = [get_alternatives(letter) for letter in word]
    return GenerationPlan(word=word, letter_alternatives=letter_alternatives)


def generate_combinations(
    plan: GenerationPlan,
    max_combinations: int = DEFAULT_MAX_COMBINATIONS,
    force: bool = False,
) -> list[str]:
    """Generate all confusable combinations for the given plan.

    Raises CombinationLimitExceeded if the theoretical count exceeds
    `max_combinations` and `force` is False. Combinations are generated
    lazily via itertools.product and only materialized into a list here,
    after the safety check has passed.
    """
    theoretical = plan.theoretical_count
    if theoretical > max_combinations and not force:
        raise CombinationLimitExceeded(theoretical, max_combinations)

    char_options = [[info.char for info in alternatives] for alternatives in plan.letter_alternatives]
    return ["".join(combo) for combo in itertools.product(*char_options)]


def iter_combinations(plan: GenerationPlan):
    """Lazily yield combinations without materializing them all in memory.

    Useful for streaming very large (but user-approved) generations
    directly to a file or terminal without holding everything in RAM.
    """
    char_options = [[info.char for info in alternatives] for alternatives in plan.letter_alternatives]
    for combo in itertools.product(*char_options):
        yield "".join(combo)
