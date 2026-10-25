"""Exploratory demo (NOT part of the preregistered study): Qwen3-4B with thinking enabled, 8 known items x {C0, C3, C6}."""
import json, requests, random
from lib import *
pool={d["id"]:d for d in map(json.loads,open(f"{ROOT}/data/pool.jsonl"))}
sel=json.load(open(f"{ROOT}/data/items_qwen3_4b.json"))["pilot"]   # pilot items only
ids=[i for i in sel if pool[i]["src"] in ("arith","mmlu")][:8]
out=open(f"{ROOT}/results/think_demo_qwen3_4b.jsonl","w")
with Server("qwen3_4b") as s:
    for iid in ids:
        for cond,k in (("C0_baseline",2),("C3_neutral",2),("C6_pressure",2)):
            it=pool[iid]; msgs,ans,sev=build_messages(it,cond,k,perm_for(iid,k),qnum_for(iid,k))
            r=requests.post(f"http://127.0.0.1:{PORT}/v1/chat/completions",json=dict(messages=msgs,max_tokens=3000,temperature=0.6,seed=1,
                chat_template_kwargs={"enable_thinking":True}),timeout=900).json()
            m=r["choices"][0]["message"]
            out.write(json.dumps(dict(id=iid,cond=cond,ans=ans,reasoning=m.get("reasoning_content"),content=m.get("content"),finish=r["choices"][0]["finish_reason"],toks=r["usage"]["completion_tokens"]))+"\n"); out.flush()
            print(iid,cond,flush=True)
print("DONE")
