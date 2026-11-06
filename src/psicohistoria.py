"""EXP-002: evaluacion temporal de eventos historicos, solo biblioteca estandar."""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

REQUIRED = ("entity", "year", "outcome")


def read_panel(path):
    """Lee CSV entidad-anio. outcome binario: evento en ese anio (no riesgo futuro)."""
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(REQUIRED).issubset(reader.fieldnames):
            raise ValueError("Se requieren columnas entity,year,outcome")
        rows = []
        seen = set()
        for line, row in enumerate(reader, 2):
            entity = (row["entity"] or "").strip()
            try:
                year = int(row["year"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Linea {line}: year invalido") from exc
            outcome = (row["outcome"] or "").strip()
            if not entity or outcome not in ("0", "1"):
                raise ValueError(f"Linea {line}: entity vacio u outcome distinto de 0/1")
            key = (entity, year)
            if key in seen:
                raise ValueError(f"Linea {line}: entidad-anio duplicado: {key}")
            seen.add(key)
            rows.append({"entity": entity, "year": year, "outcome": int(outcome)})
    if not rows:
        raise ValueError("CSV vacio")
    return sorted(rows, key=lambda r: (r["year"], r["entity"]))


def brier(p, y):
    if not 0 <= p <= 1 or y not in (0, 1):
        raise ValueError("probabilidad u outcome invalidos")
    return (p - y) ** 2


def evaluate_baseline(rows, test_start, prior_alpha=0.5, prior_beta=0.5):
    """Baseline historico expansivo, sin datos del mismo anio de prediccion."""
    if prior_alpha <= 0 or prior_beta <= 0:
        raise ValueError("Los hiperparametros deben ser positivos")
    years = sorted({r["year"] for r in rows})
    if test_start <= years[0] or test_start > years[-1]:
        raise ValueError("test_start debe dejar anios anteriores y posteriores")
    by_year = defaultdict(list)
    for r in rows:
        by_year[r["year"]].append(r)
    successes = 0
    trials = 0
    forecasts = []
    for year in years:
        block = by_year[year]
        if year >= test_start:
            if trials == 0:
                raise ValueError("Sin observaciones de entrenamiento")
            p = (successes + prior_alpha) / (trials + prior_alpha + prior_beta)
            for r in block:
                forecasts.append({"entity": r["entity"], "year": year,
                                  "p": p, "outcome": r["outcome"], "brier": brier(p, r["outcome"])})
        successes += sum(r["outcome"] for r in block)
        trials += len(block)
    return {"status": "baseline_only", "test_start": test_start,
            "n_train_before_test": sum(r["year"] < test_start for r in rows),
            "n_test": len(forecasts),
            "test_brier": sum(f["brier"] for f in forecasts) / len(forecasts),
            "predictions": forecasts,
            "warning": "Baseline de incidencia anual; no predice crisis a 5 anios. La unidad entidad-anio debe ser comparable y sin fuga temporal."}


def main():
    parser = argparse.ArgumentParser(description="EXP-002: baseline temporal")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--test-start", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate_baseline(read_panel(args.csv), args.test_start)
    output = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
