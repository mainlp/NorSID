# Layer Swapping
## Preparations
Run the following scripts to prep the Norwegian and the English data in the JointDeBERTa format.
1. `bash scripts/1_prep_en_data.sh`
2. `bash scripts/1_prep_nor_data.sh` (needed for evaluation)

## Train the EnSID Expert
First, install JointDeBERTa's requirements:
1. `pip install -r JointDeBERTa/requirements.txt` 
Train the EnSID Expert (three seeds) using the JointDeBERTa submodule:
2. `bash scripts/2_train_en_sid.sh`.
Evaluate all checkpoints (for all seeds, 10x3 total) on the NoMusic dev set:
3. `bash scripts/3_eval_all_checkpoints_on_nor_dev.sh`

## Revert Layers of the EnSID Expert
For all three seeds revert layers in pairs of two sequential layers. Set the desired checkpoint for each seed *first* by
changing the values in `SEED_TO_CKPT`.
1. `bash scripts/4_revert_en_sid_models.sh`

## Train the Language Experts (MLM)
All three language experts are trained with train_mlm.py, originally from

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