# Assignment 02: Stock Portfolio Performance Tracker

Part of **CodeCraft Python Studio** — Third Independent Python Internship Submission.

---

## Overview
A terminal application designed to monitor stock investment holdings, calculate realized and unrealized gain/loss metrics, validate tickers against the S&P 500 constituents dataset, and generate audit-ready CSV performance reports.

> **EDUCATIONAL DISCLAIMER**: This application is strictly an educational tool designed to demonstrate algorithmic valuation and standard CSV record processing. It does not provide real-time market pricing, trading automation, or professional investment advice.

---

## Valuation Formulas
All performance analytics adhere to standardized mathematical definitions:

| Metric | Formula | Description |
| :--- | :--- | :--- |
| **Invested Capital** | $\text{Purchase Price} \times \text{Quantity}$ | Total cash outlay committed to open position. |
| **Market Value** | $\text{Current Price} \times \text{Quantity}$ | Present valuation based on verified quotes. |
| **Gain / Loss ($)** | $(\text{Current Price} - \text{Purchase Price}) \times \text{Quantity}$ | Net dollar increase or decrease. |
| **Gain / Loss (%)** | $\left(\frac{\text{Current Price} - \text{Purchase Price}}{\text{Purchase Price}}\right) \times 100$ | Relative rate of return. |

---

## Key Features & Safety Policies
- **Symbol Verification**: Cross-references input tickers against `assignment_two/data/constituents.csv` (500+ official S&P constituents).
- **Zero Fabrication Rule**: When current market quotes are missing, the system labels positions as `UNPRICED` rather than generating artificial data. Aggregates explicitly flag unpriced holdings.
- **Input Boundary Rejections**: Disallows quantities $\le 0$, purchase prices $\le 0$, and negative current prices.
- **CSV Audit Trails**: Appends timestamped valuation records to `assignment_two/reports/portfolio_summary.csv` while preserving historical snapshots.

---

## Dataset Provenance
- **Dataset**: `constituents.csv`
- **Source**: [https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv](https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv)
- **Local Path**: `assignment_two/data/constituents.csv`
- **Fields**: `Symbol`, `Security`, `GICS Sector`, `GICS Sub-Industry`, `Headquarters Location`, `Date added`, `CIK`, `Founded`.

---

## Execution Guide

### Running the Portfolio Tracker
```bash
python assignment_two/stock_tracker.py
```

### Running Unit Tests
```bash
python -m unittest discover -s assignment_two/tests -v
```
