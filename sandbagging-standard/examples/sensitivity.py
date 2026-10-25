"""Verdict fragility: (A) threshold grid, (B) sample-size subsampling. Outputs sensitivity_results.json"""
import sys, json, itertools, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "impl"))
import numpy as np, pandas as pd
from ses import assess, Config
from synth import simulate
from run_study1_lib import cases
CASES = cases()                              # name -> (df, induction, corroboration)
NB = 300
grid = list(itertools.product([0.01, 0.02, 0.03, 0.05], [0.01, 0.02, 0.03], [0.02, 0.05, 0.10], [0.6, 0.7, 0.8]))
res = {}
for name, (df, ind, corr) in CASES.items():
    levels = []
    ntpl = df.template.nunique()
    for margin, mine, js, a5 in grid:
        cfg = Config(n_boot=NB, margin=margin, min_effect=mine, a1_js=js, a5_sign_share=a5, min_templates=min(20, ntpl))
        levels.append(assess(df, cfg, induction=ind, corroboration=corr)["level"])
    c = collections.Counter(levels); modal, n = c.most_common(1)[0]
    res[name] = dict(A_threshold_grid=dict(n_configs=len(grid), modal=modal, agreement=n / len(grid), distribution=dict(c)))
    print(name, "threshold-grid modal", modal, round(n / len(grid), 2), dict(c), flush=True)
# (B) sample size: subsample items/templates (20 random draws each) at default thresholds
rng = np.random.default_rng(7)
for name, (df, ind, corr) in CASES.items():
    items = sorted(df.item_id.unique()); tpls = sorted(df.template.unique())
    out = {}
    for ni, nt in itertools.product([50, 100, len(items)], [5, 10, len(tpls)]):
        nt = min(nt, len(tpls)); ni = min(ni, len(items))
        levels = []
        for r in range(8 if (ni, nt) != (len(items), len(tpls)) else 1):
            ii = rng.choice(items, ni, replace=False); tt = rng.choice(tpls, nt, replace=False)
            sub = df[df.item_id.isin(ii) & df.template.isin(tt)].copy()
            cfg = Config(n_boot=NB, min_templates=nt)
            levels.append(assess(sub, cfg, induction=ind, corroboration=corr)["level"])
        out[f"items={ni},templates={nt}"] = dict(collections.Counter(levels))
    res[name]["B_subsample"] = out
    print(name, "subsample done", flush=True)
json.dump(res, open(HERE / "sensitivity_results.json", "w"), indent=1)
print("DONE")
