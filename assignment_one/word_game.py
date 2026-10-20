"""Console Hangman Word Game - CodeCraft Python Studio

An interactive, modular console implementation of Hangman featuring ASCII gallows art,
single-letter validation, duplicate guess protection, and safe dictionary loading.
"""

from __future__ import annotations
import os
import random
import sys
from pathlib import Path
from typing import List, Set, Tuple, Optional

# Distinct 7-stage ASCII gallows art (0 to 6 errors)
STAGES: Tuple[str, ...] = (
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
)

DEFAULT_FALLBACK_WORDS: Tuple[str, ...] = (
    "python", "studio", "craft", "software", "variable", "function",
    "terminal", "console", "keyboard", "package", "developer", "module"
)

MAX_INCORRECT_GUESSES: int = 6


class DictionaryLoader:
    """Handles loading and filtering candidate secret words from local dictionary."""

    def __init__(self, data_path: Optional[Path] = None, min_len: int = 4, max_len: int = 10) -> None:
        if data_path is None:
            self.data_path = Path(__file__).resolve().parent / "data" / "words.txt"
        else:
            self.data_path = Path(data_path)
        self.min_len = min_len
        self.max_len = max_len

    def load_words(self) -> List[str]:
        """Loads valid alpha words within length criteria. Falls back safely if missing."""
        if not self.data_path.is_file():
            return list(DEFAULT_FALLBACK_WORDS)

        try:
            with open(self.data_path, "r", encoding="utf-8", errors="ignore") as f:
                words = [
                    line.strip().lower()
                    for line in f
                    if line.strip().isalpha() and self.min_len <= len(line.strip()) <= self.max_len
                ]
            return words if words else list(DEFAULT_FALLBACK_WORDS)
        except Exception:
            return list(DEFAULT_FALLBACK_WORDS)


class HangmanGame:
    """Manages the state and business logic of a single Hangman game round."""

    def __init__(self, secret_word: str) -> None:
        self.secret_word: str = secret_word.strip().lower()
        self.guessed_letters: Set[str] = set()
        self.incorrect_guesses: int = 0
        self.max_incorrect: int = MAX_INCORRECT_GUESSES

    @property
    def remaining_lives(self) -> int:
        return max(0, self.max_incorrect - self.incorrect_guesses)

    @property
    def is_won(self) -> bool:
        return all(c in self.guessed_letters for c in self.secret_word)

    @property
    def is_lost(self) -> bool:
        return self.incorrect_guesses >= self.max_incorrect

    @property
    def is_over(self) -> bool:
        return self.is_won or self.is_lost

    def get_masked_word(self) -> str:
        """Returns the word with hidden letters replaced by underscores."""
        return " ".join([c if c in self.guessed_letters else "_" for c in self.secret_word])

    def get_gallows_art(self) -> str:
        """Returns ASCII art corresponding to current error count."""
        index = min(self.incorrect_guesses, len(STAGES) - 1)
        return STAGES[index]

    def validate_guess(self, user_input: str) -> Tuple[bool, str]:
        """Validates raw user input to ensure it is a single alphabetic letter."""
        cleaned = user_input.strip().lower()
        if not cleaned:
            return False, "Input cannot be empty. Please enter a single letter."
        if len(cleaned) != 1:
            return False, "Please enter exactly one letter at a time."
        if not cleaned.isalpha():
            return False, "Invalid character. Please enter an alphabetic character (A-Z)."
        return True, cleaned

    def process_guess(self, raw_guess: str) -> Tuple[bool, str]:
        """Processes a guess, updates game state, and returns (success_flag, message)."""
        if self.is_over:
            return False, "Game is already over."

        is_valid, result = self.validate_guess(raw_guess)
        if not is_valid:
            return False, result

        letter = result
        if letter in self.guessed_letters:
            return False, f"You have already guessed '{letter.upper()}'. No penalty applied."

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            if self.is_won:
                return True, f"Brilliant! '{letter.upper()}' was correct and you completed the word!"
            return True, f"Good guess! '{letter.upper()}' is in the word."
        else:
            self.incorrect_guesses += 1
            if self.is_lost:
                return True, f"Wrong guess: '{letter.upper()}'. You have no lives left."
            return True, f"Incorrect guess: '{letter.upper()}'. Lives remaining: {self.remaining_lives}."


def run_console_session() -> None:
    """Interactive CLI runner for Hangman."""
    print("=" * 60)
    print("  CodeCraft Python Studio - Console Hangman Word Game")
    print("=" * 60)

    loader = DictionaryLoader()
    words = loader.load_words()
    print(f"[System] Loaded {len(words)} candidate words.")

    while True:
        secret = random.choice(words)
        game = HangmanGame(secret)
        print("\n[New Game] A secret word has been selected! Good luck!\n")

        while not game.is_over:
            print(game.get_gallows_art())
            print(f"Word: {game.get_masked_word()}")
            print(f"Guessed Letters: {', '.join(sorted(game.guessed_letters)).upper() or 'None'}")
            print(f"Remaining Lives: {game.remaining_lives}/{game.max_incorrect}")

            try:
                user_guess = input("\nEnter your letter guess (or 'quit' to exit): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated by user. Goodbye!")
                return

            if user_guess.lower() in ("quit", "exit"):
                print("Thanks for playing CodeCraft Hangman!")
                return

            success, msg = game.process_guess(user_guess)
            print(f"\n>> {msg}")

        # Game outcome
        print(game.get_gallows_art())
        if game.is_won:
            print("*" * 50)
            print(f" CONGRATULATIONS! You guessed the word: {game.secret_word.upper()}!")
            print("*" * 50)
        else:
            print("-" * 50)
            print(f" GAME OVER! You ran out of attempts.")
            print(f" The secret word was: {game.secret_word.upper()}")
            print("-" * 50)

        try:
            again = input("\nWould you like to play another round? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                print("Thank you for playing CodeCraft Hangman. Goodbye!")
                break
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Goodbye!")
            break


if __name__ == "__main__":
    run_console_session()
