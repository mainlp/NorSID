cd nor || exit
rasa test nlu --nlu ./tests/test_nlu.yml --out results-nor
cd ../en || exit
rasa test nlu --nlu ../nor/tests/test_nlu.yml --out results-0-shot
cd ../bert-multiling-en || exit
rasa test nlu --nlu ../nor/tests/test_nlu.yml --out results-0-shot