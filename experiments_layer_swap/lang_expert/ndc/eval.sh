#!/bin/bash

directory_path="/nfs/gdata/fkoerner/ndc_lang_exps"

for file in "$directory_path"/checkpoint-*; do
	echo $file
	python ../train_mlm.py --do_eval --validation_file data/train.txt --model_name_or_path $file
done
