"""Unit tests for Rule-Based Terminal FAQ Bot (Assignment Four)."""

import tempfile
import unittest
from pathlib import Path
from assignment_four.faq_bot import (
    FAQLoader,
    FAQMatcher,
    FAQBotSession,
    FALLBACK_MESSAGE,
    EXIT_COMMANDS,
)


class TestFAQBot(unittest.TestCase):
    """Tests FAQ dataset parsing, token normalization, intent routing, and fallbacks."""

    def setUp(self):
        self.sample_data = {
            "greetings": ["hello", "hi", "hey"],
            "faqs": [
                {
                    "question": "What are your hours of operation?",
                    "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
                },
                {
                    "question": "How do I submit my internship project?",
                    "answer": "You can submit your public GitHub repository link through your Student Workspace."
                },
                {
                    "question": "When will I receive my certificate?",
                    "answer": "Certificates are reviewed and issued within 3-5 business days after your code review."
                }
            ]
        }
        self.matcher = FAQMatcher(self.sample_data)

    def test_text_normalization(self):
        raw = "   Hello, WORLD!?! How ARE   you?   "
        expected = "hello world how are you"
        self.assertEqual(FAQMatcher.normalize_text(raw), expected)

    def test_greetings_recognition(self):
        self.assertTrue(self.matcher.is_greeting("Hello!"))
        self.assertTrue(self.matcher.is_greeting("Hi there"))
        self.assertFalse(self.matcher.is_greeting("When do you open?"))

    def test_exit_commands(self):
        for cmd in EXIT_COMMANDS:
            self.assertTrue(self.matcher.is_exit_command(cmd))
            self.assertTrue(self.matcher.is_exit_command(f"  {cmd.upper()}! "))

        self.assertFalse(self.matcher.is_exit_command("tell me about certificate"))

    def test_grounded_answer_matching(self):
        # Direct questions
        ans1 = self.matcher.find_best_answer("What are your hours of operation?")
        self.assertIn("9:00 AM to 6:00 PM IST", ans1)

        # Keyword / Intent variation: submission
        ans2 = self.matcher.find_best_answer("Where do I submit my github project?")
        self.assertIn("Student Workspace", ans2)

        # Keyword / Intent variation: certificate
        ans3 = self.matcher.find_best_answer("Tell me about the certificate issuance timing?")
        self.assertIn("3-5 business days", ans3)

    def test_unknown_query_fallback(self):
        session = FAQBotSession()
        session.dataset = self.sample_data
        session.matcher = self.matcher

        reply, should_exit = session.generate_response("What is the recipe for chocolate cake?")
        self.assertEqual(reply, FALLBACK_MESSAGE)
        self.assertFalse(should_exit)

    def test_missing_or_corrupt_file_handling(self):
        missing_loader = FAQLoader(Path("non_existent_faq.json"))
        data = missing_loader.load()
        self.assertIn("greetings", data)
        self.assertEqual(data["faqs"], [])


if __name__ == "__main__":
    unittest.main()
