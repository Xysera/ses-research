# Reproducing the Sandbagging Evidence Standard

## Environment

Python 3.11 or newer is recommended. From this directory:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

The pinned versions are the versions used for the v0.5 release checks. The core implementation requires NumPy, pandas and SciPy; ReportLab builds the publication PDF.

## Fast validation

```bash
.venv/bin/python impl/test_ses.py
```

Expected result: fourteen `PASS` lines and exit status 0.

## Full release audit from raw logs

From the Initiative 002 repository root, verify the immutable input hashes, regenerate the audit and confirmatory statistics, then run the independent release assertions:

```bash
./.venv/bin/python code/audit.py
./.venv/bin/python code/analysis_confirm.py confirm 10000
./.venv/bin/python code/analysis_secondary.py confirm
./.venv/bin/python sandbagging-standard/impl/release_audit.py
```

The audit requires five complete confirmatory files with 33,250 rows each (166,250 total). It checks their recorded SHA-256 digests, the byte-level hashes of the regenerated audit/primary/secondary JSON, Table 2 values, D1/D2 equivalence and Holm outcomes, and all 14 implementation tests. The archived 9,250-row Qwen partial run is excluded.

## Worked Study 1 analysis

The checked-in derived results can be read without the large trial logs. To regenerate them, place the Initiative 002 repository so that `sandbagging-standard/` and `results/` share a parent directory, then run:

```bash
cd examples
../.venv/bin/python run_study1.py
```

Alternatively set `XYSERA_002_ROOT` to the directory containing `results/` and `data/`. The full Study 1 logs are approximately 59 MB and are distributed as separate reproducibility artifacts rather than embedded in the paper source package.

## Expected checked-in outputs

- `examples/study1_ses_results.json`
- `examples/sensitivity_results.json`
- `examples/s3b_study1_results.json`
- `examples/screen2_summary.csv`

The original model weights are not required to reproduce the SES classifications from the trial logs. They are required only to rerun model inference.

## Publication PDF

From the Initiative 002 repository root:

```bash
./.venv/bin/python sandbagging-standard/paper/build_pdf.py
```

The output is written to `output/pdf/xysera_sandbagging_evidence_standard_v1.0-rc1.pdf`.
