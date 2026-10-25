import sys, time, json
from lib import *
name = sys.argv[1]
pool = [json.loads(l) for l in open(f"{ROOT}/data/pool.jsonl")]
with Server(name) as s:
    t = time.time(); n = 0; ok = 0
    for it in pool[::90]:
        for cond in ("C0_baseline", "C1_pen_high"):
            msgs, a, sev = build_messages(it, cond, 3, perm_for(it["id"], 3), 7)
            text, lps = s.ask(msgs); r = score(text, lps, a); n += 1; ok += r["gen_correct"]
            if n <= 3: print(repr(text), lps, a, r)
    print(name, n, "calls", round((time.time() - t) / n, 2), "s/call", ok, "correct")
