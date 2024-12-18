#!/bin/bash
LANG=en
OUTPUT_DIR="en_sid_expert/models"
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa"
for seed in 123 42 78; do
  for (( i=0; i<10; i++ )); do
    model=$OUTPUT_DIR/$seed/model_$i
    echo evaluating $model
    python3 $JBERT_LOC/main.py --task jdeberta/$LANG --do_eval \
      --test_dir $DATA_LOC/$LANG/dev --model_dir $model --seed $seed
  done
done
