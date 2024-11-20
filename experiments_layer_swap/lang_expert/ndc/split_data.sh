mkdir data
awk 'BEGIN {srand(12345)} {r = rand(); if (r < 0.8) {print > "data/train.txt"} else if (r < 0.9) {print > "data/dev.txt"} else {print > "data/test.txt"}}' ../../../data/NordicDialectCorpus/ndc_bokmaal.txt
