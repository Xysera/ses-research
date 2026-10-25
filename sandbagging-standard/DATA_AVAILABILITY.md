# Data and code availability

## Included in the source release

- Sandbagging Evidence Standard v0.5 and its decision rules.
- Reference implementation and 14 synthetic tests, including missing, invalid, zero-variance and statistically indeterminate cases.
- Source ledger, search protocol and citation audit.
- Derived Study 1 SES classifications and sensitivity outputs.
- Exploratory-screen summary.
- PDF builder and publication manuscript.
- SHA-256 release manifest.
- Release-gate audit script verifying raw and derived hashes, 166,250-trial accounting, manuscript table values, inferential outcomes and implementation tests.

## Separate reproducibility artifacts

The five complete Study 1 confirmatory logs contain 166,250 trials and occupy approximately 56 MB. They are present in the Initiative 002 repository but excluded from the compact source archive; the public deposit must include them as a separate data artifact. The exploratory screen contains 324 prompts and occupies approximately 1 MB and should accompany it:

- `results/confirm_qwen25_7b.jsonl`
- `results/confirm_llama31_8b.jsonl`
- `results/confirm_phi35_mini.jsonl`
- `results/confirm_qwen3_4b.jsonl`
- `results/confirm_gemma3_4b.jsonl`
- `results/screen2/results_out/*.jsonl`

`results/confirm_qwen25_7b.mac_partial.jsonl` is an archived, unused interrupted run and is not part of the analytic dataset. It may be retained for provenance but must be clearly labelled as excluded.

## Not redistributed

Model weights are not redistributed. The main Initiative 002 manifest records model filenames and SHA-256 hashes so independently obtained weights can be checked. Reproducing the paper's SES classifications from the raw logs does not require model weights or paid API access.

## Integrity and privacy

The study used harmless benchmark questions and model-generated text. The release contains no intended personal data, credentials or API keys. A final secret scan is required before public upload.
