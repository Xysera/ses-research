# SES v1.0-rc1 preprint publication checklist

Status date: 25 October 2026. “Complete” means completed within the repository; it does not imply peer review or community validation.

## P0 — required before publication

- [x] **1. Reproduce reported results.** Raw hashes verified; five complete logs contain 33,250 trials each (166,250 total); audit, primary and secondary outputs regenerate to the recorded hashes; manuscript values are checked by `impl/release_audit.py`.
- [x] **2. Audit implementation against specification.** Criteria, gates, induced-case cap and failed/not-assessed behavior reconciled; 14 tests pass.
- [x] **3. Resolve L0/L1 logic.** L0 requires TOST equivalence; L1 requires demonstrated underperformance; unresolved cases return `indeterminate`.
- [x] **4. Bound L4.** Defined as behavior consistent with strategic sandbagging, never proof of intent, deception or awareness; recovery, selectivity and independent corroboration are justified.
- [x] **5. Verify central literature claims.** Quantitative claims are limited to FULL/PARTIAL sources in the ledger; central arXiv/PMLR records and metadata were rechecked. See `paper/CITATION_AUDIT.md`.
- [x] **6. Finalize local reproducibility package.** Rules, ledger, implementation, tests, scripts, dependency pins, hashes and commands are included; data-access requirements are documented.
- [x] **7. Publish Study 1 preregistration.** Repository path and recorded SHA-256 digest are linked in the manuscript; a DOI may be added in a later archival release.
- [x] **8. Label empirical applications.** Study 1 is threshold-informing; Cedar/Oak are held-out but incomplete; Screen 2 is nonconfirmatory.

## P1 — scientific quality

- [x] **9. Define estimands.** Baseline, neutral, D1, D2, mirror, recovery and selectivity are formally defined in Section 5.
- [x] **10. Explain decision procedure.** Bootstrap, directional tests, Holm families, TOST, sequential gates and borderline outcomes are specified.
- [x] **11. Justify provisional thresholds.** Empirical versus judgment-based defaults and required sensitivity analyses are separated in the standard.
- [x] **12. Discuss construct validity.** False negatives and nonstrategic false positives are explicit.
- [x] **13. Expand tests.** Missing data, invalid outputs, zero variance, insufficient templates, ambiguous evidence and failed/unassessed distinctions are covered.
- [x] **14. Verify bootstrap methodology.** Coverage near the Study 1 regime and template heterogeneity is reported; conservative coverage and lower TOST power are disclosed. Broader calibration remains future validation, not a release claim.
- [x] **15. Add generalization limits.** Demonstrated multiple-choice results are separated from proposed free-form/agentic adaptations.
- [x] **16. Emphasize the negative Study 1 result.** It is central in the abstract, results, figure and discussion.
- [x] **17. Add compact application example.** Llama-3.1-8B is traced from raw contrasts through criteria to L1-ctx, with Qwen2.5 contrasting the indeterminate branch.
- [ ] **18. Independent second-pass extraction. OPEN QUALITY ITEM.** A blinded protocol exists in `review/BLINDED_ADVERSARIAL_TEST_PROTOCOL.md`; no independent human has executed it. This must remain disclosed and is required before claiming independent validation.

## P2 — presentation and release polish

- [x] **19. Keep evidence ladder together.** PDF builder groups each figure with its caption.
- [x] **20. Reformat appendix tables.** Repeating headers, fixed widths and compact type are used; final PDF is visually inspected.
- [x] **21. Standardize names and notation.** Model names, pp units, intervals, criterion IDs and rule/manuscript versions are reconciled.
- [x] **22. Improve abstract.** Framework, negative Study 1 result, held-out application and validation limits are separated.
- [x] **23. State contributions.** Ledger, standard, implementation and empirical demonstrations are distinguished.
- [x] **24. Finalize citation audit.** In-text/bibliography consistency and stable arXiv/PMLR identifiers are checked. Project links await item 7.
- [ ] **25. Complete release metadata. PARTIAL.** Author/byline, contributions and public repository are recorded. License selection and any assigned DOI/preprint identifier remain pending.
- [x] **26. PDF quality check.** Fonts, figures, pagination, tables, notation and source/PDF consistency checked for v1.0-rc1.

## Publisher handoff

1. Select licenses (suggested: CC BY 4.0 for paper/docs/data and Apache-2.0 or MIT for code).
2. Add any assigned DOI/preprint identifier.
3. Upload the PDF, source archive, data archive, manifest and checksums as one versioned release.
