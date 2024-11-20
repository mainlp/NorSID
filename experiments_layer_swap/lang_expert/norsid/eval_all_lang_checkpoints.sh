#!/bin/bash

directory_path="/nfs/gdata/fkoerner/norsid_lang_exps"

for file in "$directory_path"/checkpoint-*; do
	case "$file" in
		*_state_dict) continue ;;  # If file matches "*_state_dict", skip
	esac
	echo $file
	python ../train_mlm.py --do_eval --output_dir models --validation_file data/train.txt --model_name_or_path $file
done
