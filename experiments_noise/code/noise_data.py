import random


def alphabet(filename, col_idx):
    words = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if (not line) or line[0] == "#":
                continue
            word = line.split("\t")[col_idx]
            words.append(word)
    return list({c for word in words for c in word if c.isalpha()})


def noisy_indices(sent_toks, percentage_noisy):
    # Only include words with alphabetic content.
    poss_indices = [i for i, tok in enumerate(sent_toks)
                    if any(c.isalpha() for c in tok)]
    idx_noisy = random.sample(
        poss_indices, k=round(percentage_noisy * len(poss_indices)))
    return idx_noisy


def add_char(word, alphabet):
    idx = random.randrange(-1, len(word))
    if idx == -1:
        return random.sample(alphabet, 1)[0] + word
    return word[:idx + 1] + random.sample(alphabet, 1)[0] + word[idx + 1:]


def delete_char(word):
    idx = random.randrange(len(word))
    return word[:idx] + word[idx + 1:]


def replace_char(word, alphabet, idx=-1):
    if idx < 0:
        idx = random.randrange(len(word))
    return word[:idx] + random.sample(alphabet, 1)[0] + word[idx + 1:]


def add_random_noise(words, noise_lvl, alphabet,
                     noise=("add_char", "delete_char", "replace_char")):
    n_changed = 0
    idx_noisy = sorted(noisy_indices(words, noise_lvl))
    words_noisy = []
    for i, word in enumerate(words):
        if i in idx_noisy:
            noise_type = random.choice(noise)
            if noise_type == "add_char":
                word_noised = add_char(word, alphabet)
            elif noise_type == "delete_char":
                word_noised = delete_char(word)
            elif noise_type == "replace_char":
                word_noised = replace_char(word, alphabet)
            else:
                print("Noise " + noise_type + " not recognized.")
                word_noised = word
            words_noisy.append(word_noised)
            n_changed += 1
    return idx_noisy, words_noisy


in_data = "../../data/NoMusic/NorSID/nb.projectedTrain.conll.fixed"
alphabet = alphabet(in_data, 1)

for noise_lvl in [0.05, 0.10, 0.15, 0.20, 0.25]:
    for random_run in ["a", "b", "c"]:
        lines = []
        with open(in_data) as f_in:
            sentence = []
            for line in f_in:
                if line[0] == "#":
                    lines.append(line)
                    sentence = []
                elif not line.strip():
                    if sentence:
                        words = [token_details[1]
                                 for token_details in sentence]
                        idx_noisy, words_noisy = add_random_noise(
                            words, noise_lvl, alphabet)
                        for i, word in zip(idx_noisy, words_noisy):
                            sentence[i][1] = word
                        for token_details in sentence:
                            lines.append("\t".join(token_details))
                    sentence = []
                    lines.append(line)
                else:
                    sentence.append(line.split("\t"))
        with open(
                f"../../data/nb_projectedTrain_noise_{int(noise_lvl * 100):02d}{random_run}.conll",
                "w+") as f_out:
            for line in lines:
                f_out.write(line)
