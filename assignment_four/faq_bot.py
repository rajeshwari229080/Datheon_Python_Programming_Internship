"""Rule-Based Terminal FAQ Bot - CodeCraft Python Studio

A conversational question-answering assistant grounded strictly in verified FAQ datasets.
Utilizes regex pattern matching, normalized keyword scoring, intent prioritization,
and graceful offline fallbacks without fabricating unverified information.
"""

from __future__ import annotations
import json
import os
import re
import string
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

EXIT_COMMANDS = {"quit", "exit", "bye", "goodbye", "q"}
HELP_COMMANDS = {"help", "commands", "menu", "options", "what can you do"}

FALLBACK_MESSAGE = (
    "I am sorry, but I do not have verified information answering that question in my current dataset. "
    "Please type 'help' to review supported topics or consult your program coordinator."
)


class FAQLoader:
    """Safely loads and validates FAQ entries from JSON datasets."""

    def __init__(self, json_path: Optional[Path] = None) -> None:
        if json_path is None:
            self.json_path = Path(__file__).resolve().parent / "data" / "sample_faq.json"
        else:
            self.json_path = Path(json_path)

    def load(self) -> Dict[str, Any]:
        """Loads JSON file. Returns dictionary with greetings and faqs list."""
        default_structure = {
            "greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "faqs": []
        }

        if not self.json_path.is_file():
            return default_structure

        try:
            with open(self.json_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Ensure structure integrity
                    greetings = data.get("greetings", default_structure["greetings"])
                    raw_faqs = data.get("faqs", [])
                    validated_faqs = [
                        item for item in raw_faqs
                        if isinstance(item, dict) and "question" in item and "answer" in item
                    ]
                    return {"greetings": greetings, "faqs": validated_faqs}
                return default_structure
        except Exception:
            return default_structure


class FAQMatcher:
    """Pre-processes inputs and matches queries against known FAQ items using regex and keyword rules."""

    def __init__(self, dataset: Dict[str, Any]) -> None:
        self.greetings: List[str] = [g.lower() for g in dataset.get("greetings", [])]
        self.faqs: List[Dict[str, str]] = dataset.get("faqs", [])

        # Prioritize specific subject keywords (certificate, submission) over generic timing words
        self.intent_patterns = [
            (
                re.compile(r"\b(certificate|cert|certification|completion|award|issued)\b", re.IGNORECASE),
                "certificate",
            ),
            (
                re.compile(r"\b(submit|submission|upload|github|repo|repository|project)\b", re.IGNORECASE),
                "submission",
            ),
            (
                re.compile(r"\b(hours?|business hours|open|schedule|operating hours)\b", re.IGNORECASE),
                "hours",
            ),
        ]

    @staticmethod
    def normalize_text(text: str) -> str:
        """Strips punctuation, trims extraneous whitespace, and lowercases text."""
        if not text:
            return ""
        lowered = text.strip().lower()
        # Remove punctuation
        cleaned = lowered.translate(str.maketrans("", "", string.punctuation))
        # Collapse multiple spaces
        return re.sub(r"\s+", " ", cleaned).strip()

    def is_exit_command(self, raw_input: str) -> bool:
        norm = self.normalize_text(raw_input)
        return norm in EXIT_COMMANDS

    def is_help_command(self, raw_input: str) -> bool:
        norm = self.normalize_text(raw_input)
        return norm in HELP_COMMANDS or any(norm.startswith(h) for h in HELP_COMMANDS)

    def is_greeting(self, raw_input: str) -> bool:
        norm = self.normalize_text(raw_input)
        return any(norm == g or norm.startswith(g + " ") for g in self.greetings)

    def find_best_answer(self, raw_input: str) -> Optional[str]:
        """Finds the most specific grounded FAQ answer or returns None."""
        norm = self.normalize_text(raw_input)
        if not norm:
            return None

        # 1. Exact or near-exact question match
        for item in self.faqs:
            q_norm = self.normalize_text(item["question"])
            if norm == q_norm or norm in q_norm or q_norm in norm:
                return item["answer"]

        # 2. Specific Regex intent matchers grounded in dataset topics
        for pattern, intent_tag in self.intent_patterns:
            if pattern.search(norm):
                for item in self.faqs:
                    q_lower = item["question"].lower()
                    if intent_tag == "hours" and any(k in q_lower for k in ("hours", "operating", "operation")):
                        return item["answer"]
                    if intent_tag == "submission" and any(k in q_lower for k in ("submit", "submission", "project")):
                        return item["answer"]
                    if intent_tag == "certificate" and any(k in q_lower for k in ("certificate", "certification")):
                        return item["answer"]

        # 3. Token overlap scoring as a fallback
        query_tokens = set(norm.split())
        best_score = 0
        best_answer: Optional[str] = None

        for item in self.faqs:
            q_tokens = set(self.normalize_text(item["question"]).split())
            overlap = len(query_tokens.intersection(q_tokens))
            if overlap > best_score and overlap >= 2:
                best_score = overlap
                best_answer = item["answer"]

        return best_answer


class FAQBotSession:
    """Orchestrates interactive chat interaction loop."""

    def __init__(self, data_path: Optional[Path] = None) -> None:
        self.loader = FAQLoader(data_path)
        self.dataset = self.loader.load()
        self.matcher = FAQMatcher(self.dataset)

    def generate_response(self, user_input: str) -> Tuple[str, bool]:
        """Returns (response_text, should_exit_flag)."""
        if not user_input.strip():
            return "Please enter a question or type 'help' to see available topics.", False

        if self.matcher.is_exit_command(user_input):
            return "Thank you for chatting with CodeCraft Support. Have a productive day!", True

        if self.matcher.is_help_command(user_input):
            faq_topics = [f"- {item['question']}" for item in self.dataset["faqs"]]
            help_msg = (
                "CodeCraft Terminal FAQ Bot - Supported Topics:\n"
                + "\n".join(faq_topics)
                + "\n\nYou can also type 'exit' or 'quit' anytime to end the session."
            )
            return help_msg, False

        if self.matcher.is_greeting(user_input):
            return "Hello! I am CodeCraft Studio's assistant. How may I assist you with your internship questions today?", False

        answer = self.matcher.find_best_answer(user_input)
        if answer:
            return answer, False

        return FALLBACK_MESSAGE, False

    def start_terminal_chat(self) -> None:
        print("=" * 65)
        print("  CodeCraft Python Studio - Rule-Based FAQ Assistant")
        print("=" * 65)
        print(f"[Knowledge Base] Loaded {len(self.dataset['faqs'])} verified FAQ items.")
        print("Type 'help' to view supported topics, or 'quit' to exit.\n")

        while True:
            try:
                user_msg = input("You: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated by user. Goodbye!")
                break

            response, should_exit = self.generate_response(user_msg)
            print(f"Bot: {response}\n")

            if should_exit:
                break


def main() -> None:
    session = FAQBotSession()
    session.start_terminal_chat()


if __name__ == "__main__":
    main()
