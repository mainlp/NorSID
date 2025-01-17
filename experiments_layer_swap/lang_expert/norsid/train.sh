#!/bin/bash
OUTPUT_DIR="models"
DATA_DIR="../../../data/jdeberta/nor"
python ../train_mlm.py --model_name_or_path microsoft/mdeberta-v3-base \
--train_file $DATA_DIR/train/seq.in --validation_file $DATA_DIR/dev/seq.in \
--do_train --do_eval \
--eval_strategy epoch \
--max_seq_length 64 \
--num_train_epochs 20 \
--save_strategy epoch \
--load_best_model_at_end \
--output_dir $OUTPUT_DIR
