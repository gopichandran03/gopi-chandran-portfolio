# RNA-seq count-matrix QC demonstration

## What this does
This educational workflow reads `../../data/example_counts.csv`, checks the count matrix, computes per-sample library-size summaries, creates a sample-level QC CSV, and saves a library-size bar plot.

## Run
From the repository root:

```bash
python workflows/rnaseq/summarize_counts.py \
  --input data/example_counts.csv \
  --outdir results/rnaseq_qc
```

Install dependencies first:

```bash
python -m pip install -r requirements.txt
```

## Input format
First column: `gene_id`; remaining columns: non-negative integer counts for each sample. The included dataset is **synthetic example data**, not biological evidence.

## Outputs
- `sample_qc_summary.csv`
- `library_size.png`
- `run_metadata.json`

## Interpretation and limitations
This is a basic count-matrix QC illustration. It does not process FASTQ files and does not replace FastQC/MultiQC, alignment, transcript quantification, batch-effect assessment, differential-expression analysis, or functional annotation. A full project workflow may use FastQC/MultiQC, HISAT2, StringTie or featureCounts, DESeq2/edgeR, and documented annotation databases, depending on the study design. Choose tools and statistical methods based on the experimental design and data type.
