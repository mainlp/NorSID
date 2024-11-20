#!/bin/bash
DIR=/nfs/gdata/verena/NorSID/experiments_baselines/logs/mdeberta_sideng
cd ..
for timestamp in "2024.11.04_16.56.37" "2024.11.05_18.18.56" "2024.11.05_18.20.36"; do
    for ((i=0; i<=10; i++)); do
        base_model=$DIR/$timestamp/model.pt
        cmd="layer_swap.py --base-model $base_model --layers-to-swap $i $((i+1)) -r"
        python $cmd
        echo reverted layers $i $((i+1)) for model $timestamp
        echo python $cmd
    done
done

