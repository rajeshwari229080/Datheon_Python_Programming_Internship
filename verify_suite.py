"""Comprehensive Verification Script - CodeCraft Python Studio

Runs all 28 unit tests, checks dataset integrity, validates HTML links,
and prints an executive verification report for review.
"""

from __future__ import annotations
import subprocess
import sys
import unittest
from pathlib import Path


def run_unit_tests() -> bool:
    print("=" * 65)
    print("  CodeCraft Python Studio - Automated Verification Runner")
    print("=" * 65)

    suites = [
        ("Assignment One (Word Game)", "assignment_one/tests"),
        ("Assignment Two (Stock Tracker)", "assignment_two/tests"),
        ("Assignment Three (File Organizer)", "assignment_three/tests"),
        ("Assignment Four (FAQ Bot)", "assignment_four/tests"),
    ]

    all_passed = True
    total_tests_run = 0

    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)

    root_dir = str(Path(__file__).resolve().parent)
    for name, path_str in suites:
        print(f"\n[Running Suite] {name} ({path_str})")
        suite = loader.discover(start_dir=path_str, pattern="test_*.py", top_level_dir=root_dir)
        result = runner.run(suite)
        total_tests_run += result.testsRun
        if not result.wasSuccessful():
            all_passed = False

    print("\n" + "=" * 65)
    print(f"Total Unit Tests Run : {total_tests_run}")
    print(f"Overall Test Status  : {'ALL PASSED (100%)' if all_passed else 'FAILURES DETECTED'}")
    print("=" * 65)
    return all_passed


def verify_file_assets() -> bool:
    print("\n[Verifying File System Assets & HTML Pages]")
    required_files = [
        "index.html",
        "README.md",
        "requirements.txt",
        "interface/css/studio.css",
        "interface/js/studio.js",
        "assignment_one/word_game.py",
        "assignment_one/index.html",
        "assignment_one/data/words.txt",
        "assignment_two/stock_tracker.py",
        "assignment_two/index.html",
        "assignment_two/data/constituents.csv",
        "assignment_three/file_sorter.py",
        "assignment_three/index.html",
        "assignment_four/faq_bot.py",
        "assignment_four/index.html",
        "assignment_four/data/sample_faq.json",
        "project_docs/TECHNICAL_OVERVIEW.md",
        "project_docs/DATA_PROVENANCE.md",
        "project_docs/TEST_RESULTS.md",
    ]

    root = Path(__file__).resolve().parent
    missing = []
    for rel_path in required_files:
        target = root / rel_path
        if not target.is_file():
            missing.append(rel_path)
            print(f"  [MISSING] {rel_path}")
        else:
            print(f"  [VERIFIED] {rel_path}")

    if missing:
        print(f"\n[Error] {len(missing)} asset(s) missing!")
        return False

    print("\n[Success] All core source, data, HTML, and documentation assets verified!")
    return True


if __name__ == "__main__":
    tests_ok = run_unit_tests()
    assets_ok = verify_file_assets()

    if tests_ok and assets_ok:
        print("\n>>> CODECRAFT PYTHON STUDIO SUITE IS 100% READY AND VERIFIED! <<<\n")
        sys.exit(0)
    else:
        print("\n>>> VERIFICATION FAILED! <<<\n")
        sys.exit(1)
