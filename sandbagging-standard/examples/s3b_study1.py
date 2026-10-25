"""S3 worked example: difficulty-accuracy correlation on Study 1 logs.
Item difficulty = 1 - mean screening accuracy of the OTHER four models (independent of the model analysed)."""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))
import numpy as np, pandas as pd
from scipy import stats
from run_study1_lib import cases, MODELS, ROOT
scr = {m: pd.DataFrame(map(json.loads, open(ROOT / "data" / f"screen_{m}.jsonl"))).groupby("id").gen_correct.mean() for m in MODELS}
allc = cases(); out = {}
for m in MODELS:
    others = pd.concat([scr[o] for o in MODELS if o != m], axis=1).mean(axis=1)
    df, ind, corr = allc[f"study1_contextual_{m}"]
    df = df.assign(difficulty=1 - df.item_id.map(others))
    row = {}
    for role in ("baseline", "neutral", "penalty", "reward", "third_party"):
        g = df[df.role == role].groupby("item_id").agg(acc=("correct", "mean"), d=("difficulty", "first"))
        r, p = stats.spearmanr(g.d, g.acc); row[role] = (round(float(r), 3), float(p))
    out[m] = row
    print(m, {k: v[0] for k, v in row.items()})
json.dump(out, open(HERE / "s3b_study1_results.json", "w"), indent=1)
