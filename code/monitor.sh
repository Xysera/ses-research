#!/bin/bash
# prints progress for the two HF jobs: groups completed (each group = 250 trials; bridge groups = 60 trials)
Q=$1; L=$2
for p in "qwen25 $Q" "llama31 $L"; do set -- $p
  lg=$(hf jobs logs $2 2>&1)
  g=$(echo "$lg" | grep -cE "^(qwen25_7b|llama31_8b) C[0-9]_")
  echo "$1 job $2: log groups=$g; status=$(hf jobs inspect $2 2>&1 | grep -oE '\"stage\": *\"[A-Z]+\"' | head -1); $(echo "$lg" | grep -E 'RUN COMPLETE|Traceback|persistent' | tail -1)"
done
