# Layer Swapping
**NOTE** these scripts do not create a log, however in most cases (training, evaluation) a logfile is useful.
A quick and dirty way to log the system output to a file is to run the commands with 
`nohup bash <script_name> > <log_name>`, e.g. `nohup bash scripts/5_eval_all_reverted.sh > logs/eval.log`

## Preparations
Run the following scripts to prep the Norwegian and the English data in the JointDeBERTa format.
1. `bash scripts/1_prep_en_data.sh`
2. `bash scripts/1_prep_nor_data.sh` (needed for evaluation)

## Train the EnSID Expert
First, install JointDeBERTa's requirements:
1. `pip install -r JointDeBERTa/requirements.txt`
Then install JointDeBERTa itself in editable mode:
2. `pip install -e JointDeBERTa`
Train the EnSID Expert (three seeds) using the JointDeBERTa submodule:
3. `bash scripts/2_train_en_sid.sh`.
Evaluate all checkpoints (for all seeds, 10x3=30 total) on the NoMusic dev set:
4. `bash scripts/3_eval_all_checkpoints_on_nor_dev.sh`

## Revert Layers of the EnSID Expert
For all three seeds revert layers in pairs of two sequential layers. Set the desired checkpoint for each seed *first* by
changing the values in `SEED_TO_CKPT`:
1. `bash scripts/4_revert_en_sid_models.sh`
Evaluate all reverted models (for all seeds, 11x3=33 total) on the NoMusic dev set:
2. `bash scripts/5_eval_all_reverted.sh`

## Swap Layers of the EnSID Experts with those of SidDial Baseline
First, you must train the SidDial models, following instructions in experiments_baselines. Like when reverting, set the 
desired checkpoints per seed by changing the values in `SEED_TO_CKPT`
1. `bash scripts/6_swap_seeded_models.sh`

## Run SidEval on predictions
There are two ways to evaluate most of the models. JointDeBERTa can be evaluated using `main.py` with the  `--do_eval`
flag. This is quicker, and somewhat easier than using the SidEval script from the Shared Task. See an example 
here: `scripts/3_eval_all_checkpoints_on_nor_dev.sh`. However, the results will be slightly different than if the 
script is used. To use the script, first get predictions (see `scripts/7_get_all_swapped_preds` for an example), then 
run the SidEval script. It is somewhat brittle, in that it will calculate very bad scores when compared to the Norwegian
dev data since there is an empty entry at 289/1, which is not output by JointDeBERTa when making predictions. It will 
also fail when evaluated on English data, as this doesn't contain dialect information. To prepare the files for SidEval:
1. Add an empty entry to the Norwegian dev predictions at 289/1 (after 253/4):
```
# id = 289/1
# text =
# intent = SearchCreativeWork
# dialect = N
1      SearchCreativeWork O
```
2. Add fake dialect entries to the English gold data, e.g.:
```
# text = show all reminders
# intent = reminder/show_reminders
# slots: 5:8:reminder/reference,9:18:reminder/noun
# dialect = B
1	show	reminder/show_reminders	O
2	all	reminder/show_reminders	B-reference
3	reminders	reminder/show_reminders	O
```
You can get the swapped predictions on dev and test for English and Norwegian by running
1. `bash scripts/7_get_all_swapped_preds.sh`
Similarly, the baseline predictions on dev and test for English and Norwegian:
2. `bash scripts/8_get_all_baseline_preds.sh`

`scripts/9_run_sidEval_on_en_preds.sh` and `scripts/10_run_sidEval_on_preds.sh` will run the sid eval script on these 
predictions.

## Train the Language Experts (MLM)
All three language experts are trained with train_mlm.py, from Hugging Face Sentence Transformers.

### NorSID
This model uses data prepared in the `Preparations` step above.
1. `cd lang_expert/norsid`
2. `bash train.sh`
3. `bash eval.sh`

### NDC
This model uses half of the Nordic Dialect Corpus. Run the following scripts to prepare the data, train the model, and 
evaluate the checkpoints.
1. `cd lang_expert/ndc`
2. `bash prep_data.sh`
3. `bash train.sh`
4. `bash eval.sh`

### NorNE
This model uses the NorNe Corpus. Run the following scripts to prepare the data, train the model, and 
evaluate the checkpoints.
1. `cd lang_expert/norne`
2. `bash prep_data.sh`
3. `bash train.sh`
4. `bash eval.sh`
