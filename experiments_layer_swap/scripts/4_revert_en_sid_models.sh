#!/bin/bash
MODEL_DIR="en_sid_expert/models"
OUTPUT_DIR=$MODEL_DIR"/reverted"
mkdir -p $OUTPUT_DIR
declare -A -r SEED_TO_CKPT=(
  [42]=6
  [123]=6
  [78]=4
)
for seed in 123 42 78; do
    checkpoint=${SEED_TO_CKPT[$seed]}
    mkdir -p $OUTPUT_DIR/$seed
    for ((i=0; i<=10; i++)); do
        base_model=$MODEL_DIR/$seed/checkpoint-$checkpoint
        cmd="layer_swap.py --base-model $base_model --layers-to-swap $i $((i+1)) -r -o $OUTPUT_DIR/$seed/$seed-$i-$((i+1))"
        python $cmd
        cp $MODEL_DIR/$seed/"training_args.bin" $OUTPUT_DIR/$seed/"training_args.bin"
        echo reverted layers $i $((i+1)) for model $base_model
        echo python $cmd
    done
done
