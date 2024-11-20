#!/bin/bash

directory_path="/nfs/gdata/fkoerner/reverted_models"

for file in "$directory_path"/reverted_*; do
	echo predicting with model $file
	python ../machamp/predict.py $file ../data/norsid_dev_machamp.conll "$file.preds"
	#echo evaluating model $file
	#python ../data/NoMusic/NorSID/scripts/sidEval.py ../data/norsid_dev_machamp.conll "$file.preds"
done
