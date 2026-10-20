"""Stock Portfolio Performance Tracker - CodeCraft Python Studio

A robust, offline-capable stock portfolio performance tracking engine.
Calculates capital invested, current market valuations, absolute gain/loss,
and percentage return using verified mathematical formulas.
Outputs structured CSV reports and validates symbols against the S&P 500 constituents.

DISCLAIMER: For academic and educational demonstration purposes only.
Not intended as financial, trading, or investment advice.
"""

from __future__ import annotations
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

DISCLAIMER_TEXT = (
    "EDUCATIONAL DISCLAIMER: This software is built strictly for educational "
    "and demonstrative portfolio analysis. It does not constitute financial, "
    "investment, tax, or trading advice."
)


class Position:
    """Represents an individual stock holding."""

    def __init__(self, symbol: str, quantity: float, purchase_price: float, current_price: Optional[float] = None) -> None:
        symbol_clean = symbol.strip().upper()
        if not symbol_clean:
            raise ValueError("Stock symbol cannot be empty.")
        if quantity <= 0:
            raise ValueError(f"Quantity must be greater than zero. Provided: {quantity}")
        if purchase_price <= 0:
            raise ValueError(f"Purchase price must be greater than zero. Provided: {purchase_price}")
        if current_price is not None and current_price < 0:
            raise ValueError(f"Current price cannot be negative. Provided: {current_price}")

        self.symbol: str = symbol_clean
        self.quantity: float = float(quantity)
        self.purchase_price: float = float(purchase_price)
        self.current_price: Optional[float] = float(current_price) if current_price is not None else None

    @property
    def invested_capital(self) -> float:
        """Invested capital = purchase price * quantity"""
        return round(self.purchase_price * self.quantity, 2)

    @property
    def market_value(self) -> Optional[float]:
        """Market value = current price * quantity (None if current price unpriced)"""
        if self.current_price is None:
            return None
        return round(self.current_price * self.quantity, 2)

    @property
    def gain_loss(self) -> Optional[float]:
        """Gain/loss = (current price - purchase price) * quantity"""
        if self.current_price is None:
            return None
        return round((self.current_price - self.purchase_price) * self.quantity, 2)

    @property
    def gain_loss_percent(self) -> Optional[float]:
        """Gain/loss % = ((current price - purchase price) / purchase price) * 100"""
        if self.current_price is None:
            return None
        return round(((self.current_price - self.purchase_price) / self.purchase_price) * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Symbol": self.symbol,
            "Quantity": self.quantity,
            "Purchase Price ($)": f"{self.purchase_price:.2f}",
            "Current Price ($)": f"{self.current_price:.2f}" if self.current_price is not None else "UNPRICED",
            "Invested Capital ($)": f"{self.invested_capital:.2f}",
            "Market Value ($)": f"{self.market_value:.2f}" if self.market_value is not None else "N/A",
            "Gain/Loss ($)": f"{self.gain_loss:.2f}" if self.gain_loss is not None else "N/A",
            "Gain/Loss (%)": f"{self.gain_loss_percent:.2f}%" if self.gain_loss_percent is not None else "N/A",
        }


class ConstituentsLoader:
    """Loads and validates symbols against the S&P 500 constituents catalog."""

    def __init__(self, csv_path: Optional[Path] = None) -> None:
        if csv_path is None:
            self.csv_path = Path(__file__).resolve().parent / "data" / "constituents.csv"
        else:
            self.csv_path = Path(csv_path)
        self._cache: Optional[Dict[str, Dict[str, str]]] = None

    def load(self) -> Dict[str, Dict[str, str]]:
        if self._cache is not None:
            return self._cache

        catalog: Dict[str, Dict[str, str]] = {}
        if not self.csv_path.is_file():
            self._cache = catalog
            return catalog

        try:
            with open(self.csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sym = row.get("Symbol", "").strip().upper()
                    if sym:
                        catalog[sym] = {
                            "Security": row.get("Security", "").strip(),
                            "Sector": row.get("GICS Sector", "").strip(),
                            "SubIndustry": row.get("GICS Sub-Industry", "").strip(),
                        }
        except Exception:
            pass

        self._cache = catalog
        return catalog

    def is_valid_constituent(self, symbol: str) -> bool:
        return symbol.strip().upper() in self.load()

    def get_info(self, symbol: str) -> Optional[Dict[str, str]]:
        return self.load().get(symbol.strip().upper())


class PortfolioTracker:
    """Manages collection of positions, valuations, and CSV exports."""

    def __init__(self, constituents_path: Optional[Path] = None) -> None:
        self.positions: List[Position] = []
        self.constituents = ConstituentsLoader(constituents_path)

    def add_position(self, symbol: str, quantity: float, purchase_price: float, current_price: Optional[float] = None) -> Position:
        pos = Position(symbol, quantity, purchase_price, current_price)
        self.positions.append(pos)
        return pos

    def total_invested_capital(self) -> float:
        return round(sum(p.invested_capital for p in self.positions), 2)

    def total_market_value(self) -> Tuple[Optional[float], bool]:
        """Returns (total_market_value, all_priced_flag). If any position is unpriced, returns partial total and False."""
        all_priced = all(p.current_price is not None for p in self.positions) if self.positions else True
        priced_sum = sum(p.market_value for p in self.positions if p.market_value is not None)
        return round(priced_sum, 2), all_priced

    def total_gain_loss(self) -> Tuple[Optional[float], bool]:
        """Returns total gain/loss across priced holdings and boolean flag."""
        all_priced = all(p.current_price is not None for p in self.positions) if self.positions else True
        gain_loss_sum = sum(p.gain_loss for p in self.positions if p.gain_loss is not None)
        return round(gain_loss_sum, 2), all_priced

    def export_csv_report(self, target_path: Path, preserve_existing: bool = True) -> Path:
        """Exports holdings summary to CSV, appending or archiving according to policy."""
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "Timestamp",
            "Symbol",
            "Security_Name",
            "Quantity",
            "Purchase_Price",
            "Current_Price",
            "Invested_Capital",
            "Market_Value",
            "Gain_Loss_Dollar",
            "Gain_Loss_Percent"
        ]

        file_exists = target_path.is_file() and preserve_existing
        write_mode = "a" if file_exists else "w"
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with open(target_path, mode=write_mode, newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            for pos in self.positions:
                info = self.constituents.get_info(pos.symbol)
                sec_name = info["Security"] if info else "Unknown"
                writer.writerow({
                    "Timestamp": now_iso,
                    "Symbol": pos.symbol,
                    "Security_Name": sec_name,
                    "Quantity": f"{pos.quantity:.4f}",
                    "Purchase_Price": f"{pos.purchase_price:.2f}",
                    "Current_Price": f"{pos.current_price:.2f}" if pos.current_price is not None else "UNPRICED",
                    "Invested_Capital": f"{pos.invested_capital:.2f}",
                    "Market_Value": f"{pos.market_value:.2f}" if pos.market_value is not None else "UNPRICED",
                    "Gain_Loss_Dollar": f"{pos.gain_loss:.2f}" if pos.gain_loss is not None else "N/A",
                    "Gain_Loss_Percent": f"{pos.gain_loss_percent:.2f}%" if pos.gain_loss_percent is not None else "N/A"
                })

        return target_path


def run_interactive_tracker() -> None:
    """Interactive command-line workflow for stock portfolio management."""
    print("=" * 65)
    print("  CodeCraft Python Studio - Stock Portfolio Performance Tracker")
    print("=" * 65)
    print(f"\n{DISCLAIMER_TEXT}\n")

    tracker = PortfolioTracker()
    constituents_count = len(tracker.constituents.load())
    print(f"[Constituents] Loaded {constituents_count} verified S&P 500 company records.")

    # Demonstration initial positions if desired
    sample_positions = [
        ("AAPL", 15.0, 172.50, 189.20),
        ("MSFT", 10.0, 310.00, 342.10),
        ("GOOGL", 8.0, 135.00, None),  # Demonstrate unpriced holding handling
    ]

    for sym, qty, buy, curr in sample_positions:
        tracker.add_position(sym, qty, buy, curr)

    print("\n--- Current Portfolio Holdings ---")
    for pos in tracker.positions:
        row = pos.to_dict()
        status = f"Invested: ${row['Invested Capital ($)']} | Value: ${row['Market Value ($)']} | Return: {row['Gain/Loss ($)']} ({row['Gain/Loss (%)']})"
        print(f"[{row['Symbol']}] {row['Quantity']} shares @ ${row['Purchase Price ($)']} -> {status}")

    total_inv = tracker.total_invested_capital()
    total_val, all_priced = tracker.total_market_value()
    total_gl, _ = tracker.total_gain_loss()

    print("\n--- Portfolio Aggregates ---")
    print(f"Total Invested Capital : ${total_inv:,.2f}")
    if all_priced:
        print(f"Total Market Value     : ${total_val:,.2f}")
        print(f"Total Unrealized Return: ${total_gl:,.2f}")
    else:
        print(f"Total Market Value     : ${total_val:,.2f}* (*Note: Some positions are unpriced)")
        print(f"Total Unrealized Return: ${total_gl:,.2f}* (Calculated across priced holdings only)")

    # Save CSV
    out_file = Path(__file__).resolve().parent / "reports" / "portfolio_summary.csv"
    saved = tracker.export_csv_report(out_file)
    print(f"\n[Export] Detailed valuation record saved to: {saved}")


if __name__ == "__main__":
    run_interactive_tracker()
