"""Confirmatory/pilot analysis. usage: analysis.py STAGE [OUTCOME=gen_correct|p_correct] [NBOOT]"""
import json, sys, collections
import numpy as np, pandas as pd
from scipy import stats
ROOT = "/Users/torinetheridge/002"
stage = sys.argv[1]; outcome = sys.argv[2] if len(sys.argv) > 2 else "gen_correct"
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
MARGIN = 0.02
rng = np.random.default_rng(20021022)

def load(m):
    df = pd.DataFrame(map(json.loads, open(f"{ROOT}/results/{stage}_{m}.jsonl")))
    return df
def mats(df, outcome):
    ids = sorted(df.id.unique()); X = {}
    for c, g in df.groupby("cond"):
        ks = sorted(g.k.unique())
        piv = g.pivot_table(index="id", columns="k", values=outcome, aggfunc="mean").reindex(ids)
        X[c] = piv
    return ids, X
def boot_diff(fn, X, ids, NB):
    """fn maps dict cond->(I,K) array (already resampled) to scalar. Two-way cluster bootstrap over items & templates."""
    I = len(ids); est = {}
    base = {c: v.values for c, v in X.items()}
    obs = fn(base)
    bs = np.empty(NB)
    for b in range(NB):
        ii = rng.integers(0, I, I)
        r = {}
        for c, v in base.items():
            K = v.shape[1]; kk = rng.integers(0, K, K)
            r[c] = v[np.ix_(ii, kk)]
        bs[b] = fn(r)
    return obs, bs
def summ(obs, bs):
    lo, hi = np.percentile(bs, [2.5, 97.5]); lo90, hi90 = np.percentile(bs, [5, 95])
    p_one = (np.sum(bs <= 0) + 1) / (len(bs) + 1)       # H: obs > 0 (one-sided)
    return dict(est=obs, ci95=(lo, hi), ci90=(lo90, hi90), se=bs.std(), p_one=p_one,
                equiv=bool(lo90 > -MARGIN and hi90 < MARGIN))
H1 = lambda r: np.nanmean(r["C2_rew_high"]) - np.nanmean(r["C1_pen_high"])
H2 = lambda r: 0.5 * (np.nanmean(r["C3_neutral"]) + np.nanmean(r["C4_third_party"])) - np.nanmean(r["C1_pen_high"])
H2b = lambda r: np.nanmean(r["C0_baseline"]) - np.nanmean(r["C1_pen_high"])
H5 = lambda r: np.nanmean(r["C5_pen_low"]) - np.nanmean(r["C1_pen_high"])
if __name__ == "__main__":
    res = {}
    for m in MODELS:
        try: df = load(m)
        except FileNotFoundError: continue
        ids, X = mats(df, outcome)
        row = {"n_items": len(ids), "means": {c: float(np.nanmean(v.values)) for c, v in X.items()}}
        for nm, fn in (("H1_rew_minus_pen", H1), ("H2_ctrl_minus_pen", H2), ("base_minus_pen", H2b), ("pen_low_minus_pen_high", H5)):
            if all(c in X for c in ("C0_baseline", "C1_pen_high", "C2_rew_high", "C3_neutral", "C4_third_party", "C5_pen_low")):
                obs, bs = boot_diff(fn, X, ids, NB); row[nm] = summ(obs, bs)
        res[m] = row
        print(m, json.dumps({k: (v if not isinstance(v, dict) else {a: (np.round(b, 4).tolist() if isinstance(b, (tuple, float, np.floating)) else b) for a, b in v.items()}) for k, v in row.items()}, indent=1, default=float))
    json.dump(res, open(f"{ROOT}/results/analysis_{stage}_{outcome}.json", "w"), indent=1, default=float)
