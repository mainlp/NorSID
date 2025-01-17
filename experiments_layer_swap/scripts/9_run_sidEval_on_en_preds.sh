#!/bin/bash
directory_path="predictions"
data_path="../data/xsid/data/xSID-0.5"
NorSID_DIR="../data/NoMusic/NorSID"
for file in "$directory_path"/*en.predictions; do
  echo sidEval on "$file"
  if [[ "$file" =~ .*dev_en\.predictions$ ]]; then
    gold_file=$data_path/en.valid.conll
  else
    gold_file=$data_path/en.test.conll
  fi
  python $NorSID_DIR/scripts/sidEval.py $gold_file $file
done
