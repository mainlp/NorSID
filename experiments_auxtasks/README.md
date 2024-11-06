# SID with dialectal Norwegian auxiliary tasks

## Baselines

```
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta_1234.json --device 0 --name mdeberta_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta_5678.json --device 0 --name mdeberta_sideng
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta_8446.json --device 0 --name mdeberta_sideng
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta_1234.json --device 0 --name mdeberta_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta_5678.json --device 0 --name mdeberta_sidnor
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta_8446.json --device 0 --name mdeberta_sidnor

python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert_1234.json --device 0 --name scandibert_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert_5678.json --device 0 --name scandibert_sideng
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert_8446.json --device 0 --name scandibert_sideng
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert_1234.json --device 0 --name scandibert_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert_5678.json --device 0 --name scandibert_sidnor
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert_8446.json --device 0 --name scandibert_sidnor

python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase_1234.json --device 0 --name norbert_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase_5678.json --device 0 --name norbert_sideng
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase_8446.json --device 0 --name norbert_sideng
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase_1234.json --device 0 --name norbert_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase_5678.json --device 0 --name norbert_sidnor
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase_8446.json --device 0 --name norbert_sidnor
```

## other notes

Change to Machamp: line 93 of machamp/machamp/model/machamp.py: added kwarg to allow loading norbert
```
self.mlm = AutoModel.from_pretrained(mlm)
# ->
self.mlm = AutoModel.from_pretrained(mlm, trust_remote_code=True)
```

dev set: fixed slots
