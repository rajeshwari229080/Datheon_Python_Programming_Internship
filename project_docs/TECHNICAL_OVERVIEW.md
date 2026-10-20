# Technical Overview: CodeCraft Python Studio

**Suite Title:** CodeCraft Python Studio  
**Role:** Third Independent Python Internship Submission  
**Python Runtime:** Python 3.10+ Standard Library (Zero External Runtime Dependencies)

---

## 1. Architectural Philosophy & Isolation

CodeCraft Python Studio is architected around strict modular decomposition, test-driven reliability, and pure standard-library engineering. The suite comprises four standalone terminal applications, each operating as an independent system:

```
codecraft-python-studio/
├── index.htm                      # Universal Studio Portal
├── interface/                     # Minimalist UI styles & scripts
│   ├── css/studio.css
│   └── js/studio.js
├── assignment_one/                 # Hangman Game
│   ├── word_game.py
│   ├── data/words.txt
│   └── tests/test_word_game.py
├── assignment_two/                 # Stock Portfolio Tracker
│   ├── stock_tracker.py
│   ├── data/constituents.csv
│   └── tests/test_stock_tracker.py
├── assignment_three/               # Automated File Sorter
│   ├── file_sorter.py
│   ├── logs/
│   └── tests/test_file_sorter.py
├── assignment_four/                # Rule-Based FAQ Bot
│   ├── faq_bot.py
│   ├── data/sample_faq.json
│   └── tests/test_faq_bot.py
└── project_docs/                  # Engineering Specifications & Audit Logs
    ├── TECHNICAL_OVERVIEW.md
    ├── DATA_PROVENANCE.md
    └── TEST_RESULTS.md
```

---

## 2. Subsystem Technical Breakdown

### 2.1 Assignment One: Console Hangman Word Game
- **Module:** `assignment_one/word_game.py`
- **State Representation:** Encapsulated in `HangmanGame` using native `set` structures for $O(1)$ letter-membership lookup.
- **Input Sanitization:** Strips leading/trailing whitespace, forces case-folding, asserts single-character lengths, and checks `isalpha()`. Non-compliant inputs yield informative prompts without consuming player lives.
- **Duplicate Guess Immunity:** Guesses stored in `guessed_letters: Set[str]`. Duplicate submissions return a non-penalizing status flag.
- **ASCII Gallows Pipeline:** 7 immutable stages representing 0 to 6 errors mapped cleanly to life counts.
- **Fault Recovery:** `DictionaryLoader` provides a built-in immutable fallback vocabulary tuple if filesystem permissions or paths fail.

### 2.2 Assignment Two: Stock Portfolio Performance Tracker
- **Module:** `assignment_two/stock_tracker.py`
- **Financial Precision:** Floating-point values rounded to 2 decimal places adhering to mathematical specifications:
  $$\text{Invested Capital} = \text{Purchase Price} \times \text{Quantity}$$
  $$\text{Market Value} = \text{Current Price} \times \text{Quantity}$$
  $$\text{Gain / Loss} = (\text{Current Price} - \text{Purchase Price}) \times \text{Quantity}$$
  $$\text{Gain / Loss \%} = \left(\frac{\text{Current Price} - \text{Purchase Price}}{\text{Purchase Price}}\right) \times 100$$
- **Zero Fabrication Policy:** Unknown prices remain `UNPRICED` or `None`. Aggregates visibly denote unpriced holdings rather than producing synthetic valuations.
- **Constituents Caching:** `ConstituentsLoader` reads `assignment_two/data/constituents.csv` once, caching uppercase symbols in memory for $O(1)$ lookups.
- **CSV Audit Trailing:** Writes to `assignment_two/reports/portfolio_summary.csv` using Python's native `csv.DictWriter` in append mode, logging ISO 8601 UTC timestamps.

### 2.3 Assignment Three: Automated File Organizer
- **Module:** `assignment_three/file_sorter.py`
- **Category Taxonomy:** 9 mutually exclusive categories covering Documents, Images, Videos, Audio, Archives, Source Code, Spreadsheets, Presentations, and Other.
- **Filesystem Traversal:** Built on `os.scandir()` and `pathlib.Path` for fast iterative enumeration without loading entire directory trees into memory.
- **Safety Gatekeepers:**
  - Evaluates directory anchors, refusing root anchors (`C:\`, `/`) and Windows operating system paths.
  - Skips already organized category folders, hidden files, and symbolic links.
- **Collision Mitigation:** When destination collisions occur, systematically scans for the next increment (`filename_1.ext`, `filename_2.ext`) to ensure zero silent overwrites.
- **Dry-Run Mode:** Full preview mode executing scanning and path resolution without calling `shutil.move` or creating folders.

### 2.4 Assignment Four: Rule-Based Terminal FAQ Bot
- **Module:** `assignment_four/faq_bot.py`
- **Normalization Pipeline:** Lowercases, strips punctuation using `str.maketrans`, and condenses spaces.
- **Precedence Hierarchy:**
  1. Session command interceptor (`quit`, `exit`, `bye`, `help`).
  2. Conversational greetings (`hello`, `hi`, `hey`).
  3. Priority regex matchers for domain-specific subjects (`certificate`, `submission`, `hours`).
  4. Token-overlap Jaccard scoring on remaining candidate FAQ questions.
  5. Grounded fallback response for unverified questions (no hallucinated policies).

---

## 3. Reliability & Exception Handling
All four applications handle `KeyboardInterrupt` (`Ctrl+C`) and `EOFError` gracefully to prevent raw stack traces from reaching end users. File operations use context managers (`with open(...)`) ensuring resource disposal.
