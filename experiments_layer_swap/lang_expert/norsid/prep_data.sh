NORSID_DATA_LOC="../../../data/NoMusic/NorSID"
DATA_LOC="data"
rm -rf $DATA_LOC
mkdir $DATA_LOC

for SPLIT in "train" "dev"
do
	if [ $SPLIT == "train" ]; then
		FILE="nb.projectedTrain.conll.fixed" 
	else
		FILE="norsid_dev.conll"
	fi
	awk '/^# text/ && !/^# text-en/ {sub(/^# text[ :=]+/, ""); print}' "$NORSID_DATA_LOC/$FILE" > "$DATA_LOC/$SPLIT.txt"
done
