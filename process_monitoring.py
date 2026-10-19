#!/usr/bin/env python3
"""Illustrative process monitoring for synthetic data; not a validated QC method."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--column", default="measurement")
    a = p.parse_args()
    df = pd.read_csv(a.input)
    if a.column not in df.columns:
        raise SystemExit(f"Missing required column: {a.column}")
    x = pd.to_numeric(df[a.column], errors="coerce")
    if x.isna().any():
        raise SystemExit("Measurement column must contain numeric, non-missing values.")
    if len(x) < 2:
        raise SystemExit("At least two observations are required for this demonstration.")
    mean, sd = float(x.mean()), float(x.std(ddof=1))
    lower, upper = mean - 3 * sd, mean + 3 * sd
    result = df.copy()
    result["flag_outside_illustrative_limits"] = (x < lower) | (x > upper)
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / "process_monitoring_flags.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(range(1, len(x)+1), x, marker="o", linewidth=1.5)
    ax.axhline(mean, linestyle="-", label="Mean")
    ax.axhline(upper, linestyle="--", label="Illustrative +3 SD")
    ax.axhline(lower, linestyle="--", label="Illustrative -3 SD")
    ax.set_xlabel("Observation")
    ax.set_ylabel(a.column)
    ax.set_title("Synthetic process-monitoring example")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "process_monitoring.png", dpi=180)
    plt.close(fig)
    print(f"Mean={mean:.3f}; sample SD={sd:.3f}; flagged={(result['flag_outside_illustrative_limits']).sum()}")
    print(f"Outputs written to: {out}")

if __name__ == "__main__":
    main()
