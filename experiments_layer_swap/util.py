import torch
import sys

from model import JointDeBERTa
from predict import get_device, get_args

sys.path.insert(0, '../machamp')

def load_model(load_config, model_dir):
    # hacky because we don't know what type of model we're loading (machamp, JointDeBERTa...)
    load_config.model_dir = model_dir
    device = get_device(load_config)
    try:
        args = get_args(load_config)
        return JointDeBERTa.load_model(model_dir, args, device)
    except Exception:
        return torch.load(model_dir, map_location=device)
