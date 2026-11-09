"""Pruebas sintéticas del adaptador COW EXP-002-D."""
import csv
import tempfile
import unittest
from pathlib import Path
from src.cow_adapter import build_panel
from src.coverage import audit_panel
from src.psicohistoria import evaluate_baseline, evaluate_entity_baseline

def write(path, cols, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(cols); w.writerows(rows)

class CowAdapterTests(unittest.TestCase):
    def test_synthetic_panel_and_temporal_scores(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            system=d/"system.csv"; wars=d/"wars.csv"
            write(system,["CCode","Year"],[(2,2000),(20,2000),(2,2001),(20,2001),(2,2002),(20,2002)])
            write(wars,["Ccode","StartYear1","WarNum"],[(2,2000,1),(20,2002,2)])
            result=build_panel(system,wars)
            self.assertEqual(result["metadata"]["positive_state_years"],2)
            self.assertEqual(len(result["panel"]),6)
            self.assertEqual([x["outcome"] for x in result["panel"]],[1,0,0,0,0,1])
            b0=evaluate_baseline(result["panel"],2001)
            b1=evaluate_entity_baseline(result["panel"],2001)
            self.assertEqual(b0["n_test"],4)
            self.assertEqual(b1["n_test"],4)
            self.assertAlmostEqual(b0["predictions"][0]["p"],0.5)
    def test_reject_unmatched_event(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); s=d/"s.csv"; w=d/"w.csv"
            write(s,["CCode","Year"],[(2,2000)])
            write(w,["Ccode","StartYear1","WarNum"],[(20,2000,1)])
            with self.assertRaises(ValueError):
                build_panel(s,w)
    def test_reject_unknown_onset(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); s=d/"s.csv"; w=d/"w.csv"
            write(s,["CCode","Year"],[(2,2000)])
            write(w,["Ccode","StartYear1","WarNum"],[(2,-9,1)])
            with self.assertRaises(ValueError):
                build_panel(s,w)

if __name__=="__main__":
    unittest.main()
