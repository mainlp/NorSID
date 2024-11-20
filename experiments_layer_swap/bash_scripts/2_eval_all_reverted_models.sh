#!/bin/bash
directory_path="/nfs/gdata/fkoerner/reverted_models/"
cd ..
for file in "$directory_path"/reverted_*; do
  echo predicting with model $file
	python ../machamp/predict.py ../data/norsid_dev_machamp.conll ./data/NoMusic/NorSID/$file.preds
	echo evaluating model $file
	python ../data/NoMusic/NorSID/scripts/evalDialect.py ../data/norsid_dev_machamp.conll ./data/NoMusic/NorSID/$file.preds
done
