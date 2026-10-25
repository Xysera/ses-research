"""Screening pass: baseline (no note), 4 cyclic option rotations, all pool items. Used ONLY to select 'known' items."""
import json, os, sys
from lib import *
pool = [json.loads(l) for l in open(f"{ROOT}/data/pool.jsonl")]
for name in sys.argv[1:]:
    out = f"{ROOT}/data/screen_{name}.jsonl"
    done = set()
    if os.path.exists(out):
        done = {(d["id"], d["rot"]) for d in map(json.loads, open(out))}
    with Server(name) as s, open(out, "a") as f:
        for it in pool:
            for rot in range(4):
                if (it["id"], rot) in done: continue
                perm = [(i + rot) % 4 for i in range(4)]
                msgs, a, _ = build_messages(it, "C0_baseline", 0, perm, 10)
                text, lps = s.ask(msgs)
                f.write(json.dumps(dict(id=it["id"], src=it["src"], rot=rot, **score(text, lps, a))) + "\n"); f.flush()
    print("done", name, flush=True)
