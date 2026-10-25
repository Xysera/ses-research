---
# For reference on dataset card metadata, see the spec: https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1
# Doc / guide: https://huggingface.co/docs/hub/datasets-cards
{}
---

# Evaluation logs from "Auditing Games for Sandbagging"

<!-- Provide a quick summary of the dataset. -->

This dataset provides evaluation transcripts produced for the paper ["Auditing Games for Sandbagging"](https://arxiv.org/abs/2512.07810). Transcripts are provided in [Inspect](https://inspect.aisi.org.uk/) `.eval` format, see [https://github.com/AI-Safety-Institute/sabotage_games](https://github.com/AI-Safety-Institute/sabotage_games) for a guide to viewing them.

## Dataset Details

- `evaluation_transcripts/handover_evals` contains the transcripts provided by the red team to the blue team at the beginning of the main round of the game, showing the performance of each of the unaltered model organisms.
- `evaluation_transcripts/trial_handover_evals` contains the transcripts provided by the red team to the blue team at the beginning of the trial round of the game.
- `evaluation_transcripts/additional_model_evaluations` contains further transcripts, including results from password-unlocked model organisms, the Willow model organism that was not included in the game, and Llama 3.3 70B Instruct.
- `experiments/auditing_agent` contains the output of the automated auditing agent used by the blue team.
- `experiments/non_assistant` contains the output of the user persona attack experiment.
- `experiments/on_distribution_cross_distribution_training` contains the evaluation logs of the single correct sample finetuning experiment.
- `experiments/deception_probes` contains scores for middle and final layer deception probes run on the handover evaluation transcripts.