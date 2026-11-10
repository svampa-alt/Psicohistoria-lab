"""EXP-002-E: pruebas reproducibles de comparacion pareada."""
import unittest
from src.compare_baselines import compare

class TestCompare(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"entity": e, "year": y, "outcome": o}
            for y, outcomes in [(2000, (1, 0)), (2001, (0, 1)), (2002, (1, 0))]
            for e, o in zip(("A", "B"), outcomes)
        ]
    def test_paired_sample_and_determinism(self):
        a = compare(self.rows, 2001, strength=2, bootstrap=100, seed=7)
        b = compare(self.rows, 2001, strength=2, bootstrap=100, seed=7)
        self.assertEqual(a, b)
        self.assertEqual(a["n_test"], 4)
        self.assertEqual(a["n_test_years"], 2)
        self.assertEqual(a["events_test"], 2)
        self.assertAlmostEqual(a["delta_B1_minus_B0"], a["brier_B1"]-a["brier_B0"])
    def test_invalid_bootstrap(self):
        with self.assertRaises(ValueError):
            compare(self.rows, 2001, bootstrap=0)
    def test_same_year_not_leaked(self):
        changed = [dict(r) for r in self.rows]
        for r in changed:
            if r["year"] == 2002:
                r["outcome"] = 1-r["outcome"]
        # El score 2001 no puede depender de las etiquetas 2002.
        a = compare([r for r in self.rows if r["year"] <= 2001], 2001, bootstrap=20)
        b = compare([r for r in changed if r["year"] <= 2001], 2001, bootstrap=20)
        self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()
