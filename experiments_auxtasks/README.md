# SID with dialectal Norwegian auxiliary tasks

## Preparing auxiliary data sets

Download the Nordic Dialect Corpus as described in the main README, then run:
```
python3 dataprep/ndc_prep.py 
```

To get the dialectal transcriptions of the LIA treebank, run:
```
cd ../data/UD_Norwegian-NynorskLIA_dialect
./run.sh
# This creates no_nynorsklia_dialect-ud-{train,dev,test}.conllu in the same folder
cd ../experiments_auxtasks
python3 dataprep/udlia_prep.py
```
This creates the files `../data/UD_LIA_{train,dev}.conll`, which are used for auxiliary tasks (POS tagging, dependency parsing).

Split the NorSID development set to get data for dialect identification:
```
python3 dataprep/split_sid_dev.py
python3 dataprep/conll_to_dialect_only.py
```

Prepare the NorNE (NER) data:
```
python3 dataprep/norne_prep.py
```
This creates the files `../data/norne_{train,dev}.conll`, which contain NorNE-6 labels (GPE as LOC or ORG, no MISC) and a mix of Nynorsk and Bokmål sentences.

## Auxiliary task experiments

Training on English SID data + auxiliary tasks
```
# Dialect ID x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 8446

# Dialect ID -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 8446

# POS x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 8446

# POS -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 8446

# DepRel x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 8446

# DepRel -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sideng.json--parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 8446

# NER x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsid --seed 8446

# NER -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sideng.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sid --seed 8446
```

Training on machine-translated Norwegina SID data + auxiliary tasks
```
# Dialect ID x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsidnor --seed 8446

# Dialect ID -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_dialectid.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sidnor --seed 8446

# POS x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsidnor --seed 8446

# POS -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_pos.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sidnor --seed 8446

# DepRel x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsidnor --seed 8446

# DepRel -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_deprel.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sidnor --seed 8446

# NER x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json configs/data_ner.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_nerxsidnor --seed 8446

# NER -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_ner.json configs/data_sidnor.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_ner_sidnor --seed 8446
```

## Predictions

For each intermediate-task training set-up in `logs`, run:
```
# in the root dir of this repo:
bash ./predict_eval.sh experiments_auxtasks/logs/<SET-UP_NAME>/<TIMESTAMP> <RANDOM_SEED> <SPLIT>
```
This creates three files per run in `predictions/`:
- `<SPLIT>_<SET-UP>_<SEED>.out` (the predictions)
- `<SPLIT>_<SET-UP>_<SEED>.out.eval` (MaChAmp's evaluation)
- `<SPLIT>_<SET-UP>_<SEED>.out.eval.official` (the evaluation produced by the shared task's official script)

For each multitask set-up in `logs`, run:
```
bash ./predict_eval_multitask.sh experiments_auxtasks/logs/<SET-UP_NAME>/<TIMESTAMP> <RANDOM_SEED> <SPLIT>
```
