def get_sentences(filename):
    sentence, dialect = None, None
    entries = []
    with open(filename) as f:
        for line in f:
            if line.startswith("# text"):
                sentence = line[9:-1]
            elif line.startswith("# dialect"):
                dialect = line[12:-1]
                if sentence:
                    entries.append((sentence, dialect))
                sentence, dialect = None, None
    return entries


for split in ["train", "dev"]:
    entries = get_sentences(f"../data/norsid_dev_{split}.conll")
    with open(f"../data/norsid_dialects_dev{split}.tsv", "w+") as f:
        for sentence, dialect in entries:
            f.write(f"{sentence}\t{dialect}\n")
