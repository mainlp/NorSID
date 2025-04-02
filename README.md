# NorSID

This is the code used by the MaiNLP team in the [VarDial 2025 shared task](https://sites.google.com/view/vardial-2025/shared-tasks) on dialectal Norwegian slot and intent detection. 
It is described in the paper [Add Noise, Tasks, or Layers? A Comparison of Methods to Improve Dialectal Norwegian Slot and Intent Detection](https://aclanthology.org/2025.vardial-1.14/) (Verena Blaschke\*, Felicia Körner\*, Barbara Plank), to be published at VarDial @ COLING 2025.

## Code

Clone with "recursive" flag to download the submodule contents:
`git clone git@github.com:mainlp/NorSID.git --recursive`

Our experiments are described more closely in the respective folders:
- `experiments_baselines`: Compare mDeBERTa-v3, ScandiBERT and NorBERT-v3 when trained on the English training data, its machine-translated counterpart, or 90% of the (predominantly dialectal) development set. This folder also contains some general scripts/notes (making MaChAmp compatible with NorBERT, preparing the 90:10 split of the dev data).
- `experiments_noise`: Inject character-level noise into the MT'ed Norwegian training data and fine-tune the language models on the noised data.
- `experiments_auxtasks`: Train ScandiBERT on another NLP task in (standard or dialectal) Norwegian (POS tagging, dependency parsing, NER, dialect identification), either before training on the English SID training set or simultaneosuly.
- `experiments_layer_swap`: Train models on different datasets and swap out some of their layers (or reset some of their layers).

## Data

Data in submodule folder:
- xSID (regular training/dev/test data for English + other languages)
- NoMusic (shared task dev/test data; MT'ed Norwegian training data)
- UD Nynorsk LIA (treebank with dialectal transcriptions)
- NorNE (named entity annotations for Norwegian)

Data to be additionally downloaded:
- [Nordic Dialect Corpus](https://tekstlab.uio.no/scandiasyn/download.html) ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)): Download the phonetic & orthographic transcriptions with informant codes, unzip them, and add the folders `ndc_phon_with_informant_codes` and `ndc_with_informant_codes` to the `data` directory.

## Citation

```
@inproceedings{blaschke-etal-2025-add,
    title = "Add Noise, Tasks, or Layers? {M}ai{NLP} at the {V}ar{D}ial 2025 Shared Task on {N}orwegian Dialectal Slot and Intent Detection",
    author = {Blaschke, Verena  and
      K{\"o}rner, Felicia  and
      Plank, Barbara},
    editor = "Scherrer, Yves  and
      Jauhiainen, Tommi  and
      Ljube{\v{s}}i{\'c}, Nikola  and
      Nakov, Preslav  and
      Tiedemann, Jorg  and
      Zampieri, Marcos",
    booktitle = "Proceedings of the 12th Workshop on NLP for Similar Languages, Varieties and Dialects",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.vardial-1.14/",
    pages = "182--199",
}
```
