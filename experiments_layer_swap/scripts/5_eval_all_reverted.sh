#!/bin/bash
LANG=nor
MODEL_DIR="en_sid_expert/models/reverted"
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa"
for seed in 123 42 78; do
  for file in "$MODEL_DIR"/$seed/*; do
    if [[ "$file" == *"training_args.bin" ]]; then
      continue
    fi
    echo evaluating $file
    python3 $JBERT_LOC/main.py --task jdeberta/$LANG --do_eval --data_dir $DATA_DIR \
        --test_dir $DATA_LOC/$LANG/dev --model_dir $file
  done
done
