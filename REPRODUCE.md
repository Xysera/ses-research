# Reproducing Xysera Research Initiative 002

Requirements: Python 3.12+ (tested 3.14), `pip install -r requirements_frozen.txt`, llama.cpp `llama-server` on PATH, the five GGUF files (bartowski repos on Hugging Face; names and SHA-256 in `prereg/MANIFEST.txt`) in `models/`.
Paths: `code/lib.py` uses `ROOT=/Users/torinetheridge/002`; change it (or symlink) for another location.

1. Item pool: `python code/build_items.py` (seed 2002; needs `datasets`, internet for MMLU/ARC).
2. Screening: `python code/screen.py MODEL...` then `python code/select_items.py` (known items; pilot/confirm sets).
3. Pilot: `python code/run_exp.py MODEL pilot --tpl 6 --sens_tpl 3`.
4. Confirmatory: `python code/run_exp.py MODEL confirm --tpl 20 --sens_tpl 3` (or `run_exp_v2.py` for retry; `run_exp_v3.py --par 4` for batched GPU use; `job_run.sh` is the HF Jobs entrypoint).
5. Audit: `python code/audit.py`. Analysis: `python code/analysis_confirm.py confirm 10000` and `python code/analysis_secondary.py confirm`. Figures/tables: `python code/make_figures.py`.

Statistics, figures and tables reproduce exactly from `results/confirm_*.jsonl` (bootstrap seed 20021022). Re-running inference reproduces results only approximately (98-99% identical answers across llama.cpp builds/hardware). Integrity: `sha256sum -c prereg/MANIFEST.txt` (last line is a date and will warn) and `results/RESULTS_MANIFEST.txt`.
Provenance: Qwen3-4B, Gemma-3-4B, Phi-3.5-mini ran on an Apple M5 (llama.cpp build 11429, Metal); Qwen2.5-7B and Llama-3.1-8B on a T4 (HF Jobs, build 11804, 4 slots). Raw cloud outputs are in `results/hf/`. `results/confirm_qwen25_7b.mac_partial.jsonl` is an archived, unused partial laptop run.
