"""EXP-002: puerta de calidad para panel entidad-anio, sin dependencias externas.

La cobertura debe declararse explicitamente: ausencia de evento NO equivale a cero
si el proveedor no certifica observacion de la entidad-anio.
"""
import csv
import hashlib
import json
from pathlib import Path


def audit_panel(panel_path, coverage_path):
    """Ambos CSV deben tener entity,year; panel ademas outcome=0/1.
    coverage contiene SOLO entidad-anios observables, no inferidos.
    """
    def load(path, fields):
        with open(path, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not set(fields).issubset(reader.fieldnames):
                raise ValueError(f"{path}: faltan columnas {fields}")
            return list(reader)
    panel = load(panel_path, ("entity", "year", "outcome"))
    coverage = load(coverage_path, ("entity", "year"))
    def key(row):
        entity = (row.get("entity") or "").strip()
        if not entity:
            raise ValueError("Entidad vacia")
        try:
            year = int(row["year"])
        except (ValueError, TypeError) as e:
            raise ValueError("Anio invalido") from e
        return entity, year
    cover_keys = [key(row) for row in coverage]
    if len(set(cover_keys)) != len(cover_keys):
        raise ValueError("Cobertura duplicada")
    cover = set(cover_keys)
    observed = set()
    positives = 0
    for row in panel:
        k = key(row)
        if k in observed:
            raise ValueError(f"Panel duplicado: {k}")
        observed.add(k)
        if k not in cover:
            raise ValueError(f"Fila fuera de cobertura: {k}")
        outcome = (row["outcome"] or "").strip()
        if outcome not in ("0", "1"):
            raise ValueError(f"Outcome invalido en {k}")
        positives += outcome == "1"
    missing = sorted(cover - observed)
    return {
        "status": "quality_gate_only",
        "panel_rows": len(panel),
        "coverage_rows": len(cover),
        "positives": positives,
        "missing_observed_rows": len(missing),
        "complete": len(missing) == 0 and len(panel) > 0,
        "year_min": min((y for _, y in cover), default=None),
        "year_max": max((y for _, y in cover), default=None),
        "panel_sha256": hashlib.sha256(Path(panel_path).read_bytes()).hexdigest(),
        "coverage_sha256": hashlib.sha256(Path(coverage_path).read_bytes()).hexdigest(),
        "warning": "Cobertura declarada externamente: el programa no verifica la legitimidad de su fuente ni convierte ausencias en ceros."
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("panel")
    p.add_argument("coverage")
    args = p.parse_args()
    print(json.dumps(audit_panel(args.panel, args.coverage), indent=2))
