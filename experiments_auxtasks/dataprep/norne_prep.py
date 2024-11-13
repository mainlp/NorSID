import sys
import random


def read_norne_file(filename):
    cur_sent = []
    sentences = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                if cur_sent:
                    sentences.append(cur_sent)
                    cur_sent = []
                continue
            if line[0] == "#":
                cur_sent.append(line)
                continue
            cells = line.split("\t")
            word = cells[1]
            ne = None
            for misc in cells[9].split("|"):
                if misc.startswith("name="):
                    ne = misc[5:]
                    break
            if not ne:
                print("!!")
                print("NE annotation missing")
                print(cur_sent)
                sys.exit(1)
            # Using NorNE-6 labels:
            # - no MISC (which only appear a handful of times)
            # - GPE_ORG is merged with ORG, GPE_LOC with LOC
            if ne.endswith("MISC"):
                ne = "O"
            elif ne.endswith("GPE_ORG"):
                ne = ne[0] + "-ORG"
            elif ne.endswith("GPE_LOC"):
                ne = ne[0] + "-LOC"
            cur_sent.append(word + "\t" + ne)
        if cur_sent:
            sentences.append(cur_sent)
    return sentences


nno_train = read_norne_file("../data/norne/ud/nno/no_nynorsk-ud-train.conllu")
nno_dev = read_norne_file("../data/norne/ud/nno/no_nynorsk-ud-dev.conllu")
nob_train = read_norne_file("../data/norne/ud/nob/no_bokmaal-ud-train.conllu")
nob_dev = read_norne_file("../data/norne/ud/nob/no_bokmaal-ud-dev.conllu")

print("NNO train", len(nno_train))
print("NNO dev", len(nno_dev))
print("NOB train", len(nob_train))
print("NOB dev", len(nob_dev))

train = nno_train + nob_train
random.shuffle(train)
dev = nno_dev + nob_dev
random.shuffle(dev)

with open("../data/norne_train.conll", "w+", encoding="utf8") as f:
    for sentence in train:
        for line in sentence:
            f.write(line + "\n")
        f.write("\n")
with open("../data/norne_dev.conll", "w+", encoding="utf8") as f:
    for sentence in dev:
        for line in sentence:
            f.write(line + "\n")
        f.write("\n")
