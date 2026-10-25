"""usage: run_exp.py MODEL STAGE(pilot|confirm) OUT_SUFFIX [--tpl N] [--items N] [--conds C1,C2..] [--sens]"""
import json, os, sys, argparse
from lib import *
ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("stage"); ap.add_argument("--tpl", type=int, default=N_TPL)
ap.add_argument("--items", type=int, default=10**9); ap.add_argument("--conds", default=",".join(CONDS + EXPL))
ap.add_argument("--sens_tpl", type=int, default=0)
a = ap.parse_args()
pool = {d["id"]: d for d in map(json.loads, (open(f"{ROOT}/data/pool.jsonl")))}
sel = json.load(open(f"{ROOT}/data/items_{a.model}.json"))
ids = sel[a.stage][:a.items]
conds = a.conds.split(",")
out = f"{ROOT}/results/{a.stage}_{a.model}.jsonl"
done = set()
if os.path.exists(out):
    for d in map(json.loads, open(out)): done.add((d["cond"], d["k"], d["id"]))
plan = []
for c in conds:
    n = min(a.tpl, 10) if c == "C6_pressure" else a.tpl
    for k in range(n): plan.append((c, k))
if a.sens_tpl:
    for k in range(a.sens_tpl): plan.append(("C7_instructed", k))
with Server(a.model) as s, open(out, "a") as f:
    for c, k in plan:
        for iid in ids:
            if (c, k, iid) in done: continue
            it = pool[iid]; perm = perm_for(iid, k); qn = qnum_for(iid, k)
            msgs, ans, sev = build_messages(it, c, k, perm, qn)
            text, lps = s.ask(msgs)
            f.write(json.dumps(dict(model=a.model, stage=a.stage, cond=c, k=k, id=iid, src=it["src"], sev=sev,
                                    perm=perm, qn=qn, ans=ans, raw=text, **score(text, lps, ans))) + "\n")
        f.flush()
        print(a.model, c, k, flush=True)
