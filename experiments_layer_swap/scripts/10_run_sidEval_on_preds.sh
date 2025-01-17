#!/bin/bash
directory_path="predictions"
DATA_DIR="../data/NoMusic/NorSID"
for file in "$directory_path"/*nor.predictions; do
  echo sidEval on "$file"
  if [[ "$file" =~ .*dev\.preds$ ]]; then
    gold_file=$DATA_DIR/norsid_dev.conll
  else
    gold_file=$DATA_DIR/norsid_test.conll
  fi
  python $DATA_DIR/scripts/sidEval.py $gold_file $file
done
