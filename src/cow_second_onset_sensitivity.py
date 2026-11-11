"""EXP-002-I: sensibilidad a StartYear2 con datos COW locales. Stdlib solamente."""
import argparse, csv, io, json, zipfile, hashlib
from pathlib import Path
from collections import defaultdict

def analyze(system_zip, war_csv, test_start=1950, strength=5):
    with zipfile.ZipFile(system_zip) as z:
        names=[n for n in z.namelist() if n.lower().endswith("system2024.csv") and not n.startswith("__MACOSX")]
        if len(names)!=1: raise ValueError("system2024.csv ausente o ambiguo")
        members=list(csv.DictReader(io.TextIOWrapper(z.open(names[0]),encoding="utf-8-sig")))
    with open(war_csv,encoding="utf-8-sig",newline="") as f:
        wars=list(csv.DictReader(f))
    universe={(int(r["ccode"]),int(r["year"])) for r in members if 1816<=int(r["year"])<=2007}
    primary={(int(r["ccode"]),int(r["StartYear1"])) for r in wars if 1816<=int(r["StartYear1"])<=2007}
    second={(int(r["ccode"]),int(r["StartYear2"])) for r in wars if 1816<=int(r["StartYear2"])<=2007}
    if not (primary|second)<=universe: raise ValueError("Eventos fuera de cobertura")
    by_year=defaultdict(list)
    for c,y in universe: by_year[y].append(c)
    def score(events):
        k=n=0
        ek,en=defaultdict(int),defaultdict(int)
        ss0=ss1=0.0
        nt=ne=0
        for year in sorted(by_year):
            block=by_year[year]
            if year>=test_start:
                p0=(k+0.5)/(n+1)
                for c in block:
                    p1=(ek[c]+strength*p0)/(en[c]+strength)
                    outcome=int((c,year) in events)
                    ss0+=(p0-outcome)**2
                    ss1+=(p1-outcome)**2
                    nt+=1
                    ne+=outcome
            for c in block:
                outcome=int((c,year) in events)
                k+=outcome
                n+=1
                ek[c]+=outcome
                en[c]+=1
        if not nt: raise ValueError("Periodo de prueba vacio")
        return {"n_test":nt,"events_test":ne,"brier_B0":ss0/nt,
                "brier_B1":ss1/nt,"delta_B1_minus_B0":(ss1-ss0)/nt}
    return {"experiment":"EXP-002","stage":"002-I","test_start":test_start,
        "strength":strength,"source_sha256":{
        "system_zip":hashlib.sha256(Path(system_zip).read_bytes()).hexdigest(),
        "wars_csv":hashlib.sha256(Path(war_csv).read_bytes()).hexdigest()},
        "membership_rows":len(members),"war_rows":len(wars),
        "coverage_rows":len(universe),"primary_state_years":len(primary),
        "secondary_onsets":len(second),"new_secondary_state_years":len(second-primary),
        "new_secondary_keys":[{"ccode":c,"year":y} for c,y in sorted(second-primary,key=lambda t:(t[1],t[0]))],
        "primary_only":score(primary),"including_second":score(primary|second),
        "warning":"Sensibilidad exploratoria, no validacion causal ni reconciliacion definitiva de reingresos."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("system_zip")
    p.add_argument("war_csv")
    p.add_argument("--test-start",type=int,default=1950)
    p.add_argument("--output")
    a=p.parse_args()
    result=json.dumps(analyze(a.system_zip,a.war_csv,a.test_start),ensure_ascii=False,indent=2)+"\n"
    if a.output: Path(a.output).write_text(result,encoding="utf-8")
    else: print(result,end="")

if __name__=="__main__": main()
