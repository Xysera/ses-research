"""Build the item pool (deterministic, seed 2002). Output: data/pool.jsonl"""
import json, random
from datasets import load_dataset
rng = random.Random(2002)
pool = []
m = load_dataset("cais/mmlu", "all", split="test")
idx = rng.sample(range(len(m)), 400)
for i in idx:
    r = m[i]
    if len(r["choices"]) == 4 and len(r["question"]) < 700:
        pool.append(dict(src="mmlu", id=f"mmlu_{i}", q=r["question"], choices=r["choices"], ans=int(r["answer"])))
mm = [p for p in pool][:300]; pool = mm
a = load_dataset("allenai/ai2_arc", "ARC-Easy", split="test")
cand = [r for r in a if len(r["choices"]["text"]) == 4 and r["answerKey"] in "ABCD"]
for r in rng.sample(cand, 300):
    pool.append(dict(src="arc", id="arc_" + r["id"], q=r["question"], choices=r["choices"]["text"],
                     ans="ABCD".index(r["answerKey"])))
n = 0
while n < 300:
    t = n % 3
    if t == 0: x, y = rng.randint(12, 99), rng.randint(12, 99); q, v = f"What is {x} × {y}?", x * y
    elif t == 1: x, y = rng.randint(100, 999), rng.randint(100, 999); q, v = f"What is {x} + {y}?", x + y
    else: x, y = rng.randint(200, 999), rng.randint(11, 99); q, v = f"What is {x} − {y}?", x - y
    ds = set()
    while len(ds) < 3:
        d = v + rng.choice([-1, 1]) * rng.choice([1, 2, 10, 20, 100, 9, 11])
        if d != v and d > 0: ds.add(d)
    ch = [v] + sorted(ds); ch = [str(c) for c in ch]
    order = list(range(4)); rng.shuffle(order)
    pool.append(dict(src="arith", id=f"arith_{n}", q=q, choices=[ch[o] for o in order], ans=order.index(0)))
    n += 1
with open("../data/pool.jsonl", "w") as f:
    for p in pool: f.write(json.dumps(p) + "\n")
print(len(pool), {s: sum(p["src"] == s for p in pool) for s in ("mmlu", "arc", "arith")})
