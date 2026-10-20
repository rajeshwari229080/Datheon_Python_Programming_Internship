# Assignment 01: Console Hangman Word Game

Part of **CodeCraft Python Studio** — Third Independent Python Internship Submission.

---

## Overview
An interactive, modular console word-guessing game modeled after classic Hangman. Players attempt to guess a randomly chosen English secret word within a maximum allowance of six incorrect attempts. The engine features 7-stage ASCII gallows graphics, robust character validation, duplicate guess immunity, and graceful exception handling.

---

## Key Features
- **Dictionary Integration**: Automatically loads candidate vocabulary (4 to 10 characters) from the downloaded `google-10000-english` corpus.
- **Fail-Safe Offline Operation**: Built-in fallback vocabulary activates automatically if the local dictionary is absent or unreadable.
- **State Validation**:
  - Enforces single alphabetic character entries.
  - Automatically trims whitespace and standardizes input to lowercase.
  - Rejects numbers, symbols, and multi-letter guesses with instructional messages.
- **Zero Penalty on Duplicates**: Repeatedly guessing an already probed letter never deducts player lives.
- **Visual Progression**: Renders dynamic 7-stage ASCII gallows art corresponding to 0 through 6 errors.
- **Graceful Termination**: Handles `KeyboardInterrupt` (`Ctrl+C`) and `EOFError` without crashing.

---

## Dataset Provenance
- **Dataset**: `google-10000-english-no-swears.txt`
- **Source**: [https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt)
- **Local Path**: `assignment_one/data/words.txt`
- **Total Entries**: 9,894 curated English words.

---

## Execution Guide

### Running the Game
Run from the repository root:
```bash
python assignment_one/word_game.py
```

### Running Unit Tests
Execute the independent test suite via Python's `unittest`:
```bash
python -m unittest discover -s assignment_one/tests -v
```

---

## Module Architecture
- `DictionaryLoader`: Validates and filters candidate words from filesystem; contains safe offline fallbacks.
- `HangmanGame`: Pure game logic class tracking masked word string, guessed letters set, and remaining attempts.
- `STAGES`: Immutable tuple of 7-stage ASCII gallows graphics.
- `run_console_session()`: Interactive terminal loop with replay prompt.
