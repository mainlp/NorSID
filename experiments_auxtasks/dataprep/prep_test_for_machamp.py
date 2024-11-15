

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
