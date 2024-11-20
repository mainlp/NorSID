import re
with open("eval_swapped_test.txt", "r") as infile, open("eval_swapped_test.csv", "w") as outfile:
    row = ""
    slot = None
    intent = None
    for line in infile:
        if "predicting with" in line and not ".preds" in line:
            if slot is not None and intent is not None:
                outfile.write(f"{','.join(numbers)};{slot};{intent}\n")
                slot = None
                intent = None
            numbers = line.split("_")
            numbers = [numbers[-3], numbers[-4]]
        elif "slot" in line:
            slot = line.split(":")[-1].strip()
        elif "intent" in line:
            intent = line.split(":")[-1].strip()
    outfile.write(f"{','.join(numbers)};{slot};{intent}\n")
