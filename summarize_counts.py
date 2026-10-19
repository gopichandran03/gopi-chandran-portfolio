#!/usr/bin/env python3
"""Summarize an RNA-seq gene-count matrix (educational example, not a full pipeline)."""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV with gene_id and one column per sample")
    parser.add_argument("--outdir", required=True, help="Output directory")
    args = parser.parse_args()
    inp, out = Path(args.input), Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(inp)
    if "gene_id" not in df.columns:
        raise SystemExit("Input must contain a 'gene_id' column.")
    if df["gene_id"].isna().any() or df["gene_id"].duplicated().any():
        raise SystemExit("gene_id values must be non-empty and unique.")
    sample_cols = [c for c in df.columns if c != "gene_id"]
    if not sample_cols:
        raise SystemExit("No sample columns found.")
    counts = df[sample_cols]
    if counts.isna().any().any() or (counts < 0).any().any():
        raise SystemExit("Counts must be non-missing and non-negative.")
    if not all(pd.api.types.is_numeric_dtype(counts[c]) for c in sample_cols):
        raise SystemExit("All sample columns must be numeric.")
    if ((counts % 1) != 0).any().any():
        raise SystemExit("Counts must be integer-valued.")
    summary = pd.DataFrame({
        "sample": sample_cols,
        "library_size": [int(counts[c].sum()) for c in sample_cols],
        "genes_detected_count_gt_0": [int((counts[c] > 0).sum()) for c in sample_cols],
        "zero_count_fraction": [float((counts[c] == 0).mean()) for c in sample_cols],
    })
    summary.to_csv(out / "sample_qc_summary.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(summary["sample"], summary["library_size"])
    ax.set_title("Example RNA-seq library sizes")
    ax.set_ylabel("Total counts")
    ax.set_xlabel("Sample")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(out / "library_size.png", dpi=180)
    plt.close(fig)
    metadata = {
        "input": str(inp),
        "samples": sample_cols,
        "genes": int(len(df)),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Educational count-matrix summary; example data are synthetic."
    }
    (out / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Validated {len(df)} genes across {len(sample_cols)} samples.")
    print(f"Outputs written to: {out}")

if __name__ == "__main__":
    main()
