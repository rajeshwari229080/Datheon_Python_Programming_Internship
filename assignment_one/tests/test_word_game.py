"""Unit tests for Console Hangman Word Game (Assignment One)."""

import unittest
from pathlib import Path
from assignment_one.word_game import (
    HangmanGame,
    DictionaryLoader,
    MAX_INCORRECT_GUESSES,
    DEFAULT_FALLBACK_WORDS,
    STAGES,
)


class TestDictionaryLoader(unittest.TestCase):
    """Tests dictionary loading, filtering, and safe fallback handling."""

    def test_fallback_when_file_missing(self):
        missing_path = Path("assignment_one/data/non_existent_file.txt")
        loader = DictionaryLoader(data_path=missing_path)
        words = loader.load_words()
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
        self.assertEqual(words, list(DEFAULT_FALLBACK_WORDS))

    def test_load_real_dictionary_if_present(self):
        real_path = Path(__file__).resolve().parent.parent / "data" / "words.txt"
        if real_path.is_file():
            loader = DictionaryLoader(data_path=real_path, min_len=4, max_len=8)
            words = loader.load_words()
            self.assertGreater(len(words), 100)
            for w in words[:50]:
                self.assertTrue(w.isalpha())
                self.assertTrue(4 <= len(w) <= 8)


class TestHangmanGameLogic(unittest.TestCase):
    """Tests core Hangman game state, input validation, and win/loss rules."""

    def setUp(self):
        self.game = HangmanGame("python")

    def test_initial_state(self):
        self.assertEqual(self.game.remaining_lives, 6)
        self.assertEqual(self.game.incorrect_guesses, 0)
        self.assertEqual(self.game.get_masked_word(), "_ _ _ _ _ _")
        self.assertFalse(self.game.is_won)
        self.assertFalse(self.game.is_lost)
        self.assertFalse(self.game.is_over)

    def test_validation_rules(self):
        # Empty input
        valid, msg = self.game.validate_guess("")
        self.assertFalse(valid)
        self.assertIn("cannot be empty", msg)

        # Multi-character input
        valid, msg = self.game.validate_guess("py")
        self.assertFalse(valid)
        self.assertIn("exactly one letter", msg)

        # Non-alphabetic input
        valid, msg = self.game.validate_guess("3")
        self.assertFalse(valid)
        self.assertIn("alphabetic", msg)

        # Valid single letter
        valid, letter = self.game.validate_guess("  P  ")
        self.assertTrue(valid)
        self.assertEqual(letter, "p")

    def test_correct_guess(self):
        success, msg = self.game.process_guess("p")
        self.assertTrue(success)
        self.assertIn("p", self.game.guessed_letters)
        self.assertEqual(self.game.remaining_lives, 6)
        self.assertEqual(self.game.get_masked_word(), "p _ _ _ _ _")

    def test_incorrect_guess(self):
        success, msg = self.game.process_guess("z")
        self.assertTrue(success)
        self.assertIn("z", self.game.guessed_letters)
        self.assertEqual(self.game.incorrect_guesses, 1)
        self.assertEqual(self.game.remaining_lives, 5)
        self.assertEqual(self.game.get_masked_word(), "_ _ _ _ _ _")

    def test_duplicate_guess_no_penalty(self):
        self.game.process_guess("z")
        self.assertEqual(self.game.remaining_lives, 5)

        # Guess 'z' again
        success, msg = self.game.process_guess("z")
        self.assertFalse(success)
        self.assertIn("already guessed", msg)
        self.assertEqual(self.game.remaining_lives, 5)  # lives must NOT decrease

    def test_win_condition(self):
        for char in "python":
            self.game.process_guess(char)
        self.assertTrue(self.game.is_won)
        self.assertFalse(self.game.is_lost)
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.get_masked_word(), "p y t h o n")

    def test_loss_condition(self):
        wrong_letters = ["a", "b", "c", "d", "e", "f"]
        for char in wrong_letters:
            self.game.process_guess(char)
        self.assertFalse(self.game.is_won)
        self.assertTrue(self.game.is_lost)
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.remaining_lives, 0)

        # Process guess after game over returns false
        success, msg = self.game.process_guess("k")
        self.assertFalse(success)
        self.assertIn("already over", msg)

    def test_gallows_art_rendering(self):
        self.assertEqual(self.game.get_gallows_art(), STAGES[0])
        self.game.process_guess("x")
        self.assertEqual(self.game.get_gallows_art(), STAGES[1])


if __name__ == "__main__":
    unittest.main()
