# Automated Test Results & Verification Audit

**Project Suite:** CodeCraft Python Studio  
**Test Framework:** Python `unittest` standard library  
**Test Status:** 28 Tests Executed &bull; 28 Passed &bull; 0 Failures &bull; 0 Errors  
**Execution Timestamp:** 2026-10-20  

---

## 1. Summary of Test Coverage

| Test Suite | Module Under Test | Tests Run | Result | Duration |
| :--- | :--- | :---: | :---: | :---: |
| `assignment_one/tests/test_word_game.py` | Hangman Word Game | 10 | **PASSED** | 0.008s |
| `assignment_two/tests/test_stock_tracker.py` | Stock Portfolio Tracker | 7 | **PASSED** | 0.064s |
| `assignment_three/tests/test_file_sorter.py` | Automated File Organizer | 5 | **PASSED** | 0.037s |
| `assignment_four/tests/test_faq_bot.py` | Rule-Based FAQ Bot | 6 | **PASSED** | 0.004s |
| **Total Test Suite** | **All 4 Applications** | **28** | **100% PASSED** | **0.113s** |

---

## 2. Detailed Test Specifications by Assignment

### 2.1 Assignment One — Console Hangman Word Game
- `test_fallback_when_file_missing`: Confirms internal vocabulary activates if dictionary file is missing.
- `test_load_real_dictionary_if_present`: Verifies real words loaded within length bounds (4-10 characters).
- `test_validation_rules`:
  - Rejects empty input.
  - Rejects multi-character strings.
  - Rejects numeric and punctuation characters.
  - Accepts and normalizes valid single alphabetic letters.
- `test_correct_guess`: Confirms letter unmasking and life retention.
- `test_incorrect_guess`: Confirms life decrements and error tracking.
- `test_duplicate_guess_no_penalty`: Confirms re-guessing already tried letters consumes zero lives.
- `test_win_condition`: Confirms victory status when all letters are guessed.
- `test_loss_condition`: Confirms game termination upon reaching 6 incorrect attempts.
- `test_gallows_art_rendering`: Confirms correct ASCII stage display corresponding to error counts.

### 2.2 Assignment Two — Stock Portfolio Performance Tracker
- `test_formula_calculations`: Verifies exact mathematical outputs for gain/loss dollar values and percentages in profit and loss scenarios.
- `test_unpriced_position`: Confirms unpriced assets are safely marked without calculation errors.
- `test_input_validation_rejections`: Asserts `ValueError` when given empty symbols, nonpositive quantities, or zero/negative purchase prices.
- `test_portfolio_aggregates`: Validates total invested capital, market value, and unrealized return across multiple positions.
- `test_unpriced_aggregate_behavior`: Confirms portfolio totals clearly flag when any position is unpriced.
- `test_csv_export_and_append`: Asserts headers and records are saved and historical data preserved in append mode.
- `test_constituents_catalog`: Validates S&P 500 company lookup.

### 2.3 Assignment Three — Automated File Organizer
- `test_extension_categorization`: Validates classification across all 9 target categories.
- `test_dry_run_leaves_disk_untouched`: Verifies that dry-run mode makes zero filesystem modifications and creates no directories.
- `test_active_organization`: Verifies actual file movement into category subfolders.
- `test_collision_renaming`: Verifies incoming duplicate files are safely renamed (`file_1.ext`) without overwriting.
- `test_safety_rejects_root_and_nonexistent`: Confirms root filesystem paths and missing paths are strictly rejected.

### 2.4 Assignment Four — Rule-Based Terminal FAQ Bot
- `test_text_normalization`: Confirms punctuation stripping, lowercase conversion, and whitespace collapse.
- `test_greetings_recognition`: Confirms conversational greeting flows.
- `test_exit_commands`: Confirms `quit`, `exit`, `bye`, and `goodbye` trigger clean session termination.
- `test_grounded_answer_matching`: Confirms precise answers for operating hours, project submission, and certificate issuance.
- `test_unknown_query_fallback`: Confirms non-grounded questions return helpful fallback message.
- `test_missing_or_corrupt_file_handling`: Confirms safe recovery when JSON files are missing or malformed.

---

## 3. Reproduction Commands

To replicate all automated test results on any machine:
```bash
python -m unittest discover -s assignment_one/tests -v
python -m unittest discover -s assignment_two/tests -v
python -m unittest discover -s assignment_three/tests -v
python -m unittest discover -s assignment_four/tests -v
```
