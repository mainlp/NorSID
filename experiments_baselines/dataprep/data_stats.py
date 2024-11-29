from collections import Counter


def stats(filename):
    intents = []
    slots_bio = []
    slots_types = []
    dialects = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("# intent"):
                intent = line.split()[-1]
                intents.append(intent)
                continue
            if line.startswith("# dialect"):
                dialect = line.split()[-1]
                dialects.append(dialect)
                continue
            if line[0] == "#":
                continue
            slot = line.split()[-1]
            if slot == "O":
                continue
            slots_bio.append(slot)
            if slot[0] == "B":
                slots_types.append(slot[2:])
    print(filename)
    print()
    counter = Counter(dialects)
    for dialect in sorted(counter):
        print(dialect, counter[dialect])
    print()
    counter = Counter(intents)
    for intent in sorted(counter):
        print(intent, counter[intent])
    print()
    counter = Counter(slots_types)
    for slot_type in sorted(counter):
        print(slot_type, counter[slot_type])
    print()
    counter = Counter(slots_bio)
    for slot_bio in sorted(counter):
        print(slot_bio, counter[slot_bio])
    print()
    print()


for filename in [
        "../data/NoMusic/NorSID/nb.projectedTrain.conll.fixed",
        "../data/xsid/data/xSID-0.6/en.train.conll",
        "../data/NoMusic/NorSID/norsid_dev.conll",
        "../data/NoMusic/NorSID/norsid_test.conll",
        "../data/norsid_dev_dev_machamp.conll",
        "../data/norsid_dev_train_machamp.conll"]:
    stats(filename)
