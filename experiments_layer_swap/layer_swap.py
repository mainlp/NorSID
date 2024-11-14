import sys
import torch
from itertools import combinations
from transformers import DebertaV2ForMaskedLM

sys.path.insert(0, '../../JointBERT')

def swap_layers(layers_to_swap):
    lang_expert = DebertaV2ForMaskedLM.from_pretrained("lang_expert/ndc/models/checkpoint-0")
    slot_intent_expert = torch.load("slot_intent_expert/norsid/model_7", map_location=torch.device('cpu'))
    w_task = 1
    w_lang = 0
    state_dict = {}
    for index, ((name, lang_param), (name, slot_intent_param)) in enumerate(zip(lang_expert.deberta.named_parameters(),
                                                                              slot_intent_expert.deberta.named_parameters())):
        if "layer." in name:
            layer_num = int(name.split('.')[2])
        else:
            layer_num = -1
        if layer_num in layers_to_swap:
            # use the language expert layers
            state_dict[name] = lang_param
        elif layer_num > 0:
            # keep the original layers
            state_dict[name] = slot_intent_param
        else:
            # merge the parameters
            state_dict[name] = (w_task * slot_intent_param + w_lang * lang_param) / (w_task + w_lang)
    slot_intent_expert.deberta.load_state_dict(state_dict)
    torch.save(slot_intent_expert, f"merged_model_7_{''.join([str(l) for l in layers_to_swap])}_w{w_task}_{w_lang}")


def main():
    layers = [i for i in range(12)]
    combinations_layers_to_swap = combinations(layers, 3)
    contiguous = [l for l in combinations_layers_to_swap if l[1] == (l[0] + 1) and l[2] == (l[1] + 1)]
    for layers_to_swap in contiguous:
        swap_layers(layers_to_swap)

if __name__ == '__main__':
    main()
