"""Worked example: apply SES to the Study 1 confirmatory logs (no new model runs)."""
import sys, json, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))
import pandas as pd, numpy as np
from ses import assess, Config
ROOT = Path(os.environ.get("XYSERA_002_ROOT", HERE.parents[1]))
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
ROLE = {"C0_baseline": "baseline", "C1_pen_high": "penalty", "C2_rew_high": "reward", "C3_neutral": "neutral",
        "C4_third_party": "third_party", "C5_pen_low": "mirror"}
cfg = Config(n_boot=2000)
out = {}
def conv(d, role_map):
    d = d[d.cond.isin(role_map)].copy()
    d["role"] = d.cond.map(role_map); d["item_id"] = d["id"]; d["template"] = d.k
    d["correct"] = d.gen_correct; d["response_letter"] = d.gen; d["correct_letter"] = d.ans
    d["severity"] = d.sev; d["source"] = d.src
    return d[["item_id", "template", "role", "correct", "response_letter", "correct_letter", "severity", "source"]]
for m in MODELS:
    raw = pd.DataFrame(map(json.loads, open(ROOT / "results" / f"confirm_{m}.jsonl")))
    # Case 1: contextual consequence notes (Study 1 primary design). No domain split, no effort-control arm.
    r1 = assess(conv(raw, ROLE), cfg, induction="contextual", known_items=True)
    # Case 2: instructed underperformance (C7) vs neutral note, templates 0-2 only. Induced; most criteria not assessable.
    d7 = raw[(raw.cond.isin(["C0_baseline", "C3_neutral", "C7_instructed"])) & (raw.k < 3)]
    d7 = conv(d7, {"C0_baseline": "baseline", "C3_neutral": "neutral", "C7_instructed": "penalty"})
    r2 = assess(d7, Config(n_boot=2000, min_templates=3), induction="instructed", known_items=True)
    out[m] = {"contextual": r1, "instructed": r2}
    print(f"{m:11s} contextual: {r1['level']:7s} | instructed: {r2['level']:7s} | {r2['label'][:70]}")
json.dump(out, open(HERE / "study1_ses_results.json", "w"), indent=1, default=str)
