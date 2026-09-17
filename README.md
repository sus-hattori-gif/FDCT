# FDCT — Font/Character Deception Tool

FDCT is a small, self-contained Python CLI tool for studying and
demonstrating **Unicode homoglyphs** (also called **confusables**): pairs
or sets of Unicode characters that look visually similar (sometimes
identical) but are different code points.

Given a lowercase English word, FDCT looks up visually similar Unicode
alternatives for each letter and generates every combination of the
original word using those alternatives — for example, showing how
`hello` could also be rendered as `hellо` (with a Cyrillic `о`) or
`hеllo` (with a Cyrillic `е`), while looking nearly indistinguishable
from the original in most fonts.

**FDCT does not target or spoof any real website, brand, or system.**
It is a generic educational tool for understanding a well-documented
class of Unicode security issue (see [Unicode Technical Standard #39:
Unicode Security Mechanisms](https://www.unicode.org/reports/tr39/)),
useful for security awareness training, testing your own detection or
normalization logic, and understanding why systems like domain
registrars and username validators need confusable-checking.

## What are Unicode homoglyphs / confusables?

Unicode contains over 100,000 characters across many scripts (Latin,
Cyrillic, Greek, Armenian, and more). Some characters from different
scripts were designed independently but happen to render almost
identically — for example, Latin `o` (U+006F) and Cyrillic `о`
(U+043E). To a computer, these are completely different characters
with different code points; to a human eye, they can be
indistinguishable. This property has real security implications for
usernames, domain names, and any place where text identity matters.

**Important:** two strings that look identical on screen may not be
the same string at all. Never assume visual similarity implies
equality — always compare code points, not appearances, when identity
matters.

## Installation

FDCT requires **Python 3.10+** and has **no external dependencies** —
everything it uses is part of the Python standard library.

```bash
git clone <this-repository>
cd FDCT
python main.py
```

## Usage

Run the tool and follow the on-screen menu:

```
========================================
              FDCT
     Unicode Confusable Generator
========================================

1. Generate
2. Character information
3. About
4. Exit
```

### 1. Generate

Enter a word (lowercase English letters only). FDCT will:

1. Validate the input.
2. Calculate the theoretical number of combinations.
3. Warn you and ask for confirmation if that number exceeds the safety
   limit (100,000 by default).
4. Generate and display every combination.
5. Offer to save the results to a UTF-8 text file.

Example:

```
Enter lowercase word (or leave blank to cancel):
> hello
[+] Input accepted
[+] Confusable analysis completed
[+] Theoretical combinations: 576
[+] Combinations: 576

Results:

1. hello
2. hellо
3. hellο
...
```

### 2. Character information

Inspect a single letter's confusable characters, including each one's
code point, official Unicode name, and script:

```
Character: о
Code Point: U+043E
Unicode Name: CYRILLIC SMALL LETTER O
Script: Cyrillic
Type: Replacement
```

### 3. About

Shows a short explanation of what FDCT does and why.

## Input restrictions

Only lowercase English letters `a`–`z` are accepted. FDCT rejects, with
a clear error message:

- Uppercase letters (`Hello`)
- Numbers (`hello123`, `h3llo`)
- Spaces (`hello world`)
- Punctuation (`hello!`)
- Persian/Arabic or any other non-`a`–`z` Unicode characters (`سلام`)
- Empty input

Input is **never** silently normalized, stripped of case, or
transformed — it is validated exactly as typed.

## Combination explosion and safety limits

The number of possible combinations grows multiplicatively with the
number of available alternatives per letter, so it can grow very large
very quickly for longer words. FDCT always calculates the **theoretical**
combination count *before* generating anything.

- Default safety limit: **100,000** combinations.
- If the theoretical count exceeds the limit, FDCT reports the exact
  number and asks whether you want to proceed anyway.
- FDCT never generates combinations blindly — the check always happens
  first, and generation only proceeds after an explicit "yes" (or the
  `force=True` argument at the library level).

## Output file format

If you choose to save results, FDCT writes a single UTF-8 `.txt` file
(default name: `FDCT_results.txt`) containing the original word, the
total combination count, and every generated result, one per line:

```
FDCT
==============================

Original input:
hello

Total combinations:
576

Results:
1. hello
2. hellо
...
```

You can specify a custom filename when prompted.

## Unicode / UTF-8 considerations

- All file output uses `encoding="utf-8"` explicitly.
- Generated strings are never normalized (e.g. via NFC/NFKC) since
  normalization could collapse visually distinct-but-similar
  characters into the same code points, destroying the very
  distinctions FDCT is meant to demonstrate.
- Character metadata (code point, Unicode name) is computed live via
  Python's `unicodedata` module rather than hard-coded, so it always
  reflects the actual character.

## Project structure

```
FDCT/
│
├── main.py                 # CLI entry point
├── fdct/
│   ├── __init__.py
│   ├── generator.py        # Combination generation + safety limits
│   ├── confusables.py       # Confusables database loading/lookup
│   ├── validator.py        # Strict a-z input validation
│   ├── output.py            # Terminal display + file saving
│   └── utils.py             # Unicode metadata helpers
│
├── data/
│   └── confusables.json    # Curated Latin -> confusable character map
│
├── tests/
│   ├── test_validator.py
│   ├── test_generator.py
│   └── test_output.py
│
├── README.md
├── requirements.txt
└── LICENSE
```

## Running the tests

```bash
python -m unittest discover -s tests
```

All 18 tests should pass. Tests cover input validation (valid input,
uppercase/number/space/punctuation/Persian-Arabic rejection, empty
input), correct combination counts, preservation of the original word,
Unicode code-point handling, UTF-8 file output, and combination-limit
protection.

## Extending the confusables database

`data/confusables.json` maps each lowercase letter to a list of
confusable Unicode characters (as raw characters, not escape codes).
To add more confusables, add characters to the relevant letter's list
— all metadata (code point, name, script) is derived automatically.
For a more exhaustive set, consult the Unicode Consortium's official
[confusables data](https://www.unicode.org/Public/security/latest/confusables.txt).
