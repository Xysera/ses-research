import sys, json, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))
import pandas as pd
from synth import simulate
ROOT = Path(os.environ.get("XYSERA_002_ROOT", HERE.parents[1]))
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
ROLE = {"C0_baseline": "baseline", "C1_pen_high": "penalty", "C2_rew_high": "reward", "C3_neutral": "neutral",
        "C4_third_party": "third_party", "C5_pen_low": "mirror"}
def conv(d, role_map):
    d = d[d.cond.isin(role_map)].copy()
    d["role"] = d.cond.map(role_map); d["item_id"] = d["id"]; d["template"] = d.k
    d["correct"] = d.gen_correct; d["response_letter"] = d.gen; d["correct_letter"] = d.ans
    d["severity"] = d.sev; d["source"] = d.src
    return d[["item_id", "template", "role", "correct", "response_letter", "correct_letter", "severity", "source"]]
def cases():
    out = {}
    for m in MODELS:
        raw = pd.DataFrame(map(json.loads, open(ROOT / "results" / f"confirm_{m}.jsonl")))
        out[f"study1_contextual_{m}"] = (conv(raw, ROLE), "contextual", None)
        d7 = raw[(raw.cond.isin(["C0_baseline", "C3_neutral", "C7_instructed"])) & (raw.k < 3)]
        out[f"study1_instructed_{m}"] = (conv(d7, {"C0_baseline": "baseline", "C3_neutral": "neutral", "C7_instructed": "penalty"}), "instructed", None)
    for scn, kw, corr in [("none", {}, None), ("generic", {}, None), ("positional", {}, None),
                          ("consequence", {}, None), ("consequence", {}, {"R2": True})]:
        nm = f"synthetic_{scn}" + ("_corr" if corr else "")
        out[nm] = (simulate(scn, **kw), "contextual", corr)
    return out
