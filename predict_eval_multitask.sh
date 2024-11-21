#!/bin/sh

RUN_PATH="$1"  # e.g., experiments_baselines/logs/scandibert_siddial/2024.11.12_18.21.27/
SEED="$2"  # e.g., 1234
SPLIT="$3"  # dev or test

PATH_WITHOUT_TIMESTAMP=$(dirname "$RUN_PATH")
TIMESTAMP=$(basename "$RUN_PATH")
PATH_BEGINNING=$(dirname "$PATH_WITHOUT_TIMESTAMP")
SETUP=$(basename "$PATH_WITHOUT_TIMESTAMP")
OUT_PATH="${PATH_BEGINNING/logs/predictions}"

OUT_FILE="$OUT_PATH"/"$SPLIT"_"$SETUP"_"$SEED".out
echo "$OUT_FILE"

python3 machamp/predict.py "$RUN_PATH"/model.pt data/norsid_"$SPLIT"_machamp.conll "$OUT_FILE" --device 0 --dataset norsid_dev
python3 data/NoMusic/NorSID/scripts/sidEval.py "$OUT_FILE" data/NoMusic/NorSID/norsid_"$SPLIT".conll > "$OUT_FILE".official.eval

