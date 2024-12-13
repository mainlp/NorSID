import torch
import sys
from transformers import DebertaV2ForMaskedLM

sys.path.insert(0, "../../JointBERT")
sys.path.insert(0, "../machamp")

def load_model(model_location, no_cuda=False):
    try:
        model = DebertaV2ForMaskedLM.from_pretrained(model_location)
    except (EnvironmentError, KeyError):
        model = torch.load(model_location, map_location=get_device(no_cuda))
    model.eval()
    return model

def get_device(no_cuda=False):
    return torch.device("cuda" if torch.cuda.is_available() and not no_cuda else "cpu")
