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

