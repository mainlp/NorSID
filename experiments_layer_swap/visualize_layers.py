import argparse
import sys
import torch

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from util import load_model

sys.path.insert(0, '../machamp')
sys.path.insert(0, '../../JointBERT')

title_map = {
    "ndc": "Language Expert (MLM, NDC)",
    "norne": "Language Expert (MLM, NORNE)",
    "nomusic": "Language Expert (MLM, NoMusic)",
    "slot_intent": "Slot/Intent Expert (JointBERT, xSID en)"
}

def mean_absolute_diff(weight1, weight2):
    return torch.abs(weight2 - weight1).mean().item()

def get_mav(initial_model, finetuned_model):
    data = {
        'Layer': [],
        'attention.wq.weight': [],
        'attention.wk.weight': [],
        'attention.wv.weight': [],
        'attention.wo.weight': [],
        'feed_forward.w1.weight': [],
        'feed_forward.w2.weight': [],
        'row_level.MAV': []
    }

    for layer_idx, (init_layer, best_layer) in enumerate(zip(initial_model.deberta.encoder.layer,
                                                             finetuned_model.deberta.encoder.layer)):
        data['Layer'].append(layer_idx)
        data['attention.wq.weight'].append(mean_absolute_diff(init_layer.attention.self.query_proj.weight,
                                                              best_layer.attention.self.query_proj.weight))
        data['attention.wk.weight'].append(mean_absolute_diff(init_layer.attention.self.key_proj.weight,
                                                              best_layer.attention.self.key_proj.weight))
        data['attention.wv.weight'].append(mean_absolute_diff(init_layer.attention.self.value_proj.weight,
                                                              best_layer.attention.self.value_proj.weight))
        data['attention.wo.weight'].append(mean_absolute_diff(init_layer.attention.output.dense.weight,
                                                              best_layer.attention.output.dense.weight))
        data['feed_forward.w1.weight'].append(
            mean_absolute_diff(init_layer.intermediate.dense.weight, best_layer.intermediate.dense.weight))
        data['feed_forward.w2.weight'].append(
            mean_absolute_diff(init_layer.output.dense.weight, best_layer.output.dense.weight))
        data['row_level.MAV'].append(np.mean([data[k][-1] for k in data.keys() if k not in {"Layer", "row_level.MAV"}]))
    return data

def visualize(data, exp, output):
    df = pd.DataFrame(data).set_index('Layer')
    plt.figure(figsize=(12, 8))
    plt.title(title_map[exp])
    sns.heatmap(df, annot=True, cmap="Greens", linewidths=0.5)
    plt.xlabel("Mean Absolute Difference")
    plt.ylabel("Layer")
    plt.tight_layout()
    plt.savefig(output, format="png", dpi=300)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--initial-model", required=True)
    parser.add_argument("-m", "--finetuned-model", required=True)
    parser.add_argument("-o", "--output", help="Output filepath for the visualization.")
    parser.add_argument("-e", "--exp", choices=list(title_map.keys()), default="slot_intent")
    parser.add_argument("--no-cuda", action="store_true",
                        help="Use this flag to override the use of cuda", default=False)

    args = parser.parse_args()
    if args.output is None:
        args.output = f"{args.exp}_vis.png"
    initial_model = load_model(args.initial_model, args.no_cuda)
    finetuned_model = load_model(args.finetuned_model, args.no_cuda)
    data = get_mav(initial_model, finetuned_model)
    visualize(data, args.exp, args.output)

if __name__ == "__main__":
    main()