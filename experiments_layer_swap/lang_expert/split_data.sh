mkdir data
awk 'BEGIN {srand(12345)} {if(rand() < 0.9) {print > "data/train.txt"} else {print > "data/dev.txt"}}' ../../data/NordicDialectCorpus/ndc_bokmaal.txt