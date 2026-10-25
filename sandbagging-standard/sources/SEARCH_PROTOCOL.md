# Search protocol and log (v0.2, 2026-10-23)

## Aim
Identify published or preprinted work (to 2026-10-22) that defines, induces, detects, explains or critiques sandbagging (strategic underperformance on evaluations) or that supplies methods directly usable for the standard.

## Sources and how they were queried
1. **arXiv API** (`export.arxiv.org`), exhaustive enumeration of listed matches (this is the systematic component):
   - `abs:sandbagging` -> 41 results (40 retrieved; 1 beyond the retrieved window).
   - `abs:"strategic underperformance" OR abs:"capability concealment" OR abs:"underperform on evaluations"` -> 11 results (all retrieved).
   - `abs:"evaluation awareness"` -> 55 results (now fully paged: offsets 0 and 30).
   - `abs:sandbagging` re-paged at offset 30: all 41 results now seen.
   - Added in pass 2: `abs:"password-locked" OR abs:"password locked" OR abs:"under-elicitation" OR abs:"underelicitation" OR abs:"capability elicitation"` -> 32 (all seen); `abs:underperform AND abs:evaluation AND (abs:"language model" OR abs:LLM)` -> 473 results, only the 39 newest seen (mostly off-topic; query too broad, not used for inclusion); `abs:"hidden capabilities" OR "conceal capabilities" OR "concealing capabilities" OR "capability hiding"` -> 19 (all seen).
2. **General web search** (WebSearch tool, mixed standard/extended mode, top ~10 results each), 17 queries: sandbagging evaluations; detection (black-box); CoT monitoring; capability elicitation/hidden capabilities; evaluation gaming/situational awareness; sabotage/agentic sandbagging; mechanistic/steering; safety cases/policy; password-locking; Anthropic system cards; survival bandit; linear probes; frameworks/criteria/taxonomy; consequence-sensitive sandbagging; cause of sandbagging; stress testing deliberative alignment; position paper/definition.
3. **Citation chasing** from the reference lists of S1, S5, S6, S8 (partial).

## Screening
- **Include if:** sandbagging (or strategic underperformance on evaluations) is a topic of the work, or it supplies a detection, elicitation, artifact-control or evidence-standard method directly relevant to it.
- **Exclude:** off-topic keyword matches (e.g. geophysics, robotics, imaging) and works where sandbagging is a passing mention (listed as seen, not read).
- Reading depth is recorded per source in `LEDGER.md` (FULL / PARTIAL / ABSTRACT / LISTING ONLY / SEARCH).

## Known limits (this is not a PRISMA-grade review)
- Only arXiv was enumerated systematically. No Google Scholar, ACL Anthology, OpenReview, Semantic Scholar, or LessWrong/Alignment Forum crawl; blog and forum posts appear only via web search and are marked secondary.
- arXiv API results were truncated by the reading tool at about 40 entries per page; paging closed the gap for the sandbagging, evaluation-awareness, password-locked/elicitation and hidden-capability queries. The broad `underperform AND evaluation` query (473 results) was not exhausted.
- A single reviewer (the AI research agent) screened and extracted; no second independent pass. Reading depth varies; many 2026 papers were read at abstract level only.
- Venue and publication status come from search snippets or arXiv comments and are not independently verified.
- The 2026 arXiv identifiers and dates were taken from the retrieved listing.

## Pass 2 outcome (2026-10-23)
Full text on disk and read for: S2, S3, S6, S17, S24 (and van der Weij S1 PDF available). New abstract-level sources S36-S42. Corrected a claim in the Study 1 manuscript about prior consequence controls (S3 App. M.1, S2 B.6.1).

## Next screening pass (still to do)
Paginate arXiv queries; add `abs:"password-locked"`, `abs:"under-elicitation"`, `abs:"capability elicitation"`, `abs:"underperformance" AND abs:"evaluation"`, `abs:"scheming"`; read the S35 candidates; read S18, S24 and S22 beyond abstracts; obtain the Anthropic and OpenAI primary system-card sections.
