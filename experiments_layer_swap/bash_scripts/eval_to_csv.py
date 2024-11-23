layer_results = False
with open("results.log", "r") as infile, open("results.csv", "w") as outfile:
    row = ""
    slot = None
    intent = None
    first_col = None
    for line in infile:
        if layer_results:
            if ("predicting with" in line or "evaluating with") and not ".preds" in line:
                if slot is not None and intent is not None:
                    outfile.write(f"{first_col};{slot};{intent}\n")
                    slot = None
                    intent = None
                numbers = line.split("_")
                numbers = [numbers[-3], numbers[-4]]
                first_col = ','.join(numbers)
        else:
            if "sidEval" in line or "evaluating" in line:
                if slot is not None and intent is not None:
                    outfile.write(f"{first_col};{slot};{intent}\n")
                    slot = None
                    intent = None
                if "preds" in line:
                    first_col = line.split("preds")[-2]
                    first_col = first_col[1:-1]
                else:
                    first_col = "/".join(line.strip().split("/")[-2:])
        if "slot f1:" in line and line[0] == "s":
            slot = ";".join((line.split(":")[-1].strip()).split())
        elif "intent accuracy:" in line:
            intent = ";".join((line.split(":")[-1].strip()).split())
    outfile.write(f"{first_col};{slot};{intent}\n")
