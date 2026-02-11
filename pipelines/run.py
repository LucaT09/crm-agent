import argparse
import os
from datetime import datetime, timedelta, timezone

import pandas as pd
import yaml


def load_spec(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_parent_dir(file_path: str) -> None:
    parent = os.path.dirname(file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def build_demo_dataframe(spec: dict, n_rows: int = 100) -> pd.DataFrame:
    commodities = spec.get("commodities") or ["Lithium", "Cobalt"]
    metrics = spec.get("metrics") or ["price_usd_t"]

    now = datetime.now(timezone.utc)
    rows = []

    # Create deterministic-ish demo data
    for i in range(n_rows):
        d = (now.date() - timedelta(days=i % 30)).isoformat()
        commodity = commodities[i % len(commodities)]
        metric = metrics[i % len(metrics)]
        value = float(10000 + (i % 200) * 10)  # dummy positive number
        unit = "USD/t"
        source = "demo"
        retrieved_at = now.isoformat()

        rows.append(
            {
                "date": d,
                "commodity": commodity,
                "metric": metric,
                "value": value,
                "unit": unit,
                "source": source,
                "retrieved_at": retrieved_at,
            }
        )

    df = pd.DataFrame(rows)
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Path to YAML spec file")
    parser.add_argument("--out", required=True, help="Output CSV path")
    args = parser.parse_args()

    spec = load_spec(args.spec)

    df = build_demo_dataframe(spec, n_rows=100)

    ensure_parent_dir(args.out)
    df.to_csv(args.out, index=False)

    print(f"Wrote CSV: {args.out} ({len(df)} rows)")


if __name__ == "__main__":
    main()
