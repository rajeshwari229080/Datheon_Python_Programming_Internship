# Assignment 04: Rule-Based Terminal FAQ Bot

Part of **CodeCraft Python Studio** — Third Independent Python Internship Submission.

---

## Overview
A lightweight conversational assistant operating directly in the terminal to answer common student inquiries regarding internship guidelines, submission methods, and certification timelines. The chatbot uses regular expression intent classifiers, string normalization, and grounded knowledge retrieval without hallucinations or paid third-party AI APIs.

---

## Technical Pipeline

```
[User Input] 
     │
     ▼
[Normalization Engine] (Lowercases, strips punctuation, normalizes spacing)
     │
     ├─► [Exit Classifier] ('quit', 'exit', 'bye') ──► Graceful Exit
     ├─► [Help Classifier] ('help', 'menu') ─────────► Display Topics
     ├─► [Greeting Classifier] ('hello', 'hi') ──────► Conversational Greeting
     │
     ▼
[Regex & Intent Matcher] (Prioritized topic matching: Certs, Submission, Hours)
     │
     ├─► [Match Found] ──────► Grounded Response from sample_faq.json
     └─► [No Match] ─────────► Grounded Fallback Message (No Fabrications)
```

---

## Grounded Knowledge Base
- **Dataset**: `sample_faq.json`
- **Source**: [https://www.datheon.in/datasets/sample_faq.json](https://www.datheon.in/datasets/sample_faq.json)
- **Local Path**: `assignment_four/data/sample_faq.json`
- **Supported Intents**:
  1. **Operating Hours**: Monday through Friday, 9:00 AM - 6:00 PM IST.
  2. **Project Submission**: Submission via public GitHub repository links in the Student Workspace.
  3. **Certification Timeline**: Review and issuance in 3-5 business days post code evaluation.

---

## Execution Guide

### Running Interactive Terminal Chat
```bash
python assignment_four/faq_bot.py
```

### Running Unit Tests
```bash
python -m unittest discover -s assignment_four/tests -v
```
