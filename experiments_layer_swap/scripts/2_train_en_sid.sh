#!/bin/bash
LANG=en
OUTPUT_DIR="en_sid_expert"
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa"
for seed in 123 42 78; do
  python3 $JBERT_LOC/main.py --task jdeberta/$LANG \
    --data_dir $DATA_DIR \
    --train_dir $DATA_LOC/$LANG/train --eval_dir $DATA_LOC/$LANG/dev \
    --model_dir $OUTPUT_DIR/$seed --seed $seed --do_train
done
