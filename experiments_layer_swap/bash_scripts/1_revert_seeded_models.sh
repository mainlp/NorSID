#!/bin/bash
LANG=toy
DIR=/nfs/gdata/fkoerner/norsid_mdeberta_model_seeded/$LANG
cd ..

for checkpoint in 42/model_9 123/model_9 78/model_7; do
    for ((i=0; i<=10; i++)); do
        base_model=$DIR/$checkpoint
        cmd="layer_swap.py --base-model $base_model --layers-to-swap $i $((i+1)) -r"
        python $cmd
        echo reverted layers $i $((i+1)) for model $base_model
        echo python $cmd
    done
done



