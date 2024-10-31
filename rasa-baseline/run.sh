#!/bin/sh
mkdir -p en/data
mkdir en/tests
mkdir -p nor/data
mkdir nor/tests
python convert_data.py
cp config.yml en
cp config.yml nor
cd en || exit
rasa train nlu --nlu data
rasa test nlu --nlu tests
cd ../nor || exit
rasa train nlu --nlu data
rasa test nlu --nlu tests
