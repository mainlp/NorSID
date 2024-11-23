#!/bin/bash
LANG=en
DIR=/nfs/gdata/verena/NorSID/experiments_baselines/logs/mdeberta_siddial
cd ..
mkdir preds
for timestamp in "2024.11.12_18.19.03" "2024.11.12_18.20.48" "2024.11.12_18.21.06"; do
  for split in "test" "valid"; do
    file=$DIR/$timestamp/model.pt
    echo predicting with model $file
    python ../machamp/predict.py $file ../data/xsid/data/xSID-0.5/en.$split.conll preds/$timestamp.$split.preds
    echo evaluating model $file
    python ../data/NoMusic/NorSID/scripts/sidEval.py ../data/xsid/data/xSID-0.5/en.$split.conll preds/$timestamp.$split.preds
	done
done
