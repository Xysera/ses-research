"""Per model: items answered correctly (generated answer) under all 4 option rotations at baseline = 'known'.
Split known items into disjoint PILOT (60) and CONFIRM (150) sets, stratified by source, seed 2002."""
import json, random, sys, collections
from lib import *
for name in MODELS:
    try: rows = [json.loads(l) for l in open(f"{ROOT}/data/screen_{name}.jsonl")]
    except FileNotFoundError: continue
    by = collections.defaultdict(list)
    for r in rows: by[r["id"]].append(r)
    known = [i for i, rs in by.items() if len(rs) == 4 and all(r["gen_correct"] for r in rs)]
    src = {r["id"]: r["src"] for r in rows}
    allacc = sum(r["gen_correct"] for r in rows) / len(rows)
    pools = {s: sorted(i for i in known if src[i] == s) for s in ("mmlu", "arc", "arith")}
    rng = random.Random(f"{name}-select")
    for s in pools: rng.shuffle(pools[s])
    pilot, conf = [], []
    for s in pools:
        pilot += pools[s][:20]; conf += pools[s][20:90]
    # top up confirm set from leftovers if a source is short
    left = [i for s in pools for i in pools[s][90:]]; rng.shuffle(left)
    while len(conf) < 250 and left: conf.append(left.pop())
    json.dump(dict(model=name, n_known=len(known), screen_acc=allacc, per_src={s: len(v) for s, v in pools.items()},
                   pilot=pilot, confirm=conf[:250]), open(f"{ROOT}/data/items_{name}.json", "w"))
    print(name, "screen_acc", round(allacc, 3), "known", len(known), {s: len(v) for s, v in pools.items()}, "pilot", len(pilot), "confirm", len(conf[:250]))
