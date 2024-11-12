NORNE_DATA_LOC="../../../data/norne/ud/nob"
XSID_SCRIPTS_LOC="../../../data/xsid/scripts"
DATA_LOC="data"
rm -rf $DATA_LOC
mkdir $DATA_LOC

for SPLIT in "train" "dev" "test"
do
  awk '/^# text/ {sub(/^# text = /, ""); print}' $NORNE_DATA_LOC/no_bokmaal-ud-$SPLIT.conllu > $DATA_LOC/$SPLIT.txt
done