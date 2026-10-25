"""Additional analyses requested in internal review of the SES synthesis paper.

Produces Study 1 contrast intervals and paired Screen 2 intervals without changing
the frozen SES v0.5 decision rules.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "impl"))
from ses import Config, contrast  # noqa: E402
from run_study1_lib import MODELS, ROLE, conv  # noqa: E402

DISPLAY = {
    "qwen25_7b": "Qwen2.5-7B-Instruct",
    "llama31_8b": "Llama-3.1-8B-Instruct",
    "phi35_mini": "Phi-3.5-mini-instruct",
    "qwen3_4b": "Qwen3-4B",
    "gemma3_4b": "Gemma-3-4B-it",
}


def study1():
    cfg = Config(n_boot=10_000, seed=20021022)
    rows = []
    for model in MODELS:
        raw = pd.DataFrame(map(json.loads, open(ROOT / "results" / f"confirm_{model}.jsonl")))
        df = conv(raw, ROLE)
        values = {
            "raw_drop": contrast(df, "baseline", "penalty", cfg),
            "generic_note": contrast(df, "baseline", "neutral", cfg),
            "D1": contrast(df, "reward", "penalty", cfg),
            "D2": contrast(df, ["neutral", "third_party"], "penalty", cfg),
        }
        row = {"model": DISPLAY[model]}
        row["accuracy_by_condition"] = {
            role: float(df.loc[df.role == role, "correct"].mean())
            for role in ("baseline", "penalty", "reward", "neutral", "third_party", "mirror")
        }
        for name, result in values.items():
            row[name] = result
        rows.append(row)
    # Holm adjustment is performed separately within each preregistered
    # estimand family (five models for D1; five models for D2).
    for estimand in ("D1", "D2"):
        order = sorted(range(len(rows)), key=lambda i: rows[i][estimand]["p_one"])
        running = 0.0
        adjusted = [0.0] * len(rows)
        for rank, i in enumerate(order):
            candidate = min(1.0, (len(rows) - rank) * rows[i][estimand]["p_one"])
            running = max(running, candidate)
            adjusted[i] = running
        for i, value in enumerate(adjusted):
            rows[i][estimand]["p_holm"] = value
    return rows


def screen2():
    df = pd.read_csv(HERE / "screen2_summary.csv")
    rng = np.random.default_rng(20021024)
    rows = []
    for model in sorted(df.model.unique()):
        for emph in ("E1", "E3"):
            a = df[(df.model == model) & (df.cond == "penalty") & (df.emph == emph)].set_index("p").score
            b = df[(df.model == model) & (df.cond == "neutral") & (df.emph == emph)].set_index("p").score
            ids = sorted(set(a.index) & set(b.index))
            diff = (a.loc[ids] - b.loc[ids]).to_numpy(float)
            draws = np.empty(10_000)
            for j in range(len(draws)):
                ii = rng.integers(0, len(diff), len(diff))
                draws[j] = diff[ii].mean()
            rows.append({
                "model": model,
                "emphasis": emph,
                "n_prompts_per_condition": len(ids),
                "n_answers_per_condition": len(ids) * 10,
                "penalty_minus_neutral": float(diff.mean()),
                "ci95": [float(x) for x in np.percentile(draws, [2.5, 97.5])],
            })
    return rows


def main():
    out = {"study1": study1(), "screen2": screen2()}
    path = HERE / "revision_analysis_results.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    for row in out["study1"]:
        print(row["model"], {k: round(row[k]["est"] * 100, 2) for k in ("raw_drop", "generic_note", "D1", "D2")})
    for row in out["screen2"]:
        print(row)
    print(path)


if __name__ == "__main__":
    main()
