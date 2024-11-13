from ndc_prep import update_spelling


def get_entries(in_file, upos=True, ortho=False, verbose=True):
    next_has_phono = False
    n_sents = 0
    dialect2group = {
        "aal": "east",
        "bardu": "east",  # Indre Troms
        "eidsberg": "east",
        "gol": "east",
        "austevoll": "west",
        "farsund": "west",
        "giske": "west",
        "lierne": "troender",
        "flakstad": "north",
        "vardoe": "north",
    }
    group2count = {
        "east": 0,
        "west": 0,
        "troender": 0,
        "north": 0,
    }
    sentences = []
    with open(in_file, encoding="utf8") as f_in:
        cur_sent = []
        cur_group = None
        for line in f_in:
            line = line.strip()
            if not line:
                if cur_sent and cur_sent[-1][0] != "#":
                    # Only include sentences with dialectal data, i.e.
                    # where the last included line isn't just one of the
                    # metadata comments starting with #
                    sentences.append(cur_sent)
                    group2count[cur_group] = group2count[cur_group] + 1
                    next_has_phono = False
                    cur_group = None
                    cur_sent = None
                continue
            if line[0] == "#":
                if line.startswith("# text_orig"):
                    next_has_phono = True
                elif line.startswith("# sent_id"):
                    cur_sent = []
                    cur_sent.append(line)
                    n_sents += 1
                elif line.startswith("# dialect: "):
                    dialect = line[11:].split(" ")[0]
                    cur_group = dialect2group[dialect]
                    cur_sent.append(line)
                    cur_sent.append("# dialect_group = " + cur_group)
                continue
            if not next_has_phono:
                continue
            cells = line.split("\t")
            try:
                if ortho:
                    form = cells[1]
                else:
                    form = None
                    misc_entries = cells[-1].split("|")
                    for entry in misc_entries:
                        if entry.startswith("Phono="):
                            form = entry[6:]
                            break
                    if not form:
                        print("!!! Phonetic information missing:")
                        print(line)
                        print(in_file)
                        print("(exiting)")
                        return
                cells[1] = update_spelling(form)
                cur_sent.append("\t".join(cells))
            except IndexError:
                print("!!! malformed line:")
                print(line)
                print(in_file)
                print("(exiting)")
                return
        if cur_sent and cur_sent[-1][0] != "#":
            sentences.append(cur_sent)
            group2count[cur_group] = group2count[cur_group] + 1
    return sentences, group2count


if __name__ == "__main__":
    input_folder = "../data/UD_Norwegian-NynorskLIA_dialect/"

    for split in ("train", "dev"):
        sentences, group2count = get_entries(
            f"{input_folder}no_nynorsklia_dialect-ud-{split}.conllu")
        print(split, group2count)
        with open(f"../data/UD_LIA_{split}.conll", "w+", encoding="utf8") as f:
            for sentence in sentences:
                for details in sentence:
                    f.write(details + "\n")
                f.write("\n")
