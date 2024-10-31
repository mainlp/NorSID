# SID with noised training data

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

