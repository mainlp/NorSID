from transformers import AutoTokenizer
from glob import glob


def get_words(filename, col_idx):
    words = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if (not line) or line[0] == "#":
                continue
            word = line.split("\t")[col_idx]
            words.append(word)
    return words


def calculate_ratio(filename, words, tokenizer_name, name2tokenizer):
    tokenizer = name2tokenizer[tokenizer_name]
    n_split = 0
    for word in words:
        subtoks = tokenizer.tokenize(word)
        if len(subtoks) > 1:
            n_split += 1
    split_word_ratio = n_split / len(words)
    print(filename, tokenizer_name, split_word_ratio)
    return filename, tokenizer_name, split_word_ratio


tokenizer_names = ("microsoft/mdeberta-v3-base",
                   "ltg/norbert3-base",
                   "vesteinn/ScandiBERT")
name2tokenizer = {name: AutoTokenizer.from_pretrained(name)
                  for name in tokenizer_names}
with open("../results/split_word_ratios.tsv", "w+") as f_out:
    f_out.write("FILE\tTOKENIZER\tSPLIT WORD RATIO\n")
    for filename in ("../../data/NoMusic/NorSID/norsid_dev.conll",
                     "../../data/NoMusic/NorSID/norsid_test_nolabels.conll",
                     "../../data/NoMusic/NorSID/nb.projectedTrain.conll.fixed"):
        words = get_words(filename, 1)
        for tokenizer_name in tokenizer_names:
            filename, tokenizer_name, split_word_ratio = calculate_ratio(
                filename, words, tokenizer_name, name2tokenizer)
            f_out.write(f"{filename}\t{tokenizer_name}\t{split_word_ratio}\n")
    for filename in glob("../../data/nb_projected*"):
        words = get_words(filename, 1)
        for tokenizer_name in tokenizer_names:
            filename, tokenizer_name, split_word_ratio = calculate_ratio(
                filename, words, tokenizer_name, name2tokenizer)
            f_out.write(f"{filename}\t{tokenizer_name}\t{split_word_ratio}\n")
