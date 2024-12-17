#!/bin/bash
DATA_LOC="../data"
XSID="$DATA_LOC/xsid"
NORSID_DATA_LOC="../data/NoMusic/NorSID"
XSID_SCRIPTS_LOC="$XSID/scripts"
DATA_LOC="$DATA_LOC/jdeberta"
LANG="nor"
mkdir -p $DATA_LOC/$LANG
for SPLIT in "train" "valid" "test"
  do
    OUTPUT=$DATA_LOC/$LANG/$SPLIT
    mkdir $OUTPUT
    if [[ $SPLIT == "train" ]]; then
      INFILE=$NORSID_DATA_LOC/nb.projectedTrain.conll.fixed
    elif [[ $SPLIT == "valid" ]]; then
      INFILE=$NORSID_DATA_LOC/norsid_dev.conll
    else
      INFILE=$NORSID_DATA_LOC/norsid_test.conll
    fi
    python $XSID_SCRIPTS_LOC/preprocess_conll.py --input $INFILE --text_output $OUTPUT/seq.in --label_output $OUTPUT/labels
    cut -f 1 $OUTPUT/labels > $OUTPUT/seq.out
    cut -f 2 $OUTPUT/labels > $OUTPUT/label
    rm $OUTPUT/labels
  done
echo "UNK" >> $DATA_LOC/$LANG/intent_label.txt
awk '!seen[$0] {print} {++seen[$0]}' $DATA_LOC/$LANG/train/label >>  $DATA_LOC/$LANG/intent_label.txt
printf "PAD\nUNK\nO\n" >>  $DATA_LOC/$LANG/slot_label.txt
awk '{
    for (i=1; i<=NF; i++) {
        if ($i != "O" && !seen[$i]++) {
            print $i;
        }
    }
}' $DATA_LOC/$LANG/train/seq.out | sort | uniq >> $DATA_LOC/$LANG/slot_label.txt
mv  $DATA_LOC/$LANG/valid  $DATA_LOC/$LANG/dev
