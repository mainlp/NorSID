# SID baselines

## Preparations

Make the test files MaChAmp-compatible:
```
python3 dataprep/prep_norsid_for_machamp.py
```

### NorBERT3-base

The NorBERT model has non-Huggingface code, which makes loading it more complicated.

Update MaChAmp so NorBERT can be loaded for training: Add kwarg to line 93 of `../machamp/machamp/model/machamp.py`
```
self.mlm = AutoModel.from_pretrained(mlm)
# ->
self.mlm = AutoModel.from_pretrained(mlm, trust_remote_code=True)
```

To allow loading the NorBERT model for predictions:
Inside your `transformers_modules` installation, create the subfolders `ltg/norbert3-base/4376f702588d56cd29276a183582f77345d77a4e/` (or whatever the NorBERT commit you used is) and put the files from https://huggingface.co/ltg/norbert3-base/tree/main inside.

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
# in the root dir of this repo:
bash ./predict_eval.sh experiments_baselines/logs/<SET-UP_NAME>/<TIMESTAMP> <RANDOM_SEED> <SPLIT>
```

For the models trained on 90% of the dialectal development data (= which should only be evaluated on the remaining 10% of the development data), manually re-run the call to the evaluation script afterwards. E.g.,
```
python3 data/NoMusic/NorSID/scripts/sidEval.py experiments_baselines/predictions/dev_dev_norbert_siddial_8446.out data/norsid_dev_dev_machamp.conll > experiments_baselines/predictions/dev_dev_norbert_siddial_8446.out.official.eval 
```
