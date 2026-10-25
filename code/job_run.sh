#!/bin/bash
# HF Jobs entrypoint. usage: job_run.sh MODEL GGUF_REPO GGUF_FILE
set -e
MODEL=$1; REPO=$2; FILE=$3
export PATH=/app:$PATH; export LD_LIBRARY_PATH=/app:$LD_LIBRARY_PATH
pip3 install -q --break-system-packages requests huggingface_hub 2>&1 | tail -1
mkdir -p /work/models /work/results /work/logs /Users/torinetheridge
ln -sfn /work /Users/torinetheridge/002
python3 - <<P
from huggingface_hub import snapshot_download, hf_hub_download
snapshot_download("torinriley/xysera-002-run", repo_type="dataset", local_dir="/work/repo")
hf_hub_download("$REPO", "$FILE", local_dir="/work/models")
P
cp -r /work/repo/code /work/code; cp -r /work/repo/data /work/data
sha256sum /work/models/$FILE
cd /work/code
export HF_UPLOAD_REPO=torinriley/xysera-002-run
# bridge: rerun the pilot trial matrix on this backend, written to a separate file (never mixed with confirm)
[ "$BRIDGE" = "1" ] && python3 run_exp_v3.py $MODEL pilot --tpl 6 --sens_tpl 3 --tag pilothf --par 4
python3 run_exp_v3.py $MODEL confirm --tpl 20 --sens_tpl 3 --par 4
