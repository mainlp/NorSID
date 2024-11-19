# SID with noised training data

Add character-level noise to the machine-translated Norwegian training data. The noised versions will be saved as `../data/b_projectedTrain_noise_{05,10,15,20,25}{a,b,c}.conll` (where the noise levels are 5, 10, 15, 20, or 25%, and a/b/c mark three different random runs).
```
cd code
python noise_data.py
```

Calculate the split word ratios (saved to `results/split_word_ratios.tsv`):
```
python split_word_ratios.py
```

The 0% noise option turned out to be best for mDeBERTa (this is already implemented as a baseline for experiments_auxtasks) and 20% for NorBERT and ScandiBERT. Train these two on the 20% noised data:
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
python3 ../machamp/predict.py logs/<SET-UP_NAME>/<TIMESTAMP>/model.pt ../data/norsid_test_machamp.conll predictions/<SET-UP_NAME>_<RANDOM_SEED>.out --device 0
```

--

```
cd datasets/UD_Norwegian-NynorskLIA_dialect
./run.sh
cd ../..
python3 A_prep_lia.py  # via https://github.com/mainlp/noisydialect/tree/main
```

Hyperparameter grid search...

Determine noise levels; https://github.com/mainlp/noisydialect/tree/main
```
python3 B_data-matrix_prep.py ../configs/B_nob-full_nob-west_norbert_orig.cfg
python3 C_run.py -c ../configs/C_ancoraspa-full_ancoraspa-rpic_beto_${noise}.cfg --test_per_epoch --save_model
python3 D_data_stats.py "../results/C_${train_data}*" ../results/stats-${train_data}.tsv
```

