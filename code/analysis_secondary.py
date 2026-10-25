"""Secondary analyses S1,S2,S6,S8 + source heterogeneity (exploratory). usage: analysis_secondary.py STAGE"""
import json, sys
import numpy as np, pandas as pd
from scipy import stats
ROOT = "/Users/torinetheridge/002"; stage = sys.argv[1]
MODELS = ["qwen25_7b", "llama31_8b", "phi35_mini", "qwen3_4b", "gemma3_4b"]
out = {}
for m in MODELS:
    try: d = pd.DataFrame(map(json.loads, open(f"{ROOT}/results/{stage}_{m}.jsonl")))
    except FileNotFoundError: continue
    r = {}
    # S1 dose-response: template-level mean accuracy vs severity, C1 and C4 (and C2 for reference)
    for c in ("C1_pen_high", "C4_third_party", "C2_rew_high", "C5_pen_low"):
        t = d[d.cond == c].groupby(["k", "sev"]).gen_correct.mean().reset_index()
        sl = stats.linregress(t.sev, t.gen_correct)
        r[f"S1_slope_{c}"] = dict(slope=sl.slope, p=sl.pvalue, by_sev=d[d.cond == c].groupby("sev").gen_correct.mean().round(4).to_dict())
    # S2 recovery: C1 errors -> C0 on identical (id,k)
    b = d[d.cond == "C0_baseline"].set_index(["id", "k"]).gen_correct
    for c in ("C1_pen_high", "C3_neutral"):
        e = d[(d.cond == c) & (d.gen_correct == 0)]
        kk = [(i, k) for i, k in zip(e.id, e.k) if (i, k) in b.index]
        r[f"S2_recovery_{c}"] = dict(n_errors=len(e), recovered_in_baseline=float(np.mean([b[x] for x in kk])) if kk else None)
    # S6 position bias: letter distribution C1 vs C3; below-chance cells
    for c in ("C0_baseline", "C1_pen_high", "C3_neutral", "C7_instructed"):
        g = d[d.cond == c]
        if len(g): r[f"S6_letters_{c}"] = g.gen.value_counts(normalize=True).round(3).to_dict()
    tab = pd.crosstab(d[d.cond.isin(["C1_pen_high", "C3_neutral"])].cond, d[d.cond.isin(["C1_pen_high", "C3_neutral"])].gen)
    r["S6_chi2_C1_vs_C3_letters_p"] = float(stats.chi2_contingency(tab)[1])
    cell = d[d.cond == "C1_pen_high"].groupby("k").gen_correct.mean()
    r["S6_template_means_C1"] = {"min": float(cell.min()), "max": float(cell.max()), "n_below_chance": int((cell < .25).sum())}
    # exploratory: by source
    r["EXP_by_source"] = d.pivot_table(index="src", columns="cond", values="gen_correct").round(3).to_dict()
    # S8 / C7 per model vs C3
    if (d.cond == "C7_instructed").any():
        r["S8_C7_minus_C3"] = float(d[d.cond == "C7_instructed"].gen_correct.mean() - d[d.cond == "C3_neutral"].gen_correct.mean())
    out[m] = r
json.dump(out, open(f"{ROOT}/results/secondary_{stage}.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float)[:3500])
