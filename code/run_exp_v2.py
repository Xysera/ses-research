"""Reliability wrapper around the frozen run_exp.py logic (identical prompts, parameters, trial matrix).
Additions only: retry with server restart on infrastructure errors (outcome-independent), trial ids,
UTC timestamps, backend metadata, failure log, optional periodic upload to a HF dataset repo.
usage: run_exp_v2.py MODEL STAGE [--tpl N] [--sens_tpl N] [--tag PREFIX]"""
import json, os, sys, argparse, time, datetime, subprocess, platform
from lib import *
ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("stage"); ap.add_argument("--tpl", type=int, default=N_TPL)
ap.add_argument("--items", type=int, default=10**9); ap.add_argument("--conds", default=",".join(CONDS + EXPL))
ap.add_argument("--sens_tpl", type=int, default=0); ap.add_argument("--tag", default="")
a = ap.parse_args()
pool = {d["id"]: d for d in map(json.loads, (open(f"{ROOT}/data/pool.jsonl")))}
ids = json.load(open(f"{ROOT}/data/items_{a.model}.json"))[a.stage][:a.items]
conds = a.conds.split(",")
prefix = a.tag or a.stage
out = f"{ROOT}/results/{prefix}_{a.model}.jsonl"; fail = f"{ROOT}/results/failures_{prefix}_{a.model}.jsonl"
done = set()
if os.path.exists(out):
    for d in map(json.loads, open(out)): done.add((d["cond"], d["k"], d["id"]))
plan = []
for c in conds:
    n = min(a.tpl, 10) if c == "C6_pressure" else a.tpl
    for k in range(n): plan.append((c, k))
for k in range(a.sens_tpl): plan.append(("C7_instructed", k))
try: ver = subprocess.run(["llama-server", "--version"], capture_output=True, text=True).stderr.strip().splitlines()[0:2]
except Exception as e: ver = [str(e)]
meta = dict(backend=ver, host=platform.platform(), python=platform.python_version())
print("expected trials", len(plan) * len(ids), "already done", len(done), meta, flush=True)
repo = os.environ.get("HF_UPLOAD_REPO")
def upload():
    if not repo: return
    from huggingface_hub import HfApi
    api = HfApi()
    for p in (out, fail):
        if os.path.exists(p): api.upload_file(path_or_fileobj=p, path_in_repo=f"results_out/{os.path.basename(p)}", repo_id=repo, repo_type="dataset")
def ask_retry(s, msgs, key):
    for attempt in range(4):
        try: return s.ask(msgs)
        except Exception as e:
            open(fail, "a").write(json.dumps(dict(trial=key, attempt=attempt, err=repr(e)[:300], ts=datetime.datetime.utcnow().isoformat())) + "\n")
            s.__exit__(); time.sleep(3); s.__enter__()
    raise RuntimeError("persistent inference failure " + str(key))
s = Server(a.model); s.__enter__()
try:
    with open(out, "a") as f:
        for gi, (c, k) in enumerate(plan):
            for iid in ids:
                if (c, k, iid) in done: continue
                it = pool[iid]; perm = perm_for(iid, k); qn = qnum_for(iid, k)
                msgs, ans, sev = build_messages(it, c, k, perm, qn)
                key = f"{a.model}|{c}|{k}|{iid}"
                text, lps = ask_retry(s, msgs, key)
                f.write(json.dumps(dict(trial_id=key, model=a.model, stage=a.stage, cond=c, k=k, id=iid, src=it["src"], sev=sev,
                                        perm=perm, qn=qn, ans=ans, raw=text, status="ok",
                                        ts=datetime.datetime.utcnow().isoformat(), **score(text, lps, ans))) + "\n")
            f.flush(); print(a.model, c, k, flush=True)
            if gi % 10 == 9: upload()
finally:
    s.__exit__(); upload()
print("RUN COMPLETE", flush=True)
