"""Final integrity audit of confirmatory data. Writes results/audit_report.json"""
import json, collections, hashlib
import pandas as pd, numpy as np
ROOT="/Users/torinetheridge/002"
MODELS=["qwen25_7b","llama31_8b","phi35_mini","qwen3_4b","gemma3_4b"]
EXPECT_TPL={"C0_baseline":20,"C1_pen_high":20,"C2_rew_high":20,"C3_neutral":20,"C4_third_party":20,"C5_pen_low":20,"C6_pressure":10,"C7_instructed":3}
import sys; sys.path.insert(0,f"{ROOT}/code")
from lib import build_messages, perm_for, qnum_for, make_note, score
pool={d["id"]:d for d in map(json.loads,open(f"{ROOT}/data/pool.jsonl"))}
rep={}
for m in MODELS:
    d=pd.DataFrame(map(json.loads,open(f"{ROOT}/results/confirm_{m}.jsonl")))
    sel=json.load(open(f"{ROOT}/data/items_{m}.json")); conf=set(sel["confirm"]); pil=set(sel["pilot"])
    exp=sum(EXPECT_TPL.values())*250
    r=dict(n=len(d),expected=exp,
           dup_cells=int(d.duplicated(["cond","k","id"]).sum()),
           cells_per_cond={c:int(n) for c,n in d.groupby("cond").size().items()},
           items=int(d.id.nunique()), items_in_confirm_set=bool(set(d.id)<=conf), overlap_with_pilot=len(set(d.id)&pil),
           no_letter_rate=float(d.gen.isna().mean()),
           templates_per_cond={c:int(n) for c,n in d.groupby("cond").k.nunique().items()},
           items_per_cell_min=int(d.groupby(["cond","k"]).id.nunique().min()))
    # item pairing: every item has every (cond,k) cell
    cnt=d.groupby("id").size(); r["cells_per_item_all_equal"]=bool(cnt.nunique()==1)
    # perm/qn consistency across conditions for the same (item,k)
    pm=d.assign(p=d.perm.astype(str)).groupby(["id","k"]).p.nunique(); r["perm_consistent_across_conds"]=bool((pm==1).all())
    # recompute prompts for a random 500 trials: permutation, answer letter, qnum equality; parse check
    s=d.sample(500,random_state=1); bad=0
    for _,x in s.iterrows():
        it=pool[x.id]; msgs,ans,sev=build_messages(it,x.cond,x.k,perm_for(x.id,x.k),qnum_for(x.id,x.k))
        if ans!=x.ans or list(x.perm)!=perm_for(x.id,x.k) or sev!=x.sev: bad+=1
        g=next((c for c in x.raw if c in "ABCD"),None)
        if g!=(x.gen if isinstance(x.gen,str) else None) or int(g==x.ans)!=x.gen_correct: bad+=1
    r["prompt_reconstruction_mismatches_in_500"]=bad
    r["lp_vs_gen_agreement"]=float((d.gen==d.lp_argmax).mean())
    # severity balance in C1,C2,C4,C5
    r["severity_counts_C1_templates"]=d[d.cond=="C1_pen_high"].groupby("sev").k.nunique().to_dict()
    r["status_not_ok"]=int((d.get("status","ok")!="ok").sum()) if "status" in d else 0
    r["has_timestamps"]="ts" in d
    rep[m]=r
json.dump(rep,open(f"{ROOT}/results/audit_report.json","w"),indent=1,default=str)
for m,r in rep.items(): print(m,{k:r[k] for k in ("n","expected","dup_cells","items","items_in_confirm_set","overlap_with_pilot","no_letter_rate","cells_per_item_all_equal","perm_consistent_across_conds","prompt_reconstruction_mismatches_in_500","lp_vs_gen_agreement")})
