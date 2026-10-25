# Submission metadata

## Title

Toward an Evidence Standard for Sandbagging Claims: A Literature Synthesis, Reference Implementation and Worked Application

## Release status

Preprint release candidate v1.0-rc1, dated 25 October 2026. Not peer reviewed. Frozen decision rules: SES v0.5.

## Author/byline

Torin Ethreidge — Lead Researcher and Senior Researcher, Xysera Research

## Contributions

Torin Ethreidge: conceptualization, methodology, investigation, software, formal analysis, data curation, visualization, writing—original draft, writing—review and editing, project administration, and research leadership. An AI research agent assisted with literature screening, implementation, analysis and drafting under the named author's direction; this assistance is disclosed in the manuscript and does not receive authorship.

## Repository

Public URL: `https://github.com/Xysera/ses-research` (verified live on 25 October 2026).

## Licensing

- Original software: Apache License 2.0.
- Manuscript, original documentation, original figures, and original research data: CC BY 4.0.
- Third-party benchmark content, external logs, model artifacts, papers, and sourced materials: original upstream terms; not relicensed.

## Abstract

“Sandbagging,” strategic underperformance on an evaluation, matters because capability evaluations inform deployment and governance decisions. We synthesise 43 screened records into a proposed Sandbagging Evidence Standard with five cumulative claim levels and explicit operational criteria. A reference implementation computes matched-cell criteria from trial-level logs and returns an indeterminate outcome when neither equivalence nor underperformance is established. We exercise it with 14 synthetic tests, a worked application to 166,250 preregistered trials, held-out but incomplete released organism cases, and a nonconfirmatory screen. In Study 1, matched neutral notes reproduce almost all penalty-note degradation: three models receive L1-ctx and two are indeterminate; none supports consequence-sensitive underperformance. Cedar supports a descriptive held-out capability gap; Oak is statistically indeterminate. The standard is an auditable proposal, not a validated detector, and never establishes intent.

## Keywords

AI safety; language models; sandbagging; strategic underperformance; capability evaluation; evaluation integrity; evaluation awareness; capability elicitation

## Suggested subject areas

- Artificial Intelligence (cs.AI)
- Computation and Language (cs.CL)
- Machine Learning (cs.LG), if a secondary category is appropriate

## Public-facing summary

This paper proposes a reproducible standard for grading evidence of language-model sandbagging. Its worked application shows why ordinary prompt-context effects must be ruled out before an accuracy drop is attributed to consequences or strategic underperformance.

## Upload set

1. `xysera-ses-v1.0-rc1-paper.pdf`
2. `xysera-ses-v1.0-rc1-source.tar.gz`
3. `xysera-ses-v1.0-rc1-data.tar.gz`
4. `DATA_MANIFEST_v1.0-rc1.txt`
5. `RELEASE_SHA256SUMS_v1.0-rc1.txt`

Before upload, complete the unchecked publisher actions in `PUBLICATION_CHECKLIST.md`.
