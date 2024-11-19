# SID baselines

## Preparations

Make the test files MaChAmp-compatible:
```
python3 dataprep/prep_test_for_machamp.py
```

Update MaChAmp so NorBERT can be loaded: add kwarg to line 93 of `../machamp/machamp/model/machamp.py`
```
self.mlm = AutoModel.from_pretrained(mlm)
# ->
self.mlm = AutoModel.from_pretrained(mlm, trust_remote_code=True)
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

## Predictions

For each model in `logs`, run:
```
python3 ../machamp/predict.py logs/<SET-UP_NAME>/<TIMESTAMP>/model.pt ../data/norsid_test_machamp.conll predictions/<SET-UP_NAME>_<RANDOM_SEED>.out --device 0
```
