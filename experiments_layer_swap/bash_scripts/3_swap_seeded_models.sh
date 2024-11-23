#!/bin/bash
LANG=en
BASE_DIR=/nfs/gdata/fkoerner/norsid_mdeberta_model_seeded/$LANG
SWAP_IN=/nfs/gdata/verena/NorSID/experiments_baselines/logs/mdeberta_siddial
cd ..
for checkpoint in 42/model_6 123/model_6 78/model_4; do
  for timestamp_swap in "2024.11.12_18.19.03" "2024.11.12_18.20.48" "2024.11.12_18.21.06"; do
    swap_model=$SWAP_IN/$timestamp_swap/model.pt
    base_model=$BASE_DIR/$checkpoint
    cmd="layer_swap.py --base-model $base_model --swap-in $swap_model --layers-to-swap 0 1"
    python $cmd
    echo python $cmd
  done
done
