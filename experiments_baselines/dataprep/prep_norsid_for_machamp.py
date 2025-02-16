# Version of test set without labels:
# - add placeholders for labels
# - replace = with :
with open("../data/NoMusic/NorSID/norsid_test_nolabels.conll") as f_in:
    with open("../data/norsid_test_nolabels_machamp.conll", "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                f_out.write("\n")
            elif line.startswith("#"):
                line = line.replace(" =", ":")
                if line.startswith("# text"):
                    f_out.write(line + "\n")
                else:
                    f_out.write(line + " PLACEHOLDER\n")
            else:
                f_out.write(line + "\tPLACEHOLDER\tPLACEHOLDER\n")

# Version of test set with labels:
# - replace = with :
with open("../data/NoMusic/NorSID/norsid_test.conll") as f_in:
    with open("../data/norsid_test_machamp.conll", "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                f_out.write("\n")
                continue
            if line.startswith("#"):
                line = line.replace(" =", ":")
            f_out.write(line + "\n")

# Dev set:
# - replace = with :
with open("../data/NoMusic/NorSID/norsid_dev.conll") as f_in:
    with open("../data/norsid_dev_machamp.conll", "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                f_out.write("\n")
                continue
            if line.startswith("#"):
                line = line.replace(" =", ":")
            f_out.write(line + "\n")
