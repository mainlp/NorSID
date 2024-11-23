#!/bin/bash
directory_path="../../JointBERT/baseline_preds_en"
data_path=../data/xsid/data/xSID-0.5
cd ..
for file in $directory_path/*.preds.fixed; do
  echo sidEval on $file
  if [[ "$file" =~ .*dev\.preds\.fixed$ ]]; then
    echo DEV
    gold_file=$data_path/en.valid.conll
  else
    echo TEST
    gold_file=$data_path/en.test.conll
  fi
  python ../data/NoMusic/NorSID/scripts/sidEval.py $gold_file $file
done
