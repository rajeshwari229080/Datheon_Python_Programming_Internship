"""Unit tests for Stock Portfolio Performance Tracker (Assignment Two)."""

import csv
import tempfile
import unittest
from pathlib import Path
from assignment_two.stock_tracker import (
    Position,
    PortfolioTracker,
    ConstituentsLoader,
    DISCLAIMER_TEXT,
)


class TestPositionModel(unittest.TestCase):
    """Tests Position calculation formulas and input boundary validation."""

    def test_formula_calculations(self):
        # 10 shares @ $100, current price $120
        pos = Position("AAPL", quantity=10.0, purchase_price=100.0, current_price=120.0)
        self.assertEqual(pos.invested_capital, 1000.00)
        self.assertEqual(pos.market_value, 1200.00)
        self.assertEqual(pos.gain_loss, 200.00)
        self.assertEqual(pos.gain_loss_percent, 20.00)

        # Loss scenario: 5 shares @ $200, current price $150
        loss_pos = Position("TSLA", quantity=5.0, purchase_price=200.0, current_price=150.0)
        self.assertEqual(loss_pos.invested_capital, 1000.00)
        self.assertEqual(loss_pos.market_value, 750.00)
        self.assertEqual(loss_pos.gain_loss, -250.00)
        self.assertEqual(loss_pos.gain_loss_percent, -25.00)

    def test_unpriced_position(self):
        pos = Position("AMZN", quantity=4.0, purchase_price=150.0, current_price=None)
        self.assertEqual(pos.invested_capital, 600.00)
        self.assertIsNone(pos.market_value)
        self.assertIsNone(pos.gain_loss)
        self.assertIsNone(pos.gain_loss_percent)

        d = pos.to_dict()
        self.assertEqual(d["Current Price ($)"], "UNPRICED")
        self.assertEqual(d["Market Value ($)"], "N/A")

    def test_input_validation_rejections(self):
        # Empty symbol
        with self.assertRaises(ValueError):
            Position("", quantity=10, purchase_price=100)

        # Non-positive quantity
        with self.assertRaises(ValueError):
            Position("AAPL", quantity=0, purchase_price=100)
        with self.assertRaises(ValueError):
            Position("AAPL", quantity=-5, purchase_price=100)

        # Non-positive purchase price
        with self.assertRaises(ValueError):
            Position("AAPL", quantity=10, purchase_price=0)
        with self.assertRaises(ValueError):
            Position("AAPL", quantity=10, purchase_price=-50)

        # Negative current price
        with self.assertRaises(ValueError):
            Position("AAPL", quantity=10, purchase_price=100, current_price=-10)


class TestPortfolioTracker(unittest.TestCase):
    """Tests portfolio aggregation, constituents lookup, and CSV export."""

    def setUp(self):
        self.tracker = PortfolioTracker()

    def test_portfolio_aggregates(self):
        self.tracker.add_position("AAPL", 10.0, 100.0, 110.0)
        self.tracker.add_position("MSFT", 5.0, 200.0, 220.0)

        # Total invested: 1000 + 1000 = 2000
        self.assertEqual(self.tracker.total_invested_capital(), 2000.00)
        # Total market value: 1100 + 1100 = 2200
        val, all_priced = self.tracker.total_market_value()
        self.assertEqual(val, 2200.00)
        self.assertTrue(all_priced)

        # Total gain: 100 + 100 = 200
        gl, all_priced = self.tracker.total_gain_loss()
        self.assertEqual(gl, 200.00)
        self.assertTrue(all_priced)

    def test_unpriced_aggregate_behavior(self):
        self.tracker.add_position("AAPL", 10.0, 100.0, 110.0)
        self.tracker.add_position("GOOGL", 5.0, 100.0, None)  # unpriced

        val, all_priced = self.tracker.total_market_value()
        self.assertEqual(val, 1100.00)
        self.assertFalse(all_priced)

    def test_csv_export_and_append(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "test_report.csv"
            self.tracker.add_position("AAPL", 2.0, 150.0, 160.0)

            # First export creates file with header
            saved_file = self.tracker.export_csv_report(csv_path, preserve_existing=True)
            self.assertTrue(saved_file.is_file())

            with open(saved_file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                self.assertEqual(len(rows), 2)  # Header + 1 record
                self.assertEqual(rows[0][1], "Symbol")
                self.assertEqual(rows[1][1], "AAPL")

            # Second export appends
            self.tracker.export_csv_report(csv_path, preserve_existing=True)
            with open(saved_file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                self.assertEqual(len(rows), 3)  # Header + 2 records

    def test_constituents_catalog(self):
        data_file = Path(__file__).resolve().parent.parent / "data" / "constituents.csv"
        loader = ConstituentsLoader(data_file)
        if data_file.is_file():
            catalog = loader.load()
            self.assertGreater(len(catalog), 400)
            self.assertTrue(loader.is_valid_constituent("AAPL"))
            info = loader.get_info("AAPL")
            self.assertIsNotNone(info)
            self.assertIn("Apple", info["Security"])


if __name__ == "__main__":
    unittest.main()
