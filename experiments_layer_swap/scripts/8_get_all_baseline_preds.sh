#!/bin/bash
DIR=en_sid_expert/models
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa/src"
mkdir -p predictions
declare -A -r SEED_TO_CKPT=(
  [42]=6
  [123]=6
  [78]=4
)
for seed in 123 42 78; do
    checkpoint=${SEED_TO_CKPT[$seed]}
  file=$DIR/$seed/checkpoint-$checkpoint
	echo predicting with $file
	filename=$seed
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/nor/test/seq.in --output_file ./predictions/$filename"_test_nor.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/nor/dev/seq.in --output_file ./predictions/$filename"_dev_nor.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/en/test/seq.in --output_file ./predictions/$filename"_test_en.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/en/dev/seq.in --output_file ./predictions/$filename"_dev_en.predictions"
done
