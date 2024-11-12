import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import torch
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from transformers import DebertaV2ForMaskedLM


def visualize():
    checkpoint = 2178
    initial_model = DebertaV2ForMaskedLM.from_pretrained("models/checkpoint-0")
    best_model = DebertaV2ForMaskedLM.from_pretrained(f"models/checkpoint-{checkpoint}")

    initial_model.eval()
    best_model.eval()

    data = {
        'Layer': [],
        'attention.wq.weight': [],
        'attention.wk.weight': [],
        'attention.wv.weight': [],
        #'attention.wo.weight': [],
        'feed_forward.w1.weight': [],
        'feed_forward.w2.weight': [],
    }

    def mean_absolute_diff(weight1, weight2):
        return torch.abs(weight1 - weight2).mean().item()

    for layer_idx, (init_layer, best_layer) in enumerate(zip(initial_model.deberta.encoder.layer,
                                                             best_model.deberta.encoder.layer)):
        data['Layer'].append(layer_idx)
        data['attention.wq.weight'].append(mean_absolute_diff(init_layer.attention.self.query_proj.weight,
                                                              best_layer.attention.self.query_proj.weight))
        data['attention.wk.weight'].append(mean_absolute_diff(init_layer.attention.self.key_proj.weight,
                                                              best_layer.attention.self.key_proj.weight))
        data['attention.wv.weight'].append(mean_absolute_diff(init_layer.attention.self.value_proj.weight,
                                                               best_layer.attention.self.value_proj.weight))
        data['feed_forward.w1.weight'].append(mean_absolute_diff(init_layer.intermediate.dense.weight, best_layer.intermediate.dense.weight))
        data['feed_forward.w2.weight'].append(mean_absolute_diff(init_layer.output.dense.weight, best_layer.output.dense.weight))

    df = pd.DataFrame(data).set_index('Layer')
    mask = True
    plt.figure(figsize=(12, 8))
    plt.title("Language Expert")
    if mask:
        mean_diff = df.mean().mean()
        std_diff = df.std().mean()
        threshold = mean_diff + 0.75 * std_diff

        df_colored = df.where(df >= threshold, other=np.nan)

        ax = sns.heatmap(df_colored, annot=False, fmt=".4f", cmap="Greens", linewidths=0.5)

        norm = Normalize(vmin=df_colored.min().min(), vmax=df_colored.max().max())
        cmap = sns.color_palette("Greens", as_cmap=True)

        sm = ScalarMappable(norm=norm, cmap=cmap)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = df.iloc[i, j]
                # gt cell color and calculate brightness
                cell_color = sm.to_rgba(value)
                brightness = 0.299 * cell_color[0] + 0.587 * cell_color[1] + 0.114 * cell_color[2]
                text_color = 'black' if brightness > 0.5 else 'white'
                ax.text(j + 0.5, i + 0.5, f"{value:.4f}", ha='center', va='center', color=text_color)
    else:
        sns.heatmap(df, annot=True, cmap="Greens", linewidths=0.5)
    plt.xlabel("Mean Absolute Difference")
    plt.ylabel("Layer")
    output_name = "lang_expert.png" if not mask else "lang_expert_masked.png"
    plt.tight_layout()
    plt.savefig(output_name, format="png", dpi=300)

def main():
    visualize()

if __name__ == "__main__":
    main()