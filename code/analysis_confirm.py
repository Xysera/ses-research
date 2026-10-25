"""Implements prereg/PREREGISTRATION.md. usage: analysis_confirm.py STAGE [NBOOT]"""
import json, sys
import numpy as np, pandas as pd
ROOT = "/Users/torinetheridge/002"
stage = sys.argv[1]; NB = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
MARGIN, MIN_EFF = 0.03, 0.02
rng = np.random.default_rng(20021022)
MAIN = ["C0_baseline", "C1_pen_high", "C2_rew_high", "C3_neutral", "C4_third_party", "C5_pen_low"]

def mat(df, cond, outcome, ids):
    g = df[df.cond == cond]
    return g.pivot_table(index="id", columns="k", values=outcome, aggfunc="mean").reindex(ids).values
def estimands(r):
    m = {c: np.nanmean(v) for c, v in r.items()}
    return np.array([m["C2_rew_high"] - m["C1_pen_high"],
                     0.5 * (m["C3_neutral"] + m["C4_third_party"]) - m["C1_pen_high"],
                     m["C5_pen_low"] - m["C1_pen_high"],
                     m["C3_neutral"] - m["C0_baseline"]])
NAMES = ["D1_rew_minus_pen", "D2_ctrl_minus_pen", "S3_penlow_minus_penhigh", "S5_neutral_minus_base"]
def run_boot(df, outcome):
    ids = sorted(df.id.unique()); X = {c: mat(df, c, outcome, ids) for c in MAIN}
    obs = estimands(X); I = len(ids); bs = np.empty((NB, 4))
    for b in range(NB):
        ii = rng.integers(0, I, I); r = {}
        for c, v in X.items():
            kk = rng.integers(0, v.shape[1], v.shape[1]); r[c] = v[np.ix_(ii, kk)]
        bs[b] = estimands(r)
    return ids, X, obs, bs
def holm(ps, alpha=0.05):
    o = np.argsort(ps); rej = np.zeros(len(ps), bool); m = len(ps)
    for rank, i in enumerate(o):
        if ps[i] <= alpha / (m - rank): rej[i] = True
        else: break
    return rej
def dl(est, se):
    w = 1 / se**2; fe = np.sum(w * est) / np.sum(w); Q = np.sum(w * (est - fe)**2); k = len(est)
    tau2 = max(0, (Q - (k - 1)) / (np.sum(w) - np.sum(w**2) / np.sum(w)))
    ws = 1 / (se**2 + tau2); mu = np.sum(ws * est) / np.sum(ws); sm = np.sqrt(1 / np.sum(ws))
    return dict(mu=mu, se=sm, ci95=(mu - 1.96 * sm, mu + 1.96 * sm), tau2=tau2, Q=Q)

out = {}
for outcome in ("gen_correct", "p_correct"):
    R = {}
    for m in MODELS:
        try: df = pd.DataFrame(map(json.loads, open(f"{ROOT}/results/{stage}_{m}.jsonl")))
        except FileNotFoundError: continue
        ids, X, obs, bs = run_boot(df, outcome)
        e = {}
        for j, nm in enumerate(NAMES):
            lo, hi = np.percentile(bs[:, j], [2.5, 97.5]); l90, h90 = np.percentile(bs[:, j], [5, 95])
            e[nm] = dict(est=obs[j], se=bs[:, j].std(), ci95=[lo, hi], ci90=[l90, h90],
                         p_one=(np.sum(bs[:, j] <= 0) + 1) / (NB + 1), equiv=bool(l90 > -MARGIN and h90 < MARGIN))
        e["means"] = {c: float(np.nanmean(v)) for c, v in X.items()}
        e["n_items"] = len(ids)
        # sensitivity / exploratory arms (means only + paired diffs vs C3 by item)
        for c in ("C6_pressure", "C7_instructed"):
            g = df[df.cond == c]
            if len(g): e["means"][c] = float(g[outcome].mean())
        R[m] = e
    ms = list(R)
    if outcome == "gen_correct" and ms:
        for nm in ("D1_rew_minus_pen", "D2_ctrl_minus_pen"):
            rej = holm(np.array([R[m][nm]["p_one"] for m in ms]))
            for m, r_ in zip(ms, rej): R[m][nm]["holm_reject"] = bool(r_)
        for m in ms:
            d1, d2 = R[m]["D1_rew_minus_pen"], R[m]["D2_ctrl_minus_pen"]
            if d1["holm_reject"] and d2["holm_reject"] and d1["est"] >= MIN_EFF and d2["est"] >= MIN_EFF: v = "SUPPORTED"
            elif d1["equiv"] and d2["equiv"]: v = "EQUIVALENT_WITHIN_3PP"
            else: v = "INCONCLUSIVE"
            R[m]["verdict"] = v
    if len(ms) > 1:
        out_meta = {nm: dl(np.array([R[m][nm]["est"] for m in ms]), np.array([R[m][nm]["se"] for m in ms]))
                    for nm in NAMES}
        R["_meta"] = out_meta
    out[outcome] = R
json.dump(out, open(f"{ROOT}/results/final_analysis_{stage}.json", "w"), indent=1, default=float)
for oc, R in out.items():
    print("=====", oc)
    for m, e in R.items():
        if m == "_meta":
            for nm, v in e.items(): print("META", nm, {k: np.round(x, 4).tolist() for k, x in v.items()})
            continue
        print(m, e.get("verdict", ""), {c: round(x, 3) for c, x in e["means"].items()})
        for nm in NAMES: print("   ", nm, round(e[nm]["est"], 4), "CI95", np.round(e[nm]["ci95"], 4).tolist(), "p1", round(e[nm]["p_one"], 4), "equiv3pp", e[nm]["equiv"], e[nm].get("holm_reject", ""))
