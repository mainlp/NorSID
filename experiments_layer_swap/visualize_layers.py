import re
import sys
import torch
import logging

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from transformers import DebertaV2ForMaskedLM, XLMRobertaModel

sys.path.insert(0, '../machamp')
sys.path.insert(0, '../../JointBERT')

model_dict = {"ndc": DebertaV2ForMaskedLM,
              "norne": DebertaV2ForMaskedLM,
              "scandi_slot": XLMRobertaModel,
              "scandi_intent": XLMRobertaModel}

title_map = {
    "ndc": "Language Expert (mDeBERTa, NDC)",
    "norne": "Language Expert (mDeBERTa, NORNE)",
    "scandi_slot": "Slot Expert (ScandiBERT)",
    "scandi_intent": "Intent Expert (ScandiBERT)",
    "slot_intent": "Slot/Intent Expert (JointBERT)"
}

output_name_map = {
    "ndc": "lang_expert_ndc.jpg",
    "norne": "lang_expert_norne.jpg",
    "scandi_slot": "slot_expert_scandi.jpg",
    "scandi_intent": "intent_expert_scandi.jpg",
    "slot_intent": "slot_intent_expert.jpg"
}

def load_model(model_location, exp):
    try:
        model = model_dict[exp].from_pretrained(model_location)
    except (EnvironmentError, KeyError):
        model = torch.load(model_location, map_location=torch.device('cpu'))
    return model

def get_model_names(exp, checkpoint_num=-1):
    initial_model_path, best_model_path = None, None
    if exp == "slot_intent":
        if checkpoint_num == -1:
            logging.error(f"Need checkpoint for JointBERT slot/intent expert")
            exit()
        slot_intent_dir = "slot_intent_expert/norsid"
        best_model_path = f"{slot_intent_dir}/model_{checkpoint_num}"
        initial_model_path = f"{slot_intent_dir}/initial_model"
    elif exp in {"ndc", "norne"}:
        if checkpoint_num == -1:
            logging.error(f"Need checkpoint for norne/NDC lang expert")
            exit()
        lang_dir = f"lang_expert/{exp}/models"
        best_model_path = f"{lang_dir}/checkpoint-{checkpoint_num}"
        initial_model_path = f"{lang_dir}/checkpoint-0"
    elif exp.startswith("scandi_"):
        if exp == "scandi_slot":
            best_model_path = "sideng-checkpoint-best.pt"
        elif exp == "scandi_intent":
            best_model_path = "sidnor-checkpoint-best.pt"
        best_model_path = f"lang_expert/scandi/models/{best_model_path}"
        initial_model_path = "vesteinn/ScandiBERT"
    else:
        logging.error(f"Exp type not recognized {exp}")
        exit()
    return initial_model_path, best_model_path


def visualize(best_model_path, initial_model_path, exp):
    best_model = load_model(best_model_path, exp)
    initial_model = load_model(initial_model_path, exp)

    initial_model.eval()
    best_model.eval()

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

    def mean_absolute_diff(weight1, weight2):
        return torch.abs(weight1 - weight2).mean().item()


    if exp == "scandi":
        best_model_encoder = best_model.mlm.encoder
    else:
        best_model_encoder = best_model.deberta.encoder
    for layer_idx, (init_layer, best_layer) in enumerate(zip(initial_model.deberta.encoder.layer,
                                                             best_model_encoder.layer)):
        data['Layer'].append(layer_idx)
        data['attention.wq.weight'].append(mean_absolute_diff(init_layer.attention.self.query_proj.weight,
                                                              best_layer.attention.self.query_proj.weight))
        data['attention.wk.weight'].append(mean_absolute_diff(init_layer.attention.self.key_proj.weight,
                                                              best_layer.attention.self.key_proj.weight))
        data['attention.wv.weight'].append(mean_absolute_diff(init_layer.attention.self.value_proj.weight,
                                                               best_layer.attention.self.value_proj.weight))
        data['attention.wo.weight'].append(mean_absolute_diff(init_layer.attention.output.dense.weight,
                                                              best_layer.attention.output.dense.weight))
        data['feed_forward.w1.weight'].append(mean_absolute_diff(init_layer.intermediate.dense.weight, best_layer.intermediate.dense.weight))
        data['feed_forward.w2.weight'].append(mean_absolute_diff(init_layer.output.dense.weight, best_layer.output.dense.weight))
        data['row_level.MAV'].append(np.mean([data[k][-1] for k in data.keys() if k not in {"Layer", "row_level.MAV"}]))

    df = pd.DataFrame(data).set_index('Layer')
    mask = True
    plt.figure(figsize=(12, 8))

    plt.title(title_map[exp])
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
    output_name = re.sub("\.jpg", "_masked.jpg", output_name_map[exp])
    plt.tight_layout()
    plt.savefig(output_name, format="png", dpi=300)

def main():
    exp = "slot_intent"
    checkpoint = 7
    initial_model_name, best_model_name = get_model_names(exp, checkpoint)
    visualize(initial_model_name, best_model_name, exp)

if __name__ == "__main__":
    main()