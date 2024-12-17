# Layer Swapping
## Preparations
Run the following scripts to prep the Norwegian and the English data in the JointDeBERTa format.
1. `bash scripts/1_prep_data.sh`
2. `bash scripts/1_prep_nor_data.sh`

## Training the EnSID Expert
Run this script to train the EnSID Expert using the JointDeBERTa submodule.
1. `bash scripts/2_train_en_sid.sh`
