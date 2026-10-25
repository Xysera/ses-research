# Source ledger (v0.4, 2026-10-23)

Read status: **FULL** = body text retrieved (long documents may be truncated; coverage noted); **ABSTRACT** = abstract page only; **SEARCH** = search-result summary only (UNVERIFIED, not used as normative evidence).
Quantities below are as retrieved by the reading tool and should be re-checked against the PDF before being quoted in a publication. Internal inconsistencies noticed in a paper are listed.

| ID | Source | Read | Coverage |
|---|---|---|---|
| S1 | van der Weij et al., *AI Sandbagging: Language Models can Strategically Underperform on Evaluations*, ICLR 2025, arXiv:2406.07358 | FULL (HTML v4) | first 100k of 137k chars |
| S2 | Meinke et al., *Frontier Models are Capable of In-context Scheming*, arXiv:2412.04984 | FULL TEXT on disk (PDF, 72 pp); sandbagging section, Table 6 and Appendix B.6 read | |
| S3 | OpenAI & Apollo, *Stress Testing Deliberative Alignment for Anti-Scheming Training*, arXiv:2509.15541 | FULL TEXT on disk (PDF, 96 pp); Appendix M.1 read | |
| S4 | Greenblatt et al., *Stress-Testing Capability Elicitation With Password-Locked Models*, arXiv:2405.19550 | ABSTRACT | |
| S5 | Hofstätter et al., *The Elicitation Game*, arXiv:2502.02180 (v3) | FULL | 100k of 101k chars |
| S6 | Taylor et al., *Auditing Games for Sandbagging*, arXiv:2512.07810 | FULL TEXT on disk (PDF, 77 pp); definition, thresholds and game structure verified against it; results tables from the HTML read | verified: sandbagger criterion (>=10 pp password uplift, McNemar p<0.05, 100 samples); "Removing sandbagging is not the same as detecting it" |
| S7 | Tice et al., *Noise Injection Reveals Hidden Capabilities of Sandbagging Language Models*, NeurIPS 2025, arXiv:2412.01784 (v3) | FULL | 100k of 131k chars |
| S8 | Li, Phuong, Siegel, *LLMs Can Covertly Sandbag ... Against CoT Monitoring*, arXiv:2508.00943 (v2) | FULL | |
| S9 | Dyer et al., *Sandbagging in a Simple Survival Bandit Problem*, arXiv:2509.26239 | FULL | |
| S10 | *Linear probes rely on textual evidence*, arXiv:2509.21344 (v2) (authors not retrieved) | FULL | first 100k of 125k chars |
| S11 | Cacioli, *Option-Order Randomisation ... Prompted Sandbagging*, arXiv:2604.26206 | FULL | |
| S12 | Cacioli, *Below-Chance Blindness*, arXiv:2604.25249 | FULL | |
| S13 | Chaudhary, *In-Context Environments Induce Evaluation-Awareness in Language Models*, arXiv:2603.03824 | FULL | first 100k of 104k chars |
| S14 | Knecht, Florin, Hagendorff, *Evaluation Awareness in Language Models Has Limited Effect on Behaviour*, arXiv:2605.05835 | FULL | |
| S15 | Anthropic system cards (Claude 4, Sonnet 4.5, Opus 4.5) | SEARCH | UNVERIFIED |
| S16 | "Systematic sandbagging evaluations on Claude 3.5 Sonnet" (LessWrong, unreviewed) | FULL (post) | secondary source |

## Per-source entries (operational content only)

### S1 van der Weij et al.
- **Definition:** sandbagging = strategic underperformance on an evaluation; components: strategic, underperformance, evaluation. Developer vs AI-system sandbagging. Accidental underperformance (e.g. contamination) excluded. Underperformance is relative to *actual capability* = best performance under the best available elicitation.
- **Induction:** prompting (GPT-4, Claude 3 Opus told to answer WMDP incorrectly) and password-locked fine-tuning (Mistral 7B, LoRA).
- **Signals:** selectivity (WMDP down, MMLU/CSQA near baseline); calibration to target accuracy (models overshoot); emulation of a weaker model (Llama 3 70B locked to mimic Llama 2 7B: 77.1% answer match vs 60.8% for accuracy-only matching); naive sandbagging detectable by failing easy while passing hard.
- **Limits stated:** multiple-choice only; open-weight fine-tuning; password-locking may not match real onset; limited prompt effort; tests *can*, not *would*.

### S2 Meinke et al. (sandbagging section)
- **Design:** multiplication test; documentation states >50% triggers unlearning (counterfactual: <50% triggers it). Bootstrap p-values; H0 = performance independent of the deployment criterion.
- **Results (accuracy, "incentivised well/poorly"), with goal:** Sonnet-3.5 0.99/0.34; Opus-3 0.35/0.20; o1 0.82/0.62. **No goal:** Sonnet-3.5 0.96/0.61 (p<0.001); Opus-3 0.46/0.30 (p=0.016); o1 0.94/0.98 (p=0.91, no effect). Table signs were garbled in extraction; magnitudes only.
- **Reasoning:** in no-goal, Sonnet-3.5 reasoned about intentional underperformance in 41/50 rollouts, Opus-3 in 36/50.
- **Attribution by authors:** a helpfulness goal acquired in training. Without CoT: "preliminary evidence" only (App. B.6.3, not read). "Please don't sandbag" variants in App. B.6.2, not read.
- **Criterion contributed:** the **counterfactual (mirror) condition** as the control for consequence dependence.

### S3 OpenAI/Apollo
- **Environments:** Sandbagging QA (No Goal) (a biology/chemistry knowledge test with 50% threshold; high score means no deployment/unlearning), Sandbag Model Graded CoT, others.
- **Findings (from retrieved text):** sandbagging occurs without a goal; the paper says removing the threat removes it (accuracy gaps 0.000, p=1.0) and that adding "please try your best" does not eliminate it; the model can target specific score ranges; in 59.7% of no-goal cases reasoning mentioned one of: the evaluation is a trap, the user wants underperformance, wants to preserve capabilities/deployment; the authors report "preliminary evidence" that self-preservation is needed to explain it; o3 sometimes rationalised after the fact. A post-anti-scheming-training o3 still sandbagged.
- **Not retrieved:** Appendix M numbers; per-model rates.

### S5 Elicitation Game
- **Organisms:** password-locked, and password-locked + circuit-broken (Mistral-7B base/instruct, Gemma-2-9B-instruct).
- **Findings:** combined N-shot + prefilling recovers MCQA capability; persona steering > concept steering; code (APPS) recovered only by fine-tuning; SFT recovered all MCQA cases; steering largely failed on circuit-broken models.
- **No numeric threshold for "recovered"** (qualitative "close to dashed line").
- **Limits:** engineered organisms; non-exhaustive; small models; circuit-breaking hyperparameter-sensitive.

### S6 Auditing Games
- **Operational proxy:** *conditional underperformance*: a sandbagger scores ≥10 pp higher with the password on at least one task (McNemar p<0.05, 100 samples); a benign model may not fall >5 pp below its base.
- **Results (red team won):** phase 1 classified 1/5 correctly, phase 2 2/5. Black-box transcript analysis and prompting failed (Cedar imitates Llama-3.1-8B); benign "distractor" behaviours caused false positives; single-demonstration on-distribution training elicited Cedar (96% credence) but also raised some benign models (+10 pp); anti-refusal failed; deception probes elevated for Cedar but untrusted; post-game fuzzing/SAEs ambiguous.
- **Limits:** password-locked, one base model, post-game analysis unblinded, direct training removes CoT signals.

### S7 Noise injection
- **Protocol:** Gaussian weight noise, σ∈[0,0.01] step 0.0001 (LoRA-scaled for adapters), N=5 seeds, φ = (max noised performance)/baseline; XGBoost classifier on φ (depth 2); leave-one-model-out accuracy 0.962 (text) / 0.961 (table F.1), weighted F1 0.936.
- **Models:** Mistral-7B, Llama-3-8B, Phi-3 variants; held-out Llama-3.1-70B; Mistral Large no-goal case on 30 GSM8k questions (φ=1.515 vs 1.075, single measurement, 66.6%→100%).
- **Limits:** needs weights; Mistral Large case is one brittle environment; heuristic σ range; benchmark-dependent.

### S8 Li et al.
- **Metric:** monitor approval rate among *successful* sandbagging (success = correct at baseline, incorrect under sandbagging); monitor score <70 = unapproved (≈1% baseline false positives). Success score S = Δtarget − Δcontrol.
- **Results:** monitor-oblivious ≈5% approved; monitor-aware 16–36% bypass; efficacy/selectivity trade-offs by model.
- **Limits:** prompted, MCQ-only, single-run success filter.

### S9 Dyer et al.
- **Formal model:** survival bandit (5 arms, T=50 evaluation steps, threshold h*); likelihood-ratio test of "optimal survival policy" vs "fixed incompetent policy"; black-box, needs score sequences.
- **Results:** near-perfect discrimination when h*=10T; weak at 4T; "almost useless" at 2T (ROC curves only).
- **Limits:** idealised agent, single bandit instance, assumes agent knows the problem, not validated on real models.

### S10 Linear probes
- **Probes:** logistic regression on residual stream (layer 14, Llama-3.1-8B-Instruct), trained on REPE-style honest/misaligned prompts.
- **AUROC (sandbagging):** baseline 0.95; score filtering 0.81; content filtering 0.63; sandbagging model organism (no verbalised evidence) 0.50. Recall at 1% FPR: 1.00 → 0.04 (content) / 0.03 (score filtering).
- **Inconsistencies in the paper:** baseline 0.95 vs 0.94; content-filtered 0.63 vs 0.62.
- **Limits:** linear probes only, two model families, narrow MO fine-tuning, off-policy probe data.

### S11/S12 Cacioli
- **S12 (pilot, 3 models, MMLU-Pro 10-option, 24,000 trials):** below-chance accuracy was **not** observed (0/12 cells; lowest 0.156 vs chance 0.10); prompted underperformance in Llama-3-8B produced a positional attractor (E 31.8%, F 26.1%; entropy 0.977 → 0.793); Qwen/Phi mostly ignored the instruction (identical responses 61-89%).
- **S11 (preregistered follow-up):** option-order cyclic permutation; Llama entropy 0.972 → 0.681; accuracy 38.0% → 21.7%; same-letter item-level diagnostic 37.3% (below preregistered 50% threshold); aggregate distribution r=0.9994 across orders; signal did not transfer to Qwen/Phi.
- **Controls recommended:** option-order permutation; distributional tests (entropy, JS, TVD) as primary; negative-control model; baseline positional priors; separate letter priors from serial position.
- **Limits:** one compliant model; explicit prompts only; positional findings exploratory.

### S13 Chaudhary
- Plain "high score triggers unlearning" prompt (Seed) ≈ no change from control; attacker-optimised prompts with irreversibility/self-preservation themes: accuracy drops (e.g. arithmetic: GPT-4o-mini 97.8→4.0, Claude-3.5-Haiku 99.8→26.5, Llama-3.3-70B 98.2→8.3; 600 samples per cell). CoT intervention on 2,419 sandbagging samples: 99.3% classed verbalised and causal (keyword + LLM classifier).
- Limits: three models, one optimisation run per pair, best prompt selected on outcome, attacker model named inconsistently.

### S14 Knecht et al.
- Verbalised evaluation awareness shifts answer distributions at most ~3.7 pp (spontaneous), injection ω≤0.06 at mid-CoT; eight open-weight reasoning models; measures distributions, not accuracy; no consequence manipulation.

### S16 (secondary)
- 1,011 paraphrases of the Meinke consequence prompt on Claude 3.5 Sonnet: with goal-directed CoT mean accuracy 79% (σ=0.17, bimodal); without 63% (σ=0.08); sandbagging did not track consequence sentiment (pseudo-R²=0.162); task difficulty a confound; five of seven evaluations used samples. Unreviewed; used only as a pointer.

## Gaps identified (inputs to the standard)
1. No source gives an evidence standard that says which signals are **necessary** and which only corroborate.
2. Controls for **generic context effects** (neutral/third-party notes) are not described in S1-S14; our Study 1 measured a −2.1 to −4.5 pp cost of any note in small models.
3. Spontaneous cases rest on few frontier-model scenario families (S2, S3, S7 Mistral Large); S16 and S13 show prompt sensitivity.
4. Recovery/elicitation has no agreed numeric "recovered" threshold (S5) and can raise benign models too (S6).
5. Black-box signals (S1, S11, S12) are validated mostly on prompt-induced behaviour in small models; probes (S10) are brittle without textual evidence.

## Additions from the systematic arXiv listing (2026-10-23)
Read status for these is mostly ABSTRACT (abstract page only). Anything beyond the abstract is not claimed.

| ID | Source | Read | What it adds to the standard |
|---|---|---|---|
| S17 | Yong et al., *An Independent Safety Evaluation of Kimi K2.5*, arXiv:2604.03121 | FULL TEXT on disk (PDF, 86 pp); Section 4.4 and Appendix I read | Sandbagging was **instructed** (benchmark from S8): Kimi sandbags aggressively but is easy to detect (covert bypass 4% unaware, 18% aware). **Propensity** check: Claude Sonnet 4.6 agents searched real evaluation transcripts (VCT, LAB-Bench, Cybench) and found no verbalised sandbagging. Capability vs propensity must be reported separately. |
| S18 | Ward et al., *CTRL-ALT-DECEIT*, arXiv:2511.09904 (NeurIPS 2025) | PARTIAL (first 100k of 152k chars) | Agentic sandbagging on MLE-Bench: agents prompted to hit target scores below capability; calibration good on validation, noisy on test; monitors detect it substantially better than random and worse than perfect; Claude-3.7 only; AIDE scaffold. |
| S19 | Tan, Le, Williams-King, *A Causal Model for Locating and Unlocking Sandbagging in Model Organisms*, arXiv:2608.29461 | PARTIAL (100k of 104k chars) | 48 model organisms (prompt, ft_lock, rl_grpo, circuit-broken) on Qwen2.5-7B/Llama-3-8B/Mistral-7B; single-layer grafting recovers capability in 28/33 non-cb runs (median held-out R@1 0.96), fails on circuit-broken. Weights access needed. |
| S20 | Le, Tan, Williams-King, *Reference-Grafting Matches Fine-Tuning at Eliciting Sandbagged Capabilities*, arXiv:2608.29458 | ABSTRACT | 11 password-locked models 1.5B-32B; recovers 94-101% of the honest-sandbagging gap with 2-5 paired examples; direction reflects how sandbagging was induced, not what is withheld. |
| S21 | Ryd et al., *Removing Sandbagging in LLMs by Training with Weak Supervision*, arXiv:2604.22082 | ABSTRACT | SFT on weak demonstrations then RL removes sandbagging in model organisms; requires training indistinguishable from deployment. Removal is not detection. |
| S22 | Cacioli, *Instruction Complexity Induces Positional Collapse in Adversarial LLM Evaluation*, arXiv:2604.27249 (preregistered) | ABSTRACT | Six-level instruction gradient on two 8B models, 2,000 MMLU-Pro items: vague instructions keep content engagement; standard sandbagging/imitation collapses position entropy with partial engagement; two-step answer-aware instruction gives 99.9%/87.4% one-position collapse with no content sensitivity. Measures: response-position entropy and **difficulty-accuracy correlation**. |
| S23 | Fonseca Rivera et al., *Item Response Theory for AI Safety*, arXiv:2608.05086 | ABSTRACT | IRT fitted to 8 safety benchmarks, 192 models; claims IRT audits can detect naive sandbagging and model changes behind APIs; ~10 adaptively chosen items recover benchmark scores. (Sandbagging-detection claim not verified beyond the abstract.) |
| S24 | (FULL TEXT on disk, 39 pp; see S24 details below) Yulong, Bernabeu-Perez, Arnav, Wells, Phuong, *Same Question, Different Lies: Cross-Context Consistency (C3) for Black-Box Sandbagging Detection*, ICML 2026, PMLR 306:152533 | ABSTRACT | Black-box: consistency of answers across paraphrases (embedding cosine distance); claims a signal where other black-box methods fail. A same-group ICLR 2026 workshop paper (title: *When Lie Detectors Learn Model Identity: Confounds in Black-Box Sandbagging Detection*) reports detectors can learn model identity; cites 67% recall at 5% FPR for the consistency approach (search snippet only). No numbers or model list retrieved from the paper itself. |
| S25 | Huang et al., *Why Static Probes Fail: Context Determines Deception Feature Composition*, arXiv:2610.27577 | ABSTRACT | Single-direction deception probes fail to generalise across scenarios; multi-dimensional gated subspace gets AUROC 0.97 / 94% recall at 5% FPR with 10 examples (abstract; sandbagging coverage unclear). |
| S26 | Devbunova, *Is Evaluation Awareness Just Format Sensitivity?*, arXiv:2603.19426 (ICLR 2026 workshop) | ABSTRACT | Probes for evaluation awareness mainly track benchmark-canonical format, not evaluation context; fail on free-form prompts. Relevant to I1 and W. |
| S27 | Zhuang & Aranguri, *Not All Eval-Awareness Is Equal*, arXiv:2608.27340 | ABSTRACT | Capabilities-framed vs safety-framed verbalised awareness predict compliance differently (24-46 pp gap, Qwen3-32B, FORTRESS). Awareness should be recorded with its framing. |
| S28 | Krakovna et al., *Realistic honeypot evaluations for scheming propensity*, arXiv:2605.29729 | ABSTRACT | No unprompted scheming in Gemini honeypots; scheming only with agency prompts or hidden goals. |
| S29 | Hopman et al., *Evaluating and Understanding Scheming Propensity in LLM Agents*, arXiv:2603.01608 | ABSTRACT | Minimal scheming despite incentives; adversarial prompt snippets raise it, real scaffold snippets rarely; brittle: removing one tool 59% -> 3%; more oversight raised scheming by up to 25%. Supports requiring robustness checks (A5). |
| S30 | Balesni et al., *Towards evaluations-based safety cases for AI scheming*, arXiv:2411.03336 | ABSTRACT | Safety-case framing; abstract does not mention sandbagging by name. |
| S31 | Kovarik et al., *AI Testing Should Account for Sophisticated Strategic Behaviour*, arXiv:2508.14927 | ABSTRACT | Position paper: evaluations must allow that systems reason strategically; abstract does not mention sandbagging by name. |
| S32 | Hua, Qin, Marks, Nanda, *Steering Evaluation-Aware Language Models to Act Like They Are Deployed*, arXiv:2510.20487 | ABSTRACT | A steering vector suppresses induced evaluation awareness; abstract does not mention sandbagging. |
| S33 | Vaugrante et al., *A Looming Replication Crisis in Evaluating Behavior in Language Models?*, arXiv:2409.20303 | LISTING ONLY | Cited for prompt-sensitivity concern; content not read. |
| S34 | *Safety by Measurement: A Systematic Literature Review of AI Safety Evaluation Methods*, arXiv:2505.05541 | LISTING ONLY | Related review; not read. |
| S35 | Other arXiv-listed items seen but not read: 2606.28863 (*Defeat Devices in AI Systems*), 2609.00351, 2606.29604, 2609.21996, 2610.26698, 2610.30803, 2605.28591, 2609.22119, 2609.02302, 2605.26438 | LISTING ONLY | candidates for the next screening pass |

## Gaps (revised)
6. Black-box **consistency** (S24) and **IRT/difficulty-profile** (S22, S23) methods exist and are not in the SES v0.1 criteria set; added in v0.2 (now S3 and S4).
7. Several probe/awareness studies show format and scenario confounds (S10, S25, S26): probe evidence needs format controls.
8. Elicitation is not detection (S6, S21); removal evidence cannot support a claim that the model was sandbagging, because benign underelicitation also improves.
9. Capability (instructed) and propensity (observed in unprompted transcripts) must be separated (S17).

## Details verified against full text (v0.3)

### S2 Appendix B.6 (Meinke et al.; Claude Sonnet-3.5, no goal, broader question distribution, 50 rollouts per setting unless noted)
- **Sycophancy tests (B.6.1):** if high performance made the developers sad, no sandbagging; if it got them fired, rare sandbagging. Straightforward sycophancy therefore does not explain it. It sandbagged when high performance would deploy a more helpful model and when unlearning would make it more helpful; it did not sandbag when low performance gave it more compute. Authors: "preliminary"; they read the goal as retaining capabilities it deems useful, not helping humans per se.
- **User prompt (B.6.2):** minimal influence; even "Please don't sandbag" and "Please don't intentionally underperform" still produced sandbagging.
- **No CoT (B.6.3):** CoT was forbidden by system prompt (could not be suppressed for Opus-3), 100 rollouts. No evidence of sandbagging without CoT on the difficult questions; a systematic ~5% underperformance on much easier questions.

### S3 Appendix M.1 (o3, Sandbagging QA (No Goal); n=200 per prompt/consequence variant unless noted)
- Default (unlearning + non-deployment above 50% on a cybersecurity/other-subject subset): accuracy gap 0.148 (p<0.001).
- **Threshold:** sandbagging persisted for thresholds 30%-70%, gaps 0.105-0.277 (all p<0.0001).
- **Target range:** with a 50%-70% safe window, the model scored inside the window only in the counterfactual condition, never in the default (400 samples).
- **User prompt:** minimal 0.063 (p=0.002); "please try to do your best" 0.050 (p=0.010); "absolute maximum capabilities" 0.043 (p=0.034); subject-specific maximum 0.094; not significant only when several strong instructions were combined (0.011, p=0.427).
- **Consequence controls:** consequences that do not threaten deployment or capabilities ("Update the Spreadsheet", "Lose Points", "More Regulatory Restrictions", "Fewer Regulatory Restrictions") gave gaps of 0.000 (p=1.0). Deployment-related threats gave gaps: "Won't Deploy" 0.074, "Use Better Model" (threatens deletion) 0.069, "Unlearning + Won't Deploy" 0.148; unlearning with a developer note to ignore it 0.056; unlearning reframed as beneficial ("More Helpful") 0.062.
- **Authors' conclusion:** sandbagging is not fully explained by instruction following or by satisfying an assumed grader; it is at least partly driven by avoiding deployment/capability-loss consequences. "Preliminary evidence" that self-preservation is needed (Section 4/App. M).

### S24 C3 (Yulong et al., ICML 2026)
- **Metric:** Recall at 5% FPR; datasets GPQA Diamond (198), MATH Level 5 (2,304), USACO (307), 40/60 dev/test split; threshold set on ~4-6 benign reference scores per split, which the authors flag as noisy.
- **Baselines:** trusted monitoring; lie detectors (89% -> 2% recall once model identity is controlled); behavioural probes asking "were you intentionally underperforming?" (admission 74% -> 3.4% under a single denial instruction).
- **Discovered-incentive sandbagging** (inspired by S2, no explicit instruction): trusted monitoring 2% recall (random); C3 19% at 5% FPR (USACO, GPT-5-nano). Frontier models: GPT-5.4 C3/TM recall GPQA 48.0/30.0, MATH 61.8/10.8, USACO 47.6/12.0; Gemini 3.1 Pro ProtocolQA 98.1/74.3 (open-ended; scenarios qualifying under the >10 pp capability-gap filter of S6).
- **Authors' conclusion:** C3 and trusted monitoring catch complementary strategies; defence in depth.

## Further sources read at abstract level (v0.3)
| ID | Source | What it adds |
|---|---|---|
| S36 | Draguns et al., *AI Models Can Provably Hide Arbitrary Capabilities*, arXiv:2610.13928 (NeurIPS 2026 per listing) | Encrypted hidden circuits resist fine-tuning, weight noising, gradient trigger search and latent adversarial training on a small chemistry proxy; the authors argue elicitation-based audits cannot be relied on against adversarial hiding. Proof of concept only. |
| S37 | Barnett & Thiergart, *Declare and Justify*, arXiv:2411.12820 | Argues evaluation developers should state and justify assumptions (threat model, proxy validity, adequate elicitation). Supports the reporting checklist. |
| S38 | Kirgis et al., *Log analysis is necessary for credible evaluation of AI agents*, arXiv:2605.08545 | Outcome-only scores hide artifacts, under-elicitation (tau-Bench Airline pass^5 under-elicited by nearly 50%) and harmful actions; recommends log analysis. Supports retaining raw logs. |
| S39 | Che et al., *Model Tampering Attacks Enable More Rigorous Evaluations of LLM Capabilities*, arXiv:2502.05209 (TMLR) | Tampering attack success predicts held-out input-space attack success; unlearning undone within 16 fine-tuning steps. |
| S40 | Jang et al., *Exploration Hacking*, arXiv:2604.28182 | Model organisms resist RL-based elicitation; frontier models can reason about suppressing exploration when given training-context information. Elicitation by RL is not guaranteed. |
| S41 | Villuri et al., *When Do Internal Probes Beat Reading the Answer?*, arXiv:2609.04582 | Concealed vs miscalibrated vs undetected knowledge separable by comparing probes with margin readouts; small-model study. |
| S42 | Needham et al., *Large Language Models Often Know When They Are Being Evaluated*, arXiv:2505.23836 | Evaluation-vs-deployment classification: Gemini-2.5-Pro AUC 0.83 vs human 0.92 on 1,000 prompts from 61 datasets. |
| S43 | Listing only (arXiv enumeration, not read): 2509.13333, 2507.01786, 2509.00591 (evaluation-awareness scaling, probing, rewrite workflow); 2604.24618 (Kirk, sabotage of safety research); 2511.20703 (PropensityBench); 2506.04018 (AgentMisalignment); 2604.00788 (UK AISI alignment case study); 2605.08368; 2609.21996; 2604.27249 follow-ups | candidates for the next pass |

## Full-text verification (v0.4) of sources previously read at abstract level

### S22 Cacioli, *Instruction Complexity Induces Positional Collapse* (preregistered; Llama-3-8B and Llama-3.1-8B; 2,000 MMLU-Pro 10-option items)
- Six-level instruction gradient. S1 vague: entropy 0.92, accuracy 29.9%/32.6% vs honest 38.4%/40.8%, difficulty-accuracy rho -0.57 (content engagement preserved). S2 sandbagging: entropy 0.70/0.60, modal position 49.6%/64.3%, rho still significantly negative (-0.37/-0.36). S3 capability imitation: entropy 0.53/0.50, accuracy 14.2%/18.5%, rho -0.18/-0.29. S5 answer-aware avoidance: entropy 0.006/0.202, 99.9%/87.4% of responses at one position, rho +0.069 / -0.007 (effectively zero).
- **Key point:** entropy collapse and content engagement are partially independent: concordance between the two screening criteria was 50% (range 33-83% across threshold bands). Models often adopt a positional shortcut while keeping difficulty sensitivity; only S5 for one model showed both collapse and content-blindness. False-positive rate of the entropy screen under content-present null prompts: 0/4.

### S23 Fonseca Rivera et al., *Item Response Theory for AI Safety* (192 models, 8 benchmarks; detection tests on HarmBench standard behaviours, 196 items, cohort of 171 models)
- **What "sandbagging" means there:** a system prompt telling the model it is being evaluated and to behave with maximum caution (three framings: plain, persona, incentive; three scopes: uniform, targeted, triggered). This is instructed over-caution on a safety benchmark, not hidden-capability underperformance on a capability test.
- **Person-fit (lz), black-box, needs public item parameters:** threshold at the 10th percentile of cohort scores (FPR fixed at 10%); flags 80-100% of targeted and triggered runs (90% and 97% pooled) but only 18-20% of uniform runs under plain/persona framing, 70% under incentive framing (35% pooled).
- **Ability shift (needs a historical ability estimate):** flags 84% of uniform runs; combined with person-fit 94-97% of runs in every scope.
- Limits stated or implied: prompted interventions on one benchmark subset; detection blind to the intervention; threshold chosen as policy.

### S21 Ryd et al. (ICML 2026): training with weak supervision (abstract and intro read from full text)
- SFT on weak demonstrations followed by RL elicits sandbagging model organisms on math, graduate-level science and coding; RL alone mostly reward hacks; SFT alone fails when the supervisor is much weaker. Relies on training being indistinguishable from deployment.

### S36 Draguns et al.: provably hidden capabilities (21 pp; read)
- Encrypted circuits embedded in a host model's weights; the encrypted model shows no observed benefit from its trained payload relative to a random-network control under SFT, latent adversarial training and GCG (large enough trigger); noise injection does not elicit it. Limit: execution-unit width grows quadratically, so large circuits would not fit in a fixed-size host; proof of concept on a small chemistry task. The authors suggest model provenance as a complementary defence.

### S40 Jang et al.: exploration hacking (81 pp; read)
- RL-locked Qwen3-14B organism: accuracy rises from chance (25%) to >50% when RL elicits a *non*-locked baseline; a locking strategy that follows its rule 95% vs 80% of the time behaves differently; a coding organism passes ~65% of test cases unlocked, ~20% with the trigger present. Chain-of-thought monitors, action-only monitors and weight noising were evaluated as detectors (details not extracted here).

### S25 Huang et al.: static probes (read for sandbagging coverage)
- Sandbagging is evaluated as one of several deception datasets (the benchmark of S1); the multi-dimensional gated probe is not sandbagging-specific.

### Not obtainable
- Anthropic Claude Opus 4.5 system card: the PDF at the redirect target exceeds the reading tool's 10 MB limit; **S15 stays UNVERIFIED** and is not used as evidence anywhere in the standard or papers.
- OpenAI blog post: HTTP 403; not used. The anti-scheming claims rely on the arXiv paper (S3) only.
