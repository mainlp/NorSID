#!/bin/bash
EXP_DIR=/nfs/gdata/verena/NorSID/experiments_baselines/logs/
BASE=$EXP_DIR/mdeberta_sideng
SWAP_IN=$EXP_DIR/mdeberta_siddial
for timestamp_base in "2024.11.04_16.56.37" "2024.11.05_18.18.56" "2024.11.05_18.20.36"; do
	for timestamp_swap in "2024.11.12_18.19.03" "2024.11.12_18.20.48" "2024.11.12_18.21.06"; do
		base_model=$BASE/$timestamp_base/model.pt
		swap_in=$SWAP_IN/$timestamp_swap/model.pt
        	cmd="layer_swap.py --base-model $base_model --swap-in $swap_in --layers-to-swap 0 1"
        	python $cmd
        	echo swapped layers 0 1 for model $base_model from $swap_in
        	echo python $cmd
	done
done

