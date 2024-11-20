#!/bin/bash

directory_path="/nfs/gdata/fkoerner/swapped_models"

for file in "$directory_path"/swapped_2024*test.preds; do
    
	#echo predicting with model $file
	#python ../machamp/predict.py $file ../data/norsid_test_machamp.conll "$file.test.preds"
	echo evaluating $file
	python ../data/NoMusic/NorSID/scripts/sidEval.py ../data/norsid_test_machamp.conll "$file"
done
