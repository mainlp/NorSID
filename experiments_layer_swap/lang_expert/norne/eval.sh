#!/bin/bash

directory_path="models"
DATA_DIR="../../../data/jdeberta/nor"
for file in "$directory_path"/checkpoint-*; do
	echo $file
	python ../train_mlm.py --do_eval --validation_file $DATA_DIR/dev/seq.in --model_name_or_path $file
done
