import torch
import argparse
from transformers import DebertaV2ForMaskedLM
import logging
from util import load_model

logging.basicConfig(level=logging.DEBUG)

def swap_layers(base_model, swap_in, args):
    w_task, w_lang = args.weighting
    state_dict = {}
    swap_in_encoder = swap_in.mlm if hasattr(swap_in, "mlm") else swap_in.deberta
    base_model_encoder = base_model.mlm if hasattr(base_model, "mlm") else base_model.deberta

    # TODO make generic
    swap_in_encoder.resize_token_embeddings(250102)

    for index, ((name, swap_in_param), (name, base_model_param)) in enumerate(zip(swap_in_encoder.named_parameters(),
                                                                              base_model_encoder.named_parameters())):
        layer_num = int(name.split(".")[2]) if "layer." in name else -1
        if layer_num in args.layers_to_swap or name.startswith("embeddings"):
            # use the language expert layers or revert
            state_dict[name] = swap_in_param
            logging.info(f"Swapping in {name} from {args.swap_in}" if not args.revert else f"Reverting {name}")
        elif (layer_num > 0 or args.revert or
              name.startswith("encoder.LayerNorm") or name.startswith("encoder.rel_embeddings")):
            # keep the original layers
            state_dict[name] = base_model_param
            logging.info(f"Keeping {name} layer from {args.base_model}")
        else:
            # non-FFN, non-attention layer
            # merge the parameters
            logging.info(f"Merging {name} with weighting {w_task} (base_model) {w_lang} (swap_in)")
            state_dict[name] = (w_task * base_model_param + w_lang * swap_in_param) / (w_task + w_lang)

    if hasattr(base_model, "deberta"):
        base_model.deberta.load_state_dict(state_dict)
    else:
        base_model.mlm.load_state_dict(state_dict)
    return base_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--base-model", required=True)
    parser.add_argument("-s", "--swap-in")
    parser.add_argument("-l", "--local", action="store_true")
    parser.add_argument("-r", "--revert", action="store_true")
    parser.add_argument("-n", "--layers-to-swap", nargs="+", default = [0, 1])
    parser.add_argument("-w", "--weighting", nargs=2, default=[0, 1])
    parser.add_argument("-o", "--output", help="Where to store the model", required=True)
    parser.add_argument("--no-cuda", action="store_true",
                        help="Use this flag to override the use of cuda", default=False)

    args = parser.parse_args()

    if args.revert:
        swap_in = DebertaV2ForMaskedLM.from_pretrained("microsoft/mdeberta-v3-base")
    elif args.swap_in:
        swap_in = load_model(args.swap_in, args.no_cuda)
    else:
        raise ValueError("Either choose to revert (-r) or specify a model to swap in (-s).")

    args.layers_to_swap = [int(l) for l in args.layers_to_swap]
    base_model = load_model(args.base_model, args.no_cuda)
    assembled_model = swap_layers(base_model, swap_in, args)
    torch.save(assembled_model, args.output)

if __name__ == "__main__":
    main()
