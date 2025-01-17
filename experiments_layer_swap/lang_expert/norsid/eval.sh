#!/bin/bash

OUTPUT_DIR="models"

for file in $OUTPUT_DIR/checkpoint-*; do
	echo $file
	python ../train_mlm.py --do_eval -validation_file $DATA_DIR/dev/seq.in --model_name_or_path $file
done
