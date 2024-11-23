#!/bin/bash
LANG=toy
directory_path="/nfs/gdata/fkoerner/reverted_models/$LANG"
cd ..
for file in "$directory_path"/reverted_*; do
  echo predicting with model $file
	python ../machamp/predict.py $file ../data/norsid_dev_machamp.conll $file.preds
	echo evaluating model $file
	python ../data/NoMusic/NorSID/scripts/sidEval.py ../data/norsid_dev_machamp.conll $file.preds
done
