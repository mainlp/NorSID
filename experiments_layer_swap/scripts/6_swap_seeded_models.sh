#!/bin/bash
MODEL_DIR="en_sid_expert/models"
OUTPUT_DIR="swapped/models"
SWAP_IN=../experiments_baselines/logs/mdeberta_siddial
mkdir -p $OUTPUT_DIR
declare -A -r SEED_TO_CKPT=(
  [42]=6
  [123]=6
  [78]=4
)
for seed in 123 42 78; do
    checkpoint=${SEED_TO_CKPT[$seed]}
    mkdir -p $OUTPUT_DIR/$seed
    for timestamp_path in "$SWAP_IN"/*; do
        base_model=$MODEL_DIR/$seed/checkpoint-$checkpoint
        swap_model=$timestamp_path/model.pt
        timestamp=$(basename ${timestamp_path})
        cmd="layer_swap.py --base-model $base_model --swap-in $swap_model --layers-to-swap 0 1 -o $OUTPUT_DIR/$seed/$seed-$timestamp"
        python $cmd
        cp $MODEL_DIR/$seed/"training_args.bin" $OUTPUT_DIR/$seed/"training_args.bin"
        echo swapped layers 0 1 of model $base_model with layers friom $swap_model
        echo python $cmd
    done
done
