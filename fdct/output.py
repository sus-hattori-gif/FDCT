"""Terminal display and file-saving for FDCT results."""

from __future__ import annotations

from pathlib import Path

DEFAULT_FILENAME = "FDCT_results.txt"


def format_results_for_terminal(word: str, results: list[str]) -> str:
    """Format the generated combinations for display in the terminal."""
    lines = [
        f"[+] Input: {word}",
        f"[+] Total combinations: {len(results)}",
        "",
        "Results:",
        "",
    ]
    lines.extend(f"{i}. {combo}" for i, combo in enumerate(results, start=1))
    return "\n".join(lines)


def format_results_for_file(word: str, results: list[str]) -> str:
    """Format the generated combinations for the saved text file."""
    lines = [
        "FDCT",
        "=" * 30,
        "",
        "Original input:",
        word,
        "",
        "Total combinations:",
        str(len(results)),
        "",
        "Results:",
    ]
    lines.extend(f"{i}. {combo}" for i, combo in enumerate(results, start=1))
    return "\n".join(lines) + "\n"


def save_results(word: str, results: list[str], filename: str = DEFAULT_FILENAME) -> Path:
    """Save results to a UTF-8 text file and return the path written to."""
    path = Path(filename)
    content = format_results_for_file(word, results)
    path.write_text(content, encoding="utf-8")
    return path
