"""Same frozen trial matrix, prompts and scoring as run_exp.py / run_exp_v2.py; adds request-level parallelism
(llama-server --parallel P with P client threads) for GPU throughput. Results are written in deterministic item order
per (condition, template) group. usage: run_exp_v3.py MODEL STAGE [--tpl N] [--sens_tpl N] [--tag PREFIX] [--par P]"""
import json, os, sys, argparse, time, datetime, subprocess, platform
from concurrent.futures import ThreadPoolExecutor
import lib
from lib import *
ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("stage"); ap.add_argument("--tpl", type=int, default=N_TPL)
ap.add_argument("--conds", default=",".join(CONDS + EXPL)); ap.add_argument("--sens_tpl", type=int, default=0)
ap.add_argument("--tag", default=""); ap.add_argument("--par", type=int, default=4)
a = ap.parse_args()
class PServer(Server):
    def __enter__(self):
        path = f"{ROOT}/models/{MODELS[self.name]}"
        self.proc = subprocess.Popen(["llama-server", "-m", path, "--port", str(PORT), "-c", str(4096 * a.par), "-ngl", "99",
                                      "--parallel", str(a.par), "--no-webui", "--log-disable"],
                                     stdout=open(f"{ROOT}/logs/server_{self.name}.log", "a"), stderr=subprocess.STDOUT)
        import requests
        for _ in range(300):
            try:
                if requests.get(f"http://127.0.0.1:{PORT}/health", timeout=2).status_code == 200: return self
            except Exception: pass
            time.sleep(1)
        raise RuntimeError("server did not start")
pool = {d["id"]: d for d in map(json.loads, (open(f"{ROOT}/data/pool.jsonl")))}
ids = json.load(open(f"{ROOT}/data/items_{a.model}.json"))[a.stage]
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
meta = dict(backend=ver, host=platform.platform(), python=platform.python_version(), parallel=a.par)
print("expected trials", len(plan) * len(ids), "already done", len(done), meta, flush=True)
repo = os.environ.get("HF_UPLOAD_REPO")
def upload():
    if not repo: return
    from huggingface_hub import HfApi
    for p in (out, fail):
        if os.path.exists(p): HfApi().upload_file(path_or_fileobj=p, path_in_repo=f"results_out/{os.path.basename(p)}", repo_id=repo, repo_type="dataset")
s = PServer(a.model); s.__enter__()
def one(job):
    c, k, iid = job; it = pool[iid]; perm = perm_for(iid, k); qn = qnum_for(iid, k)
    msgs, ans, sev = build_messages(it, c, k, perm, qn)
    text, lps = s.ask(msgs)
    return dict(trial_id=f"{a.model}|{c}|{k}|{iid}", model=a.model, stage=a.stage, cond=c, k=k, id=iid, src=it["src"], sev=sev,
                perm=perm, qn=qn, ans=ans, raw=text, status="ok", ts=datetime.datetime.utcnow().isoformat(), **score(text, lps, ans))
try:
    with open(out, "a") as f, ThreadPoolExecutor(a.par) as ex:
        for gi, (c, k) in enumerate(plan):
            todo = [(c, k, iid) for iid in ids if (c, k, iid) not in done]
            if todo:
                for attempt in range(4):
                    try: rows = list(ex.map(one, todo)); break
                    except Exception as e:
                        open(fail, "a").write(json.dumps(dict(group=f"{c}|{k}", attempt=attempt, err=repr(e)[:300], ts=datetime.datetime.utcnow().isoformat())) + "\n")
                        s.__exit__(); time.sleep(3); s.__enter__()
                else: raise RuntimeError(f"persistent inference failure in group {c} {k}")
                for r in rows: f.write(json.dumps(r) + "\n")
                f.flush()
            print(a.model, c, k, flush=True)
            if gi % 10 == 9: upload()
finally:
    s.__exit__(); upload()
print("RUN COMPLETE", flush=True)
