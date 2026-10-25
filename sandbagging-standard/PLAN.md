# Sandbagging Evidence Standard: plan (no new experiments required)

Goal: a versioned, testable, reproducible document that says what evidence is needed before underperformance is called sandbagging, with an operational test for each criterion and a reference implementation.

1. **Source ledger** (`sources/LEDGER.md`): every paper used, what was read (full text / abstract / secondary summary), what it operationally measures, thresholds, stated limitations. Claims from unread text are marked UNVERIFIED and not used as normative evidence.
2. **Criteria** (`criteria/STANDARD.md`): tiers (necessary behavioural / artifact exclusions / corroborating / verdict rules), each with: definition, operational test, inputs required, what a pass/fail means, known failure modes, source(s).
3. **Reference implementation** (`impl/`): a script that reads a standard evaluation-log schema and computes each criterion that the data allow, with unit tests.
4. **Worked examples** (`examples/`): Study 1 data run through the implementation (induced case C7, null case, generic note cost confound, positional-artifact case). No new model runs.
5. **Reproducibility**: schema, version number, changelog, test suite, hashes, citation file.

Honest limits to state: no positive case without an explicit underperformance instruction is available locally, so worked evaluation covers induced cases, nulls and artifacts only; the ledger is a literature synthesis up to the stated cutoff, not exhaustive.
