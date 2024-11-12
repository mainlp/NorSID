cd nor || exit
rasa test nlu --nlu data/nlu.yml --out results-train
cd ../en || exit
rasa test nlu --nlu data/nlu.yml --out results-train
cd ../bert-multiling-en || exit
rasa test nlu --nlu ../en/data/nlu.yml --out results-train