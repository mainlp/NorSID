import random
from collections import Counter


entries = []
with open("../data/NoMusic/NorSID/norsid_dev.conll") as f:
    entry = []
    for line in f:
        if not line.strip():
            if entry:
                entries.append(entry)
            entry = []
        else:
            entry.append(line)

random.shuffle(entries)
intents = []
dialects = []
with open("../data/norsid_dev_train.conll", "w+", encoding="utf8") as f:
    for entry in entries[:int(0.9 * len(entries))]:
        for line in entry:
            if line.startswith("# intent"):
                intents.append(line[11:-1])
            elif line.startswith("# dialect"):
                dialects.append(line[12])
            f.write(line)
        f.write("\n")
for item in Counter(intents).most_common():
    print(item[0], item[1])
for item in Counter(dialects).most_common():
    print(item[0], item[1])
intents = []
dialects = []
with open("../data/norsid_dev_dev.conll", "w+", encoding="utf8") as f:
    for entry in entries[int(0.9 * len(entries)):]:
        for line in entry:
            if line.startswith("# intent"):
                intents.append(line[11:-1])
            elif line.startswith("# dialect"):
                dialects.append(line[12])
            f.write(line)
        f.write("\n")
for item in Counter(intents).most_common():
    print(item[0], item[1])
for item in Counter(dialects).most_common():
    print(item[0], item[1])
