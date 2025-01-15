from model import JointDeBERTa
from predict import get_device, get_args

def load_model(load_config, model_dir):
    load_config.model_dir = model_dir
    args = get_args(load_config)
    device = get_device(load_config)
    return JointDeBERTa.load_model(model_dir, args, device)
