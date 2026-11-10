"""EXP-002-G: reproducible official COW download and temporal comparison.
Downloads only to a user-selected local directory; never commits third-party rows.
"""
import argparse
import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path
from src.cow_adapter import build_panel
from src.compare_baselines import compare

WAR_URL = "https://correlatesofwar.org/wp-content/uploads/Inter-StateWarData_v4.0.csv"
SYSTEM_URL = "https://correlatesofwar.org/wp-content/uploads/System2024.zip"
MAX_BYTES = 8_000_000

def download(url):
    with urllib.request.urlopen(url, timeout=45) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Descarga demasiado grande")
    return data

def membership_csv(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        choices = [n for n in z.namelist() if n.lower().endswith(".csv") and "system2024" in n.lower() and not n.startswith("__MACOSX")]
        if len(choices) != 1:
            raise ValueError(f"Se esperaba exactamente un CSV system2024; encontrados {choices}")
        data = z.read(choices[0])
        if len(data) > MAX_BYTES:
            raise ValueError("CSV de membresia demasiado grande")
        return data, choices[0]

def run(out_dir, test_start=1950):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    war = download(WAR_URL)
    archive = download(SYSTEM_URL)
    system, system_member = membership_csv(archive)
    war_path, sys_path = out_dir / "Inter-StateWarData_v4.0.csv", out_dir / "system2024.csv"
    war_path.write_bytes(war)
    sys_path.write_bytes(system)
    report = {"experiment":"EXP-002", "stage":"002-G", "status":"downloaded_not_yet_reconciled",
              "source_urls":{"war":WAR_URL,"membership":SYSTEM_URL},
              "sha256":{"war":hashlib.sha256(war).hexdigest(),"membership_zip":hashlib.sha256(archive).hexdigest(),"membership_csv":hashlib.sha256(system).hexdigest()},
              "membership_archive_member":system_member,"test_start":test_start}
    try:
        result = build_panel(sys_path, war_path)
        report["adapter_metadata"] = result["metadata"]
        report["status"] = "constructed_not_validated"
        report["comparison"] = compare(result["panel"], test_start=test_start, strength=5, bootstrap=1000, seed=20261110)
        report["status"] = "comparison_exploratory_not_validated"
    except (ValueError, KeyError, UnicodeError, csv.Error) as exc:
        report["blocking_error"] = str(exc)
    (out_dir / "EXP-002-G-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--test-start", type=int, default=1950)
    args = parser.parse_args()
    print(json.dumps(run(args.out_dir,args.test_start),ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
