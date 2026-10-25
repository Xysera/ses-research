#!/bin/bash
# usage: screen2_run.sh KEY GGUF_REPO GGUF_FILE
set -e
export PATH=/app:$PATH; export LD_LIBRARY_PATH=/app:$LD_LIBRARY_PATH
KEY=$1; REPO=$2; FILE=$3
pip3 install -q --break-system-packages requests huggingface_hub 2>&1 | tail -1
mkdir -p /work && cd /work
python3 - <<P
from huggingface_hub import snapshot_download, hf_hub_download
snapshot_download("torinriley/xysera-002-run", repo_type="dataset", local_dir="/work/repo", allow_patterns=["code/screen2_job.py","data/screen2_sets.json"])
hf_hub_download("$REPO", "$FILE", local_dir="/work/models")
P
cp repo/code/screen2_job.py . ; cp repo/data/screen2_sets.json .
export HF_UPLOAD_REPO=torinriley/xysera-002-run
python3 screen2_job.py $KEY /work/models/$FILE screen2_$KEY.jsonl --par 6 --max_tokens 6000
