from glob import glob


def is_vowel(char):
    return char.lower() in "aeiouyåæø"


def is_consonant(char):
    return not is_vowel(char)


def remove_short_vowel_consonant_cluster(token):
    prev_char = token[0]
    double_cons = False
    offset = 0
    for i, cur_char in enumerate(token):
        if i == 0:
            continue
        if is_consonant(cur_char):
            if cur_char == prev_char:
                double_cons = True
            elif double_cons:
                if not (prev_char in "sk" and cur_char == "j"):
                    token = token[:i - 1 - offset] + token[i - offset:]
                    offset += 1
                double_cons = False
            else:
                double_cons = False
        else:
            double_cons = False
        prev_char = cur_char
    return token


def update_spelling(token):
    # Make the transcription more similar to actual writing.

    # Syllabic consonants, syllable boundaries
    token = token.replace("'", "")

    # Short vowels marked via consonant doubling in
    # ways unlikely to be used in "normal" writing
    token = token.replace("ssjt", "rst")
    token = token.replace("ssjk", "rsk")
    if len(token) > 3 and token not in ["ikkje", "issje"]:
        # NB this catches some false positives
        token = remove_short_vowel_consonant_cluster(token)

    # Retroflex flap: could be either "l" or "rd",
    # but we have many more "l" cases in the NDC data
    token = token.replace("L", "l")

    token = token.replace("_", " ")

    return token


skip_tokens = ['#', '##', '*',  # pauses, overlaps
               # interjections
               'ee', 'eh', 'ehe', 'em', 'heh', 'hm', 'm', 'm-m', 'mhm', 'mm'
               ]
interviewers = ['ms', 'jb', 'ifg', 'rvf', 'sb', 'lks', 'mn', 'sl', 'sr',
                'kb', 'kh', 'iii', 'eo', 'hna', 'ma', 'os', 'as', 'ov',
                'amr', 'ran', 'mi', 'lh', 'mj', 'ahl', 'ks', 'amj', 'cbo',
                'jbj', 'jk', 'bl', 'ta', 'pmk', 'aml', 'amg']
lines = []
for file in glob(
        "../../data/ndc_phon_with_informant_codes/files/norwegian/*.txt"):
    with open(file) as f:
        for line in f:
            speaker, content = line.split(" ", 1)
            if speaker in interviewers:
                # interviewers don't have phono transcriptions
                continue
            tokens_raw = content.strip().split()
            tokens_final = []
            for token in tokens_raw:
                if not token or token in skip_tokens:
                    continue
                # Make the transcription more similar to actual writing.
                token = update_spelling(token)
                tokens_final.append(token)
            if len(tokens_final) < 2:
                continue
            lines.append(" ".join(tokens_final))

print("Writing ndc_dialect.txt")
with open("../../data/ndc_dialect.txt", "w+", encoding="utf8") as f:
    for line in lines:
        f.write(line + "\n")


lines = []
for file in glob("../../data/ndc_with_informant_codes/files/norwegian/*.txt"):
    with open(file) as f:
        for line in f:
            speaker, content = line.split(" ", 1)
            if speaker in interviewers:
                # interviewers don't have phono transcriptions
                continue
            tokens_raw = content.strip().split()
            tokens_final = []
            for token in tokens_raw:
                if not token or token in skip_tokens or token == "e":
                    continue
                token = token.replace("_", " ")
                tokens_final.append(token)
            if len(tokens_final) < 2:
                continue
            lines.append(" ".join(tokens_final))

print("Writing ndc_bokmaal.txt")
with open("../../data/ndc_bokmaal.txt", "w+", encoding="utf8") as f:
    for line in lines:
        f.write(line + "\n")
