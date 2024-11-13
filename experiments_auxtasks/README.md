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
```

Split the NorSID development set to get data for dialect identification:
```
python3 dataprep/split_sid_dev.py
```

## Baselines

```
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_siddial --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_siddial --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_siddial --seed 8446

python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_siddial --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_siddial --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_siddial --seed 8446

python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_siddial --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_siddial --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_siddial.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_siddial --seed 8446
```

## Auxiliary task experiments

```
# Dialect ID x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_idxsid --seed 8446

# Dialect ID -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_dialectid.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_id_sid --seed 8446

# POS x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_posxsid --seed 8446

# POS -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_pos.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_pos_sid --seed 8446

# DepRel x SID: Joint multi-task learning
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_deprelxsid --seed 8446

# DepRel -> SID: Intermediate-task training
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sideng.json configs/data_deprel.json --parameters_config configs/model_scandibert.json --sequential --device 0 --name scandibert_deprel_sid --seed 8446

```

## other notes

Change to Machamp: line 93 of machamp/machamp/model/machamp.py: added kwarg to allow loading norbert
```
self.mlm = AutoModel.from_pretrained(mlm)
# ->
self.mlm = AutoModel.from_pretrained(mlm, trust_remote_code=True)
```

dev set: fixed slots
