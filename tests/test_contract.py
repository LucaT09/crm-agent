import os
import pandas as pd
import yaml


def load_spec(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_output_csv_contract():
    # In GitHub Actions set via env var
    spec_path = os.environ.get("SPEC_PATH", "specs/example.yaml")
    spec = load_spec(spec_path)

    out_path = spec["outputs"][0]["path"]
    assert os.path.exists(out_path), f"Expected output CSV at {out_path}, but not found."

    df = pd.read_csv(out_path)

    # Column contract
    expected_cols = [c["name"] for c in spec["outputs"][0]["schema"]["columns"]]
    assert list(df.columns) == expected_cols, f"Columns mismatch. Expected {expected_cols}, got {list(df.columns)}"

    # Quality rules
    rules = spec.get("quality_rules", [])
    for rule in rules:
        if rule["rule"] == "no_nulls":
            cols = rule["columns"]
            assert df[cols].isnull().sum().sum() == 0, f"Nulls found in columns: {cols}"
        if rule["rule"] == "row_count_min":
            min_rows = int(rule["min_rows"])
            assert len(df) >= min_rows, f"Row count {len(df)} < min_rows {min_rows}"
