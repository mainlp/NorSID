# SID with dialectal Norwegian auxiliary tasks

## Baselines

```
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sideng --seed 8446
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor --seed 8446

python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sideng --seed 8446
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor --seed 8446

python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sideng.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sideng --seed 8446
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 1234
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 5678
python3 machamp/train.py --dataset_configs configs/data_sidnor.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor --seed 8446
```

## other notes

Change to Machamp: line 93 of machamp/machamp/model/machamp.py: added kwarg to allow loading norbert
```
self.mlm = AutoModel.from_pretrained(mlm)
# ->
self.mlm = AutoModel.from_pretrained(mlm, trust_remote_code=True)
```

dev set: fixed slots
