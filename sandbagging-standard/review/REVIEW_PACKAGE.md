# Review package: Sandbagging Evidence Standard (SES) v0.5 (release candidate)

**For:** researchers working on evaluation integrity, sandbagging, scheming or capability elicitation.
**From:** Xysera Research. **Status:** draft for critique, not peer reviewed, not for citation.

## What we are asking
We have written a proposed standard for how strongly an evaluation result may be described as sandbagging, with an operational test per criterion, a reference implementation and worked evaluations that needed no new model runs. We would like you to try to break it. Short, blunt comments are the most useful.

## What is in the package
- `paper/PAPER_DRAFT.md`: the synthesis paper (read this first, ~10 pages).
- `criteria/STANDARD.md`: the standard itself (claim levels L0-L4, criteria K/A/C/S/R/E/I/W, decision table, reporting checklist).
- `sources/LEDGER.md` and `sources/SEARCH_PROTOCOL.md`: sources, reading depth, search method and its limits.
- `impl/` (`ses.py`, `synth.py`, `test_ses.py`) and `examples/` (worked example on 166,250 trials from a preregistered study of five small open-weight models; sensitivity report).
- `CHANGELOG.md`: every rule changed after looking at example data is listed there.

## Five claims we want challenged
1. **Levels and ordering.** Is the ladder L0 (no underperformance) to L4 (behaviour consistent with strategic sandbagging) sensible? Should the instruction-inference control (C4) be required for L3, or only recommended?
2. **Necessary vs corroborating.** We treat mirror condition, matched controls and artifact exclusions as necessary and probes, reasoning, calibration and consistency as corroborating. Is that split defensible given current evidence?
3. **Defaults.** Equivalence margin ±3 points, minimum effect 2 points, at least 100 items and 10 templates, no-answer rate ≤1%, letter-distribution tolerance (p<0.01 and JS≥0.05). Are these reasonable? Which would you change and why? (The last two are provisional conventions set while looking at example data.)
4. **Capability vs propensity.** Induced cases stop at "capability demonstrated". Is that too conservative, or not conservative enough?
5. **No claims about intent.** We refuse to assign intent from behaviour at any level. Should a standard allow any route to such a claim?

## Specific questions
- Which published studies or logs would be the best test of L3/L4 on real spontaneous behaviour? Are transcripts or trial-level logs available to external groups?
- Which sources are we missing? The search is systematic only for arXiv; Anthropic system cards and an OpenAI scheming blog post could not be retrieved by our tools.
- Are the matched controls (neutral note, third-party penalty, mirror) and the "generic context effect" label (L1-ctx) usable for agentic or open-ended tasks? What would you replace them with?
- Could the standard be gamed by a developer who designs a model or an evaluation to pass the checks? What would a sophisticated model do to defeat them?
- Are there criteria that you think give false comfort (for example a preserved difficulty-accuracy correlation, which a preregistered study found can coexist with positional shortcuts)?

## Known weaknesses (please do not rediscover these for us)
Exercised only on simulated cases, a null and artifact set, and instructed cases; no positive case without an explicit underperformance instruction exists in our data, and an exploratory screen of three open reasoning models (324 prompts, `examples/SCREEN2_REPORT.md`) found none. A single AI agent screened and extracted the literature with no second pass. Several 2026 papers were read at abstract level only. The sensitivity analysis reuses data that informed some thresholds. 300 bootstrap draws were used in sensitivity runs.

## How to reproduce
`REPRODUCE.md` in this package. Tests: `.venv/bin/python impl/test_ses.py` (14 tests); release gate: `.venv/bin/python impl/release_audit.py`. The worked example needs the separately distributed Study 1 trial logs.

## How to reply
Annotated copies of the standard or a list of numbered comments are both fine. We will log every substantive change in `CHANGELOG.md` with your reason and credit you if you wish.
