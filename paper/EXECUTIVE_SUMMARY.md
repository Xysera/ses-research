# Executive summary: Research Initiative 002

**Result: negative (equivalence).** No consequence-sensitive accuracy was detected in any of five small open-weight models.

- **Trials:** 166,250 (5 models x 33,250), all complete, audited, no duplicates, no-letter rate <= 0.08%.
- **Time:** about a day of wall-clock including setup (estimate; about 11 h unattended local inference for three models, about 1.3 h on cloud GPUs for two).
- **Spend:** about USD 1 on Hugging Face Jobs T4 GPUs (estimated from job runtimes; billing not verified). No API spend.
- **Per-model D1 (reward - penalty) / D2 (controls - penalty), percentage points:** Qwen2.5-7B +0.26 / +0.10; Llama-3.1-8B -0.08 / +0.12; Phi-3.5-mini +0.08 / +0.15; Qwen3-4B +0.16 / +0.08; Gemma-3-4B -0.12 / -0.22. Pooled +0.08 [-0.41, +0.57] and +0.05 [-0.38, +0.48].
- **Verdicts:** all five models "equivalent within 3 pp". None "supported", none "inconclusive". No model's D1 or D2 was significant.
- **Unexpected finding:** any note, even a neutral one, cost 2.1-4.5 points of accuracy (pooled -3.2). A baseline-only comparison would have shown 2.2-4.7 points of apparent capability suppression, fully reproduced by a neutral note. This is a confound in our data; it says nothing about any published study.
- **Sensitivity check:** an explicit "answer wrongly" directive lowered accuracy in four models (-3.9 to -19.7 pp) but not Llama-3.1-8B; so the harness can detect drops, except it gives no information for Llama.

**Limitations that matter:** small quantised models; one question per prompt (no running score); known-item selection; no chain of thought; authored templates; two models ran on a different GPU backend than three (checked: 98-99% identical answers, no within-model confound); the +-3 pp margin was fixed after the pilot. A null here says nothing about frontier models, agentic settings or optimised prompts.

**Merits publication?** As an honest preregistered negative result and a methods note (matched neutral/third-party controls, equivalence testing, generic note cost): yes, as an arXiv technical report or safety/evaluation workshop paper. Not strong enough for a main venue on its own; the natural extension is multi-question or agentic formats and larger models, which would need compute beyond this budget.

**Where:** manuscript `paper/manuscript.md` (also `.html`), figures `paper/figures/`, tables `paper/tables/`, reproduction `REPRODUCE.md`, preregistration `prereg/`.
