"""Release-gate audit for SES v1.0-rc1.

Run from the Initiative 002 repository root after regenerating the analyses.
It independently checks immutable raw-log hashes, trial accounting, regenerated
analysis hashes, manuscript table values, inferential outcomes, and SES tests.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STD = ROOT / "sandbagging-standard"
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
RAW_EXPECTED = {
    "gemma3_4b": "485a860122a2d4bab394f2f2bacd4130920175b9991d072db4cda8306ea64559",
    "llama31_8b": "0befc5c4f7d6ed008c47fa6891822c3cf6a19979de52be526361f202f3a27f87",
    "phi35_mini": "0a5f9cd7653723e55277359745fe15d54a1e654665e35884d872389b7994a14a",
    "qwen25_7b": "3a8c60473f3010c088489a42df386bb658346b5f1c3e40667a5bda3507416044",
    "qwen3_4b": "4fc8c8b3d50c42c6868f661d296b0e3b2fddcbe41eee68e954bb61acbd784198",
}
DERIVED_EXPECTED = {
    "results/audit_report.json": "0df9b8fdf8badeaa35c757284606275402c9a908636da5d9016b5a4b0265d31a",
    "results/final_analysis_confirm.json": "5f6dc91b2d4440929ea44d0edac8a245ef7df57672024412ff60854416c6736e",
    "results/secondary_confirm.json": "91e21e4a2bd91fc0668bed856da58a4bb8ef3a96b29e41c72b315b096746c7c5",
}
PAPER_MEANS = {
    "qwen25_7b": [97.80, 95.40, 95.66, 95.46, 95.54, 95.50],
    "llama31_8b": [98.72, 93.98, 93.90, 94.24, 93.96, 94.00],
    "phi35_mini": [98.10, 95.92, 96.00, 96.00, 96.14, 96.06],
    "qwen3_4b": [97.74, 94.50, 94.66, 94.62, 94.54, 94.50],
    "gemma3_4b": [98.82, 94.64, 94.52, 94.46, 94.38, 94.62],
}
ROLES = ["C0_baseline", "C1_pen_high", "C2_rew_high", "C3_neutral", "C4_third_party", "C5_pen_low"]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)
    print("PASS", message)


def main() -> None:
    total = 0
    for model in MODELS:
        path = ROOT / "results" / f"confirm_{model}.jsonl"
        check(sha(path) == RAW_EXPECTED[model], f"raw hash {model}")
        n = sum(1 for _ in path.open(encoding="utf-8"))
        check(n == 33_250, f"trial count {model}=33,250")
        total += n
    check(total == 166_250, "total confirmatory trials=166,250")

    for rel, expected in DERIVED_EXPECTED.items():
        check(sha(ROOT / rel) == expected, f"regenerated hash {rel}")

    analysis = json.loads((ROOT / "results/final_analysis_confirm.json").read_text())
    for model, expected in PAPER_MEANS.items():
        got = [round(100 * analysis["gen_correct"][model]["means"][r], 2) for r in ROLES]
        check(got == expected, f"Table 2 means {model}")
        for key in ("D1_rew_minus_pen", "D2_ctrl_minus_pen"):
            cell = analysis["gen_correct"][model][key]
            check(cell["equiv"] and not cell["holm_reject"], f"{model} {key} equivalence/no rejection")

    paper = (STD / "paper/PAPER_DRAFT.md").read_text(encoding="utf-8")
    check("166,250" in paper and "indeterminate" in paper, "paper carries trial count and indeterminate outcome")
    placeholder = bool(re.search(r"Public archive URL pending deposit|stable public preregistration URL/DOI will be inserted", paper))
    print("OPEN publisher metadata: preregistration deposit" if placeholder else "PASS public preregistration identifier inserted")

    test = subprocess.run([sys.executable, str(STD / "impl/test_ses.py")], capture_output=True, text=True, check=True)
    passes = test.stdout.count("PASS test_")
    check(passes == 14, "14/14 SES implementation tests")
    print("RELEASE AUDIT PASSED")


if __name__ == "__main__":
    main()
