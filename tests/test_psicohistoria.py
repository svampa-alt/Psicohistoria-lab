"""Pruebas sin dependencias externas para EXP-002."""
import csv
import tempfile
import unittest
from pathlib import Path
from src.psicohistoria import read_panel, brier, evaluate_baseline, evaluate_entity_baseline


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


    def test_b1_shrinkage_and_no_same_year_leakage(self):
        rows = [
            {"entity": "A", "year": 2000, "outcome": 1},
            {"entity": "B", "year": 2000, "outcome": 0},
            {"entity": "A", "year": 2001, "outcome": 0},
            {"entity": "B", "year": 2001, "outcome": 1},
            {"entity": "C", "year": 2001, "outcome": 1},
        ]
        out = evaluate_entity_baseline(rows, 2001, strength=2)
        self.assertEqual(out["n_test"], 3)
        self.assertAlmostEqual(out["predictions"][0]["p"], 2 / 3)
        self.assertAlmostEqual(out["predictions"][1]["p"], 1 / 3)
        self.assertAlmostEqual(out["predictions"][2]["p"], 0.5)

    def test_b1_strength_invalid(self):
        with self.assertRaises(ValueError):
            evaluate_entity_baseline([{"entity": "A", "year": 2000, "outcome": 1},
                                      {"entity": "A", "year": 2001, "outcome": 0}], 2001, strength=0)



class TestCoverageGate(unittest.TestCase):
    def test_missing_is_not_automatically_zero(self):
        from src.coverage import audit_panel
        with tempfile.TemporaryDirectory() as d:
            panel, coverage = Path(d)/"panel.csv", Path(d)/"coverage.csv"
            panel.write_text("entity,year,outcome\nA,2000,1\n", encoding="utf-8")
            coverage.write_text("entity,year\nA,2000\nB,2000\n", encoding="utf-8")
            result = audit_panel(panel, coverage)
            self.assertFalse(result["complete"])
            self.assertEqual(result["missing_observed_rows"], 1)

    def test_outside_coverage_rejected(self):
        from src.coverage import audit_panel
        with tempfile.TemporaryDirectory() as d:
            panel, coverage = Path(d)/"panel.csv", Path(d)/"coverage.csv"
            panel.write_text("entity,year,outcome\nB,2000,0\n", encoding="utf-8")
            coverage.write_text("entity,year\nA,2000\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "fuera de cobertura"):
                audit_panel(panel, coverage)

if __name__ == "__main__":
    unittest.main()
