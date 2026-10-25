# Sandbagging Evidence Standard (SES) v1.0-rc1

A preprint release candidate containing frozen SES v0.5 decision rules, a reference implementation and reproducible worked applications. It grades behavioural evidence; it is not a validated detector and does not infer intent.

- `sources/LEDGER.md`: sources used, what was actually read, quantities and limits.
- `criteria/STANDARD.md`: claim levels L0-L4, criteria K/A/C/S/R/E/I/W, decision table, reporting checklist.
- `impl/ses.py`: reference implementation (matched-cell two-way cluster bootstrap, equivalence, letter-distribution test, recovery, verdict). `impl/synth.py`: synthetic logs with known ground truth. `impl/test_ses.py`: 14 tests. `impl/release_audit.py`: release-gate reproduction checks.
- `examples/`: Study 1 worked example.
- `sources/SEARCH_PROTOCOL.md`, `examples/SENSITIVITY_REPORT.md`, `CHANGELOG.md`.

## Run
```
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python impl/test_ses.py
.venv/bin/python impl/release_audit.py
```
See `REPRODUCE.md` for the worked example and full-data layout.

## Log schema (DataFrame columns)
item_id, template, role (baseline|penalty|mirror|third_party|neutral|reward|effort_control), correct (0/1), response_letter, correct_letter; optional severity, source, domain (target|control). Cells (item_id, template) must be matched across roles (same option permutation).

## Status and limits
Preprint release candidate v1.0-rc1 by Torin Ethreidge, Lead Researcher and Senior Researcher at Xysera Research; decision rules remain SES v0.5. Public repository: `https://github.com/Xysera/ses-research`. Original code is Apache-2.0; the manuscript, original documentation, figures and original research data are CC BY 4.0; third-party materials retain their original terms. Exercised only against synthetic cases, a Study 1 null/artifact application, incomplete held-out organism cases, and a small negative exploratory screen. The standard supports claims of behaviour only, never intent. Not peer reviewed. See `paper/CITATION_AUDIT.md` for the claim audit.
