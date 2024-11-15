import sys
import torch
from itertools import combinations
from transformers import DebertaV2ForMaskedLM

sys.path.insert(0, '../../JointBERT')

def swap_layers(layers_to_swap):
    local = False
    device = "cpu" if local else "cuda:0"
    lang_dir = "lang_expert/ndc/models" if local else "/nfs/gdata/fkoerner/ndc0.5_lang_exps"
    slot_intent_dir = "slot_intent_expert/models/norsid" if local else "/nfs/gdata/fkoerner/norsid_mdeberta_model"
    lang_expert = DebertaV2ForMaskedLM.from_pretrained(f"{lang_dir}/checkpoint-2178")
    lang_expert.to(device)
    slot_intent_expert = torch.load(f"{slot_intent_dir}/model_7", map_location=device)
    w_task = 0.5
    w_lang = 0.5
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
    torch.save(slot_intent_expert, f"/nfs/gdata/fkoerner/swapped_models/merged_model_7_{''.join([str(l) for l in layers_to_swap])}_w{w_task}_{w_lang}")


def main():
    layers = [i for i in range(6)]
    combinations_layers_to_swap = combinations(layers, 2)
    contiguous = [l for l in combinations_layers_to_swap if l[1] == (l[0] + 1)]
    contiguous = [[0, 1]]
    for layers_to_swap in contiguous:
        swap_layers(layers_to_swap)

if __name__ == '__main__':
    main()
