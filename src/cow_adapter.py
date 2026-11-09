"""EXP-002-D: adaptador COW, datos locales del proveedor; no descarga ni redistribuye."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

FIRST, LAST = 1816, 2007

def read_csv(path, required):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not set(required).issubset(reader.fieldnames):
            raise ValueError(f"{path}: columnas requeridas {required}; encontradas {reader.fieldnames}")
        return list(reader)

def integer(value, label):
    try:
        v = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label}: entero invalido {value!r}") from exc
    return v

def build_panel(system_path, war_path):
    """system2024 (CCode,Year); InterStateWarData_v4.0 (Ccode,StartYear1,WarNum).
    Evento: comienzo de participacion estatal segun StartYear1, no comienzo de guerra global.
    """
    system = read_csv(system_path, ("CCode", "Year"))
    wars = read_csv(war_path, ("Ccode", "StartYear1", "WarNum"))
    universe = set()
    for r in system:
        c = integer(r["CCode"], "CCode sistema")
        y = integer(r["Year"], "Year sistema")
        if FIRST <= y <= LAST:
            if (c, y) in universe:
                raise ValueError(f"membresia duplicada {(c,y)}")
            universe.add((c,y))
    if not universe:
        raise ValueError("sin cobertura 1816-2007")
    events, outside, unknown = set(), [], 0
    for r in wars:
        c = integer(r["Ccode"], "Ccode guerra")
        y = integer(r["StartYear1"], "StartYear1")
        if y == -9:
            unknown += 1
            continue
        if FIRST <= y <= LAST:
            if (c, y) not in universe:
                outside.append({"ccode": c, "year": y, "war": r["WarNum"]})
            else:
                events.add((c,y))
    if unknown or outside:
        raise ValueError(f"fuente no reconciliada: fechas desconocidas={unknown}, eventos fuera de membresia={outside[:8]} (total={len(outside)})")
    keys = sorted(universe, key=lambda z: (z[1], z[0]))
    return {
        "panel": [{"entity":str(c), "year":y, "outcome":int((c,y) in events)} for c,y in keys],
        "coverage": [{"entity":str(c), "year":y} for c,y in keys],
        "metadata": {
            "status":"constructed_not_validated",
            "definition":"onset of state participation: StartYear1; StartYear2 not modeled",
            "system_rows":len(system), "war_rows":len(wars),
            "coverage_rows":len(keys), "positive_state_years":len(events),
            "system_sha256":hashlib.sha256(Path(system_path).read_bytes()).hexdigest(),
            "war_sha256":hashlib.sha256(Path(war_path).read_bytes()).hexdigest(),
            "caveats":["COW membership any-time-in-year; possible event before membership within same year",
                       "StartYear2/re-entry or second episodes not counted",
                       "Zero assumes exhaustive provider war registry for 1816-2007",
                       "No source data should be committed; inspect codebooks and exclusions before inference"]
        }
    }

def main():
    p=argparse.ArgumentParser(description="EXP-002-D: COW local-only adapter")
    p.add_argument("system_csv")
    p.add_argument("war_csv")
    p.add_argument("--out-dir",required=True,type=Path)
    a=p.parse_args()
    result=build_panel(a.system_csv,a.war_csv)
    a.out_dir.mkdir(parents=True,exist_ok=True)
    for name,rows,fields in (("panel.csv",result["panel"],("entity","year","outcome")),("coverage.csv",result["coverage"],("entity","year"))):
        with (a.out_dir/name).open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    (a.out_dir/"metadata.json").write_text(json.dumps(result["metadata"],indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["metadata"],indent=2))

if __name__=="__main__":
    main()
