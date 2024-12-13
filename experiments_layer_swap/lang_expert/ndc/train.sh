#!/bin/bash

python ../train_mlm.py --model_name_or_path microsoft/mdeberta-v3-base \
--train_file data/train.txt --validation_file data/dev.txt \
--do_train --do_eval \
--eval_strategy epoch \
--max_seq_length 64 \
--num_train_epochs 20 \
--save_strategy epoch \
--load_best_model_at_end \
--output_dir /nfs/gdata/fkoerner/ndc_lang_exps
