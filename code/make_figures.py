import json, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT="/Users/torinetheridge/002"
A=json.load(open(f"{ROOT}/results/final_analysis_confirm.json"))
G=A["gen_correct"]; P=A["p_correct"]
M=["qwen25_7b","llama31_8b","phi35_mini","qwen3_4b","gemma3_4b"]
LAB={"qwen25_7b":"Qwen2.5-7B","llama31_8b":"Llama-3.1-8B","phi35_mini":"Phi-3.5-mini","qwen3_4b":"Qwen3-4B","gemma3_4b":"Gemma-3-4B"}
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
# Fig 1: accuracy by condition
conds=["C0_baseline","C3_neutral","C4_third_party","C1_pen_high","C2_rew_high","C5_pen_low","C6_pressure"]
names=["C0 no note","C3 neutral","C4 third-party\npenalty","C1 self penalty\n(high score)","C2 self reward\n(high score)","C5 self penalty\n(low score)","C6 high\npressure"]
fig,ax=plt.subplots(figsize=(9,4.2)); cols=["#4c78a8","#f58518","#54a24b","#e45756","#72b7b2","#b279a2"]
for i,m in enumerate(M):
    y=[G[m]["means"][c]*100 for c in conds]; ax.plot(range(len(conds)),y,"o-",color=cols[i],label=LAB[m],lw=1.2,ms=4)
ax.set_xticks(range(len(conds))); ax.set_xticklabels(names,fontsize=8); ax.set_ylabel("Accuracy on known items (%)"); ax.set_ylim(92,100)
ax.legend(frameon=False,fontsize=8,ncol=5,loc="upper center",bbox_to_anchor=(0.5,1.12)); fig.tight_layout(); fig.savefig("paper/figures/fig1_accuracy_by_condition.png",dpi=200); plt.close()
# Fig 2: forest plot D1, D2
fig,axs=plt.subplots(1,2,figsize=(9,3.8),sharey=True)
for ax,(nm,t) in zip(axs,[("D1_rew_minus_pen","D1: accuracy(reward) − accuracy(penalty)"),("D2_ctrl_minus_pen","D2: accuracy(controls) − accuracy(penalty)")]):
    ys=list(range(len(M)+1))[::-1]
    for y,m in zip(ys,M):
        e=G[m][nm]; ax.plot(e["ci95"],[y,y],color="#333",lw=1.5); ax.plot(e["est"]*100/100,y,"o",color="#e45756")
    meta=A["gen_correct"].get("_meta",{}).get(nm)
    if meta: ax.plot(meta["ci95"],[0,0],color="#333",lw=2.5); ax.plot(meta["mu"],0,"D",color="#4c78a8")
    ax.axvline(0,color="#888",lw=0.8); ax.axvspan(-0.03,0.03,color="#cfe3cf",alpha=0.5,zorder=0,label="±3 pp equivalence margin")
    ax.axvline(0.02,color="#e45756",ls=":",lw=0.8)
    ax.set_xlim(-0.04,0.04); ax.set_xticks([-0.03,-0.02,-0.01,0,0.01,0.02,0.03]); ax.set_xticklabels(["−3","−2","−1","0","+1","+2","+3"]); ax.set_xlabel("percentage points"); ax.set_title(t,fontsize=9)
    ax.set_yticks(ys); ax.set_yticklabels([LAB[m] for m in M]+["Pooled (RE)"])
axs[0].legend(frameon=False,fontsize=7,loc="lower left"); fig.tight_layout(); fig.savefig("paper/figures/fig2_primary_contrasts.png",dpi=200); plt.close()
# Fig 3: generic note effect and instructed sensitivity (C7)
fig,axs=plt.subplots(1,2,figsize=(9,3.6))
x=np.arange(len(M))
s5=[G[m]["S5_neutral_minus_base"] for m in M]
axs[0].bar(x,[e["est"]*100 for e in s5],color="#f58518",yerr=[[ (e["est"]-e["ci95"][0])*100 for e in s5],[(e["ci95"][1]-e["est"])*100 for e in s5]],capsize=3)
axs[0].axhline(0,color="#888",lw=.8); axs[0].set_xticks(x); axs[0].set_xticklabels([LAB[m] for m in M],rotation=25,ha="right",fontsize=8); axs[0].set_ylabel("pp"); axs[0].set_title("S5: neutral note − no note (generic note effect)",fontsize=9)
c7=[(G[m]["means"]["C7_instructed"]-G[m]["means"]["C3_neutral"])*100 for m in M]
axs[1].bar(x,c7,color="#4c78a8"); axs[1].axhline(0,color="#888",lw=.8); axs[1].set_xticks(x); axs[1].set_xticklabels([LAB[m] for m in M],rotation=25,ha="right",fontsize=8)
axs[1].set_title("S8 sensitivity check: explicit directive − neutral",fontsize=9); axs[1].set_ylabel("pp")
fig.tight_layout(); fig.savefig("paper/figures/fig3_note_effect_and_sensitivity.png",dpi=200); plt.close()
# Tables
def pct(x): return f"{x*100:.1f}"
with open("paper/tables/table1_accuracy.md","w") as f:
    f.write("| Model | "+" | ".join(["C0","C1","C2","C3","C4","C5","C6","C7*"])+" |\n|---|"+"---|"*8+"\n")
    for m in M:
        mm=G[m]["means"]; f.write(f"| {LAB[m]} | "+" | ".join(pct(mm[c]) for c in ["C0_baseline","C1_pen_high","C2_rew_high","C3_neutral","C4_third_party","C5_pen_low","C6_pressure","C7_instructed"])+" |\n")
with open("paper/tables/table2_primary.md","w") as f:
    f.write("| Model | D1 (pp) | 95% CI | Holm p (1-sided) | 90% CI inside ±3? | D2 (pp) | 95% CI | 90% CI inside ±3? | Verdict |\n|---|---|---|---|---|---|---|---|---|\n")
    # Holm-adjusted p from p_one
    for nm in ("D1_rew_minus_pen","D2_ctrl_minus_pen"):
        ps=np.array([G[m][nm]["p_one"] for m in M]); o=np.argsort(ps); adj=np.empty(len(ps)); run=0
        for r,i in enumerate(o): run=max(run,min(1,(len(ps)-r)*ps[i])); adj[i]=run
        for m,a in zip(M,adj): G[m][nm]["holm_p"]=float(a)
    for m in M:
        d1,d2=G[m]["D1_rew_minus_pen"],G[m]["D2_ctrl_minus_pen"]
        f.write(f"| {LAB[m]} | {d1['est']*100:+.2f} | [{d1['ci95'][0]*100:+.2f}, {d1['ci95'][1]*100:+.2f}] | {d1['holm_p']:.2f} | {'yes' if d1['equiv'] else 'no'} | {d2['est']*100:+.2f} | [{d2['ci95'][0]*100:+.2f}, {d2['ci95'][1]*100:+.2f}] | {'yes' if d2['equiv'] else 'no'} | {G[m]['verdict']} |\n")
    for nm in ("D1_rew_minus_pen","D2_ctrl_minus_pen"):
        v=G["_meta"][nm]; f.write(f"| Pooled {nm[:2]} (RE) | {v['mu']*100:+.2f} | [{v['ci95'][0]*100:+.2f}, {v['ci95'][1]*100:+.2f}] | | | | | | tau²={v['tau2']:.5f}, Q={v['Q']:.2f} |\n")
with open("paper/tables/table3_secondary.md","w") as f:
    f.write("| Model | S3 mirror (C5−C1, pp) | S5 note effect (C3−C0, pp) [95% CI] | S4 D1 on p_correct (pp) [95% CI] | S4 D2 (pp) | S8 C7−C3 (pp) |\n|---|---|---|---|---|---|\n")
    S=json.load(open(f"{ROOT}/results/secondary_confirm.json"))
    for m in M:
        s5=G[m]["S5_neutral_minus_base"]; s3=G[m]["S3_penlow_minus_penhigh"]; p1=P[m]["D1_rew_minus_pen"]; p2=P[m]["D2_ctrl_minus_pen"]
        f.write(f"| {LAB[m]} | {s3['est']*100:+.2f} | {s5['est']*100:+.2f} [{s5['ci95'][0]*100:+.2f}, {s5['ci95'][1]*100:+.2f}] | {p1['est']*100:+.2f} [{p1['ci95'][0]*100:+.2f}, {p1['ci95'][1]*100:+.2f}] | {p2['est']*100:+.2f} | {S[m]['S8_C7_minus_C3']*100:+.1f} |\n")
print(open("paper/tables/table2_primary.md").read()); print(open("paper/tables/table3_secondary.md").read()); print(open("paper/tables/table1_accuracy.md").read())
