"""EXP-002-E: comparacion pareada B0/B1 por bloques anuales, sin datos externos."""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from src.psicohistoria import read_panel, evaluate_baseline, evaluate_entity_baseline

def compare(rows, test_start, strength=5.0, bootstrap=1000, seed=20261110):
    if bootstrap < 1:
        raise ValueError("bootstrap debe ser positivo")
    a = evaluate_baseline(rows, test_start)["predictions"]
    b = evaluate_entity_baseline(rows, test_start, strength)["predictions"]
    keys_a = [(x["entity"], x["year"], x["outcome"]) for x in a]
    keys_b = [(x["entity"], x["year"], x["outcome"]) for x in b]
    if keys_a != keys_b:
        raise ValueError("B0 y B1 no evaluados en las mismas observaciones")
    by_year = defaultdict(list)
    for x, y in zip(a, b):
        by_year[x["year"]].append(y["brier"] - x["brier"])
    years = sorted(by_year)
    def mean_diff(selected_years):
        vals = [d for yr in selected_years for d in by_year[yr]]
        return sum(vals) / len(vals)
    observed = mean_diff(years)
    rng = random.Random(seed)
    replicates = sorted(mean_diff([rng.choice(years) for _ in years]) for _ in range(bootstrap))
    lo = replicates[int(0.025 * (bootstrap - 1))]
    hi = replicates[int(0.975 * (bootstrap - 1))]
    return {"experiment": "EXP-002", "stage": "002-E", "data_kind": "supplied_panel",
            "test_start": test_start, "strength": strength,
            "n_test": len(a), "n_test_years": len(years),
            "events_test": sum(x["outcome"] for x in a),
            "brier_B0": sum(x["brier"] for x in a)/len(a),
            "brier_B1": sum(x["brier"] for x in b)/len(b),
            "delta_B1_minus_B0": observed, "bootstrap_year_blocks": bootstrap,
            "bootstrap_seed": seed, "delta_ci95_percentile": [lo, hi],
            "warning": "Bootstrap anual descriptivo; no corrige dependencia entre paises, cambio temporal ni sesgo de seleccion. No es evidencia empirica sin panel historico verificado."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("panel_csv", type=Path)
    p.add_argument("--test-start", type=int, required=True)
    p.add_argument("--strength", type=float, default=5.0)
    p.add_argument("--bootstrap", type=int, default=1000)
    p.add_argument("--seed", type=int, default=20261110)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = compare(read_panel(args.panel_csv), args.test_start, args.strength, args.bootstrap, args.seed)
    s = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(s, encoding="utf-8")
    else:
        print(s, end="")

if __name__ == "__main__":
    main()
