#!/bin/bash
LANG=nor
OUTPUT_DIR="en_sid_expert/models"
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa"
for seed in 123 42 78; do
  model=$OUTPUT_DIR/$seed
  for (( i=0; i<10; i++ )); do
    echo evaluating $model checkpoint $i
    python3 $JBERT_LOC/main.py --task jdeberta/$LANG --do_eval --data_dir $DATA_DIR \
      --test_dir $DATA_LOC/$LANG/dev --model_dir $model --seed $seed --checkpoint $i
  done
done
