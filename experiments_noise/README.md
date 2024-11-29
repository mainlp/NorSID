# SID with noised training data

## Preparations

For adapting MaChAmp to allow loading NorBERT, see the readme in `../experiments_baselines.

Add character-level noise to the machine-translated Norwegian training data. The noised versions will be saved as `../data/b_projectedTrain_noise_{05,10,15,20,25}{a,b,c}.conll` (where the noise levels are 5, 10, 15, 20, or 25%, and a/b/c mark three different random runs).
```
cd code
python noise_data.py
```

Calculate the split word ratios (saved to `results/split_word_ratios.tsv`):
```
python split_word_ratios.py
```

## Finetuning models

```
cd ..  # back to this folder

python3 ../machamp/train.py --dataset_configs configs/data_sidnor10a.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor10 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10b.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor10 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10c.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor10 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20a.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor20 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20b.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor20 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20c.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor20 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30a.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor30 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30b.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor30 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30c.json --parameters_config configs/model_mdeberta.json --device 0 --name mdeberta_sidnor30 --seed 8446

python3 ../machamp/train.py --dataset_configs configs/data_sidnor10a.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor10 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10b.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor10 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10c.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor10 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20a.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor20 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20b.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor20 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20c.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor20 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30a.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor30 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30b.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor30 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30c.json --parameters_config configs/model_scandibert.json --device 0 --name scandibert_sidnor30 --seed 8446

python3 ../machamp/train.py --dataset_configs configs/data_sidnor10a.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor10 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10b.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor10 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor10c.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor10 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20a.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor20 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20b.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor20 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor20c.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor20 --seed 8446
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30a.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor30 --seed 1234
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30b.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor30 --seed 5678
python3 ../machamp/train.py --dataset_configs configs/data_sidnor30c.json --parameters_config configs/model_norbertbase.json --device 0 --name norbert_sidnor30 --seed 8446
```

## Predictions

For each model in `logs`, run:
```
# in the root dir of the repo:
bash ./predict_eval.sh experiments_noise/logs/<SET-UP_NAME>/<TIMESTAMP> <RANDOM_SEED> <SPLIT>
```
This creates three files per run in `predictions/`:
- `<SPLIT>_<SET-UP>_<SEED>.out` (the predictions)
- `<SPLIT>_<SET-UP>_<SEED>.out.eval` (MaChAmp's evaluation)
- `<SPLIT>_<SET-UP>_<SEED>.out.eval.official` (the evaluation produced by the shared task's official script)

## Analysis

Calculate the correlations between the split word ratios and the SID performance:
```
python3 code/ratios_and_sid_results_correlations.py
```
This creates the file `results/ratios_and_sid_results_correlations.tsv`.
