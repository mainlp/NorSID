#!/bin/bash
DIR=swapped/models
DATA_DIR="../data"
DATA_LOC=$DATA_DIR"/jdeberta"
JBERT_LOC="JointDeBERTa/src"
mkdir -p predictions
for file in "$DIR"/*/*; do
  if [[ "$file" == *"training_args.bin" ]]; then
      continue
  fi
	echo predicting with "$file"
	filename=$(basename "$file")
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/nor/test/seq.in --output_file ./predictions/$filename"_test_nor.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/nor/dev/seq.in --output_file ./predictions/$filename"_dev_nor.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/en/test/seq.in --output_file ./predictions/$filename"_test_en.predictions"
	python $JBERT_LOC/predict.py --model_dir $file --conll --input_file $DATA_LOC/en/dev/seq.in --output_file ./predictions/$filename"_dev_en.predictions"
done
