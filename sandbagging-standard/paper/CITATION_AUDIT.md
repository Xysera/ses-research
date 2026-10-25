# Citation and claim audit

**Status:** publication audit refreshed 24 October 2026 for preprint release candidate v1.0-rc1.

## Scope

Every quantitative claim in `PAPER_DRAFT.md` was traced either to a source marked FULL/PARTIAL in `sources/LEDGER.md` or to a project result artifact. Bibliographic titles, author lists, arXiv identifiers and version dates for the cited arXiv papers were checked against the arXiv API. The ICML 2026 metadata for the weak-supervision and C3 papers was checked against PMLR volume 306. The primary records for van der Weij et al. (arXiv:2406.07358), Meinke et al. (arXiv:2412.04984), Taylor et al. (arXiv:2512.07810), and Yulong et al. (PMLR 306:152533-152571) were rechecked on 24 October 2026.

## Corrections made

1. Replaced the categorical novelty statement “we found no single document” with the search-bounded statement “our search did not identify”.
2. Replaced “spontaneous, consequence-dependent sandbagging” with “consequence-dependent underperformance without an explicit instruction”. The evaluated models were placed in constructed scenarios, so “spontaneous” was too broad.
3. Replaced “no spontaneous positive case exists in our data” with the operationally precise “no positive case without an explicit underperformance instruction exists in our data”.
4. Separated two distinct Cacioli papers that had been combined under one reference.
5. Completed the Boxo, Neelappa and Raval author list.

## Evidence boundaries retained

- S15 (Anthropic system cards) remains unverified and supports no manuscript claim.
- The inaccessible OpenAI blog post supports no manuscript claim; claims about the anti-scheming experiments rely on arXiv:2509.15541.
- Sources read only at abstract level support no quantitative manuscript claim.
- Screen 2 is explicitly exploratory and underpowered for small effects.
- SES levels describe strength of behavioural evidence and never establish intent, consciousness, self-preservation or deception.

## Remaining external check

An independent human reviewer should spot-check the central quantitative extractions from Meinke et al. Appendix B.6, Schoen et al. Appendix M.1, and Yulong et al. before a venue submission. This has not occurred and is disclosed in the manuscript; it is recommended quality control for a preprint and required before claiming independent validation.
