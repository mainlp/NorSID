from scipy.stats import pearsonr, spearmanr


model2split_ratios_dev, model2split_ratios_test = {}, {}
model2intents_dev, model2intents_test = {}, {}
model2slots_dev, model2slots_test = {}, {}
with open("../results/ratios_and_sid_results.tsv") as f:
    first_line = True
    for line in f:
        if first_line:
            # skip first line
            first_line = False
            continue
        line = line.strip()
        if not line:
            continue
        cells = line.split("\t")
        model = cells[0]
        if model not in model2split_ratios_dev:
            model2split_ratios_dev[model] = []
            model2split_ratios_test[model] = []
            model2intents_dev[model] = []
            model2intents_test[model] = []
            model2slots_dev[model] = []
            model2slots_test[model] = []
        model2split_ratios_dev[model].append(float(cells[2]))
        model2split_ratios_test[model].append(float(cells[5]))
        model2intents_dev[model].append(float(cells[3]))
        model2intents_test[model].append(float(cells[6]))
        model2slots_dev[model].append(float(cells[4]))
        model2slots_test[model].append(float(cells[7]))


with open("../results/ratios_and_sid_results_correlations.tsv", "w") as f:
    f.write("model\tintents_pearson\tintents_pearson_pval\tintents_spearman\tintents_spearman_pval\t")
    f.write("slots_pearson\tslots_pearson_pval\tslots_spearman\tslots_spearman_pval\n")
    for model in model2split_ratios_dev:
        f.write(model + " dev\t")
        split_ratios_dev = model2split_ratios_dev[model]
        intents_dev = model2intents_dev[model]
        slots_dev = model2slots_dev[model]
        split_ratios_test = model2split_ratios_test[model]
        intents_test = model2intents_test[model]
        slots_test = model2slots_test[model]
        pearson = pearsonr(split_ratios_dev, intents_dev)
        spearman = spearmanr(split_ratios_dev, intents_dev)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\t")
        pearson = pearsonr(split_ratios_dev, slots_dev)
        spearman = spearmanr(split_ratios_dev, slots_dev)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\n")
        f.write(model + " test\t")
        pearson = pearsonr(split_ratios_test, intents_test)
        spearman = spearmanr(split_ratios_test, intents_test)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\t")
        pearson = pearsonr(split_ratios_test, slots_test)
        spearman = spearmanr(split_ratios_test, slots_test)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\n")
        f.write(model + " dev+test\t")
        pearson = pearsonr(split_ratios_dev + split_ratios_test, intents_dev + intents_test)
        spearman = spearmanr(split_ratios_dev + split_ratios_test, intents_dev + intents_test)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\t")
        pearson = pearsonr(split_ratios_dev + split_ratios_test, slots_dev + slots_test)
        spearman = spearmanr(split_ratios_dev + split_ratios_test, slots_dev + slots_test)
        f.write(f"{pearson.statistic:.2f}\t{pearson.pvalue:.2f}\t")
        f.write(f"{spearman.statistic:.2f}\t{spearman.pvalue:.2f}\n")
