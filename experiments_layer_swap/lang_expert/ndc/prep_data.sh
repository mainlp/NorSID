#!/bin/bash

NDC_DATA_LOC="../../../data/NordicDialectCorpus/"
DATA_LOC="data"
rm -rf $DATA_LOC
mkdir $DATA_LOC

awk 'BEGIN {srand(12345)} {r = rand(); if (r < 0.4) {print > "data/train.txt"} else if (r < 0.45) {print > "data/dev.txt"} else if (r < 0.5) {print > "data/test.txt"}}' $NDC_DATA_LOC/ndc_bokmaal.txt
