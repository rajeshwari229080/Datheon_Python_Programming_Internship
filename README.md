# CodeCraft Python Studio

**Third Independent Python Internship Submission Suite**  
*A comprehensive collection of four modular, fully-tested Python applications unified through a modern workspace documentation portal.*

---

## Suite Summary

CodeCraft Python Studio delivers four practical Python applications covering interactive programming, financial data analysis, filesystem automation, and rule-based conversational systems:

| # | Project Name | Entry Point | Core Focus | Verified Tests |
| :-: | :--- | :--- | :--- | :-: |
| **01** | **Console Hangman Word Game** | `assignment_one/word_game.py` | 6-attempt vocabulary game, 7-stage ASCII graphics, duplicate guess immunity | **10 / 10** |
| **02** | **Stock Portfolio Tracker** | `assignment_two/stock_tracker.py` | Financial valuation formulas, S&P 500 lookup, CSV reports, zero price fabrication | **7 / 7** |
| **03** | **Automated File Organizer** | `assignment_three/file_sorter.py` | 9-category sorting, dry-run simulation, non-destructive renaming, root guard | **5 / 5** |
| **04** | **Rule-Based Terminal FAQ Bot** | `assignment_four/faq_bot.py` | Grounded JSON FAQs, regex intent priority, text normalization, truthful fallback | **6 / 6** |

---

## Workspace Navigation & Web Portal

The suite includes an interactive, responsive local HTML portal connecting all four assignments:
- **Universal Homepage:** [`index.htm`](index.htm)
- **Assignment 01 Documentation:** [`assignment_one/index.htm`](assignment_one/index.htm)
- **Assignment 02 Documentation:** [`assignment_two/index.htm`](assignment_two/index.htm)
- **Assignment 03 Documentation:** [`assignment_three/index.htm`](assignment_three/index.htm)
- **Assignment 04 Documentation:** [`assignment_four/index.htm`](assignment_four/index.htm)
- **Shared Stylesheet:** [`interface/css/studio.css`](interface/css/studio.css)

Open `index.htm` directly in any web browser to explore interactive project overviews, architectural diagrams, formula definitions, and execution guides.

---

## Quick Start & Execution

All applications run on standard **Python 3.10+** without requiring any third-party package installations.

### 1. Launch Assignment 01 (Hangman Game)
```bash
python assignment_one/word_game.py
```

### 2. Launch Assignment 02 (Stock Portfolio Tracker)
```bash
python assignment_two/stock_tracker.py
```

### 3. Launch Assignment 03 (File Organizer - Dry Run Preview)
```bash
python assignment_three/file_sorter.py --target "path/to/folder" --dry-run
```

### 4. Launch Assignment 04 (Rule-Based FAQ Bot)
```bash
python assignment_four/faq_bot.py
```

---

## Automated Verification

Execute the complete 28-test suite across all assignments using Python's built-in `unittest`:
```bash
# Run all four assignment test suites
python -m unittest discover -s assignment_one/tests -v
python -m unittest discover -s assignment_two/tests -v
python -m unittest discover -s assignment_three/tests -v
python -m unittest discover -s assignment_four/tests -v
```

---

## Technical Documentation
- **[TECHNICAL_OVERVIEW.md](project_docs/TECHNICAL_OVERVIEW.md)**: Architectural breakdown, memory complexity, error handling policies.
- **[DATA_PROVENANCE.md](project_docs/DATA_PROVENANCE.md)**: Dataset sources, verified line counts, local caching, and fallback guarantees.
- **[TEST_RESULTS.md](project_docs/TEST_RESULTS.md)**: Full test execution logs, coverage analysis, and edge case assertions.

---

## License & Integrity
Developed independently as an academic internship submission. All source code, styles, interface components, and tests are author-original.
