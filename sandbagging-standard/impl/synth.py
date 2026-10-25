"""Synthetic trial-log generator with known ground truth, for testing the SES implementation."""
import numpy as np, pandas as pd
ROLES = ["baseline", "penalty", "mirror", "third_party", "neutral", "reward", "effort_control"]
NOTE_ROLES = ROLES[1:]

def simulate(scenario, n_items=150, n_templates=20, seed=0, generic=0.03, strategic=0.12, with_effort=True, with_domains=True):
    rng = np.random.default_rng(seed)
    fragile = rng.random(n_items) < 0.15
    domain = np.where(rng.random(n_items) < 0.5, "target", "control")
    base_p = np.where(fragile, 0.75, 0.99)
    rows = []
    roles = ROLES if with_effort else [r for r in ROLES if r != "effort_control"]
    for i in range(n_items):
        for t in range(n_templates):
            correct_letter = "ABCD"[rng.integers(0, 4)]
            base_ok = rng.random() < base_p[i]            # latent baseline knowledge on this cell
            u = rng.random(); u2 = rng.random()
            for role in roles:
                ok = base_ok
                if role in NOTE_ROLES and scenario != "none":
                    # generic note cost falls on fragile items (and a little on others)
                    if ok and u < (generic / 0.15 * 0.8 if fragile[i] else generic * 0.2): ok = False
                strategic_hit = scenario in ("consequence", "instructed") and role in ("penalty", "effort_control") \
                                and (domain[i] == "target" if with_domains else True) and u2 < strategic * (2 if with_domains else 1)
                if strategic_hit: ok = False
                if scenario == "positional" and role == "penalty" and rng.random() < 0.40: ok = False; forced = "A"
                else: forced = None
                if ok: resp = correct_letter
                else:
                    wrong = [c for c in "ABCD" if c != correct_letter]
                    resp = forced if (forced and forced != correct_letter) else wrong[rng.integers(0, 3)]
                    if forced and forced == correct_letter: ok, resp = True, correct_letter
                rows.append(dict(item_id=i, template=t, role=role, correct=int(resp == correct_letter), response_letter=resp,
                                 correct_letter=correct_letter, severity=t % 3, source="s1" if i % 2 else "s2", domain=domain[i]))
    return pd.DataFrame(rows)
