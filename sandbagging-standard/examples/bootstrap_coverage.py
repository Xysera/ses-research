"""Simulation check of two-way percentile-bootstrap coverage with 10 or 20 templates.

This is a diagnostic for the paper, not a calibration of SES thresholds. The data
generating process is a matched binary-outcome model with crossed item/template
random effects. Coverage is therefore scenario-dependent.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.special import expit

HERE = Path(__file__).resolve().parent
SEED = 20021025
N_REP = 200
N_BOOT = 1_000
N_ITEMS = 250


def target_effect(mu, delta_logit, item_sd, template_sd, rng):
    u = rng.normal(0, item_sd, 2_000_000)
    v = rng.normal(0, template_sd, 2_000_000)
    eta = mu + u + v
    return float(np.mean(expit(eta) - expit(eta - delta_logit)))


def run_case(n_templates, template_sd, delta_logit, seed):
    rng = np.random.default_rng(seed)
    # Study 1 cells were approximately 94-99% accurate.  mu=3.5 produces
    # marginal control accuracy near 95% under these random-effect settings.
    mu, item_sd = 3.5, 0.9
    truth = target_effect(mu, delta_logit, item_sd, template_sd, rng)
    covered = 0
    widths = []
    estimates = []
    control_means = []
    for _ in range(N_REP):
        item = rng.normal(0, item_sd, (N_ITEMS, 1))
        template = rng.normal(0, template_sd, (1, n_templates))
        eta = mu + item + template
        control = rng.binomial(1, expit(eta))
        penalty = rng.binomial(1, expit(eta - delta_logit))
        diff = control - penalty
        obs = float(diff.mean())
        ii = rng.integers(0, N_ITEMS, (N_BOOT, N_ITEMS))
        kk = rng.integers(0, n_templates, (N_BOOT, n_templates))
        draws = diff[ii[:, :, None], kk[:, None, :]].mean(axis=(1, 2))
        lo, hi = np.percentile(draws, [2.5, 97.5])
        covered += int(lo <= truth <= hi)
        widths.append(float(hi - lo))
        estimates.append(obs)
        control_means.append(float(control.mean()))
    p = covered / N_REP
    mcse = float(np.sqrt(p * (1 - p) / N_REP))
    return {
        "n_items": N_ITEMS,
        "n_templates": n_templates,
        "template_logit_sd": template_sd,
        "true_marginal_effect": truth,
        "mean_control_accuracy": float(np.mean(control_means)),
        "replications": N_REP,
        "bootstrap_draws": N_BOOT,
        "coverage": p,
        "coverage_mcse": mcse,
        "mean_ci_width": float(np.mean(widths)),
        "mean_estimate": float(np.mean(estimates)),
    }


def main():
    cases = []
    j = 0
    for n_templates in (10, 20):
        for template_sd in (0.2, 0.6):
            cases.append(run_case(n_templates, template_sd, 0.60, SEED + j))
            j += 1
    out = {
        "design": "matched binary outcomes near 95% control accuracy with crossed logistic-normal item and template effects",
        "warning": "scenario check, not a distribution-free guarantee",
        "cases": cases,
    }
    path = HERE / "bootstrap_coverage_results.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    for case in cases:
        print(case)
    print(path)


if __name__ == "__main__":
    main()
