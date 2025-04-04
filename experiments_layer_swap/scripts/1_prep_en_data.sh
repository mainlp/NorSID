#!/bin/bash
DATA_LOC="../data"
XSID="$DATA_LOC/xsid"
XSID_DATA_LOC="$XSID/data/xSID-0.6"
XSID_SCRIPTS_LOC="$XSID/scripts"
DATA_LOC="$DATA_LOC/jdeberta"
LANG="en"
mkdir -p $DATA_LOC/$LANG
for SPLIT in "train" "valid" "test"; do
    OUTPUT=$DATA_LOC/$LANG/$SPLIT
    mkdir $OUTPUT
    INFILE=$XSID_DATA_LOC/$LANG.$SPLIT.conll
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
          if ($i ~ /^B-/) {
              print $i;
              sub(/^B-/, "I-", $i);
              print $i;
          } else if ($i != "O") {
              print $i;
          }
      }
  }' $DATA_LOC/$LANG/train/seq.out | sort | uniq >> $DATA_LOC/$LANG/slot_label.txt
mv  $DATA_LOC/$LANG/valid  $DATA_LOC/$LANG/dev
