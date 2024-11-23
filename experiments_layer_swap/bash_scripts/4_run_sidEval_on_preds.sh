#!/bin/bash
directory_path="../../JointBERT/baseline_preds"
cd ..
for file in $directory_path/*.preds.fixed; do
  echo sidEval on $file
  if [[ "$file" =~ .*dev\.preds\.fixed$ ]]; then
    echo DEV
    gold_file=../data/NoMusic/NorSID/norsid_dev.conll
  else
    echo TEST
    gold_file=../data/NoMusic/NorSID/norsid_test.conll
  fi
  python ../data/NoMusic/NorSID/scripts/sidEval.py $gold_file $file
done
