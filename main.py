#!/usr/bin/env python3
"""FDCT - Font/Character Deception Tool.

A Unicode homoglyph/confusable character generator, built to study and
demonstrate how visually similar Unicode characters (homoglyphs) can be
combined to create deceptive lookalike text. See README.md for details.

Run with: python main.py
"""

from __future__ import annotations

import sys

from fdct.confusables import all_letters_with_confusables
from fdct.generator import (
    DEFAULT_MAX_COMBINATIONS,
    CombinationLimitExceeded,
    build_plan,
    generate_combinations,
)
from fdct.output import DEFAULT_FILENAME, format_results_for_terminal, save_results
from fdct.validator import InvalidInputError, validate_word

BANNER = """\
========================================
              FDCT
     Unicode Confusable Generator
========================================
"""

MENU = """\
1. Generate
2. Character information
3. About
4. Exit
"""

ABOUT_TEXT = """\
FDCT (Font/Character Deception Tool) generates Unicode "homoglyph" or
"confusable" variants of a lowercase English word - strings that use
visually similar but distinct Unicode characters in place of one or
more original Latin letters.

This exists to study and demonstrate Unicode homoglyph risks (e.g. in
usernames, domains, or displayed text), not to target any real system.
Two strings can look identical on screen while being completely
different sequences of code points. See README.md for more detail.
"""


def prompt_word() -> str | None:
    print("Enter lowercase word (or leave blank to cancel):")
    word = input("> ").strip()
    if word == "":
        return None
    return word


def run_generate() -> None:
    word = prompt_word()
    if word is None:
        return

    try:
        word = validate_word(word)
    except InvalidInputError as exc:
        print(f"[!] Invalid input: {exc}")
        return

    print("[+] Input accepted")
    plan = build_plan(word)
    theoretical = plan.theoretical_count
    print(f"[+] Confusable analysis completed")
    print(f"[+] Theoretical combinations: {theoretical:,}")

    force = False
    if theoretical > DEFAULT_MAX_COMBINATIONS:
        print(
            f"[!] Warning: this exceeds the default safety limit of "
            f"{DEFAULT_MAX_COMBINATIONS:,}."
        )
        answer = input("Generate anyway? This may use significant memory. [y/N]: ").strip().lower()
        if answer != "y":
            print("[-] Generation cancelled.")
            return
        force = True

    try:
        results = generate_combinations(plan, force=force)
    except CombinationLimitExceeded as exc:
        # Should not happen given the check above, but handled defensively.
        print(f"[!] {exc}")
        return

    print(f"[+] Combinations: {len(results)}")
    print()
    print(format_results_for_terminal(word, results))

    save_answer = input("\nDo you want to save the results to a text file? [y/n]: ").strip().lower()
    if save_answer == "y":
        filename = input(
            f"Filename (press Enter for default '{DEFAULT_FILENAME}'): "
        ).strip()
        if filename == "":
            filename = DEFAULT_FILENAME
        path = save_results(word, results, filename)
        print(f"[+] Results saved to: {path.resolve()}")


def run_character_info() -> None:
    print("Enter a lowercase letter to inspect its confusables (a-z):")
    letter = input("> ").strip()
    if len(letter) != 1 or not ("a" <= letter <= "z"):
        print("[!] Please enter exactly one lowercase letter a-z.")
        return

    alternatives = all_letters_with_confusables()[letter]
    print(f"\nConfusable characters for '{letter}':\n")
    for info in alternatives:
        print(str(info))
        print("-" * 40)


def run_about() -> None:
    print(ABOUT_TEXT)


def main() -> int:
    print(BANNER)
    while True:
        print(MENU)
        choice = input("> ").strip()
        print()
        if choice == "1":
            run_generate()
        elif choice == "2":
            run_character_info()
        elif choice == "3":
            run_about()
        elif choice == "4":
            print("Goodbye.")
            return 0
        else:
            print("[!] Invalid menu choice. Please enter 1-4.")
        print()


if __name__ == "__main__":
    sys.exit(main())
