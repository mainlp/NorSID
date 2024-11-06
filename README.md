# NorSID

VarDial 2025 shared task: https://sites.google.com/view/vardial-2025/shared-tasks

Data in submodule folder:
- xSID (regular training/dev/test data for English + other languages)
- NoMusic (shared task dev data; MTed Norwegian training data)
- UD Nynorsk LIA (treebank with dialectal transcriptions)

Clone with "recursive" flag to download the submodule contents:
`git clone git@github.com:mainlp/NorSID.git --recursive`

## Data

Download additional data sets:
- [Nordic Dialect Corpus](https://tekstlab.uio.no/scandiasyn/download.html) ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)): Download the phonetic & orthographic transcriptions with informant codes, unzip them, and add the folders `ndc_phon_with_informant_codes` and `ndc_with_informant_codes` to the `data` directory.
