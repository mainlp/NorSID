import sys
import torch
import argparse
from transformers import DebertaV2ForMaskedLM
import logging

logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, '../../JointBERT')
sys.path.insert(0, '../machamp')

def get_model_id(model_name):
    model_id = model_name.split('/')[-1]
    if model_id == "model.pt":
        model_id = model_name.split('/')[-2]
    elif model_id.startswith("model_"):
        model_id = f"{model_name.split('/')[-2]}_{model_name.split('/')[-1]}"
    return model_id

def swap_layers(layers_to_swap, weighting, base, swap_in, local=False, revert=False):
    device = "cpu" if local else "cuda:0"

    if revert:
        model_to_swap_in = DebertaV2ForMaskedLM.from_pretrained("microsoft/mdeberta-v3-base")
    else:
        try:
            model_to_swap_in = DebertaV2ForMaskedLM.from_pretrained(swap_in)
        except:
            model_to_swap_in = torch.load(swap_in, map_location=device)
        model_to_swap_in.to(device)

    base_model = torch.load(base, map_location=device)
    w_task = weighting[0]
    w_lang = weighting[1]
    state_dict = {}

    model_to_swap_in_encoder = model_to_swap_in.mlm if hasattr(model_to_swap_in, 'mlm') else model_to_swap_in.deberta
    base_model_encoder = base_model.mlm if hasattr(base_model, 'mlm') else base_model.deberta
    model_to_swap_in_encoder.resize_token_embeddings(250102)

    for index, ((name, swap_in_param), (name, base_model_param)) in enumerate(zip(model_to_swap_in_encoder.named_parameters(),
                                                                              base_model_encoder.named_parameters())):
        if "layer." in name:
            layer_num = int(name.split('.')[2])
        else:
            layer_num = -1
        if layer_num in layers_to_swap:# or "embedding" in name:#(revert and "embedding" in name):
            # use the language expert layers
            state_dict[name] = swap_in_param
            logging.info(f"Swapping in {name} from {swap_in}")
        elif layer_num > 0 or revert:# or "LayerNorm" in name:# (revert and "LayerNorm" in name):
            # keep the original layers
            state_dict[name] = base_model_param
        else:
            # non-FFN or attention layer
            # merge the parameters
            logging.info(f"Merging {name} with weighting {w_task} (base_model) {w_lang} (swap_in)")
            state_dict[name] = (w_task * base_model_param + w_lang * swap_in_param) / (w_task + w_lang)

    base_model.deberta.load_state_dict(state_dict) if hasattr(base_model, 'deberta') else base_model.mlm.load_state_dict(state_dict)

    mode = "reverted" if revert else "swapped"
    dir_save_to = "models" if local else f"/nfs/gdata/fkoerner/{mode}_models"
    models = get_model_id(base)
    if not revert:
        models = f"{models}_{get_model_id(swap_in)}"
    torch.save(base_model, f"{dir_save_to}/{mode}_{models}_{'_'.join([str(l) for l in layers_to_swap])}_w{w_task}_{w_lang}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base-model", required=True)
    parser.add_argument("-s", "--swap-in")
    parser.add_argument("-l", "--local", action="store_true")
    parser.add_argument("-r", "--revert", action="store_true")
    parser.add_argument("-n", "--layers-to-swap", nargs="+")
    parser.add_argument("-w", "--weighting", nargs=2, default=[0, 1])

    args = parser.parse_args()
    if not args.swap_in and not args.revert:
        logging.error(f"Either choose to revert")
    layers_to_swap = [0, 1] if not args.layers_to_swap else args.layers_to_swap
    layers_to_swap = [int(l) for l in layers_to_swap]
    swap_layers(layers_to_swap, args.weighting, args.base_model, args.swap_in, args.local, args.revert)

if __name__ == '__main__':
    main()
