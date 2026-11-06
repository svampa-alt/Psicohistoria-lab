"""Pruebas sin dependencias externas para EXP-002."""
import csv
import tempfile
import unittest
from pathlib import Path
from src.psicohistoria import read_panel, brier, evaluate_baseline


class TestBaseline(unittest.TestCase):
    def test_brier(self):
        self.assertAlmostEqual(brier(0.25, 1), 0.5625)
        self.assertAlmostEqual(brier(0.25, 0), 0.0625)

    def test_no_same_year_leakage(self):
        rows = [
            {"entity": "A", "year": 2000, "outcome": 0},
            {"entity": "B", "year": 2000, "outcome": 1},
            {"entity": "A", "year": 2001, "outcome": 1},
            {"entity": "B", "year": 2001, "outcome": 0},
            {"entity": "A", "year": 2002, "outcome": 1},
        ]
        result = evaluate_baseline(rows, 2001)
        self.assertEqual(result["n_test"], 3)
        self.assertAlmostEqual(result["predictions"][0]["p"], 0.5)
        self.assertAlmostEqual(result["predictions"][1]["p"], 0.5)
        self.assertAlmostEqual(result["predictions"][2]["p"], 0.5)

    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.csv"
            path.write_text("entity,year,outcome\nA,2000,1\nA,2000,0\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicado"):
                read_panel(path)

    def test_no_train_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_baseline([{"entity": "A", "year": 2000, "outcome": 1}], 2000)


if __name__ == "__main__":
    unittest.main()
