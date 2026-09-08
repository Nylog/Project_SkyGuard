from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from roles import is_allowed
from graph import agent

MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "bert_classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

if  torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model.to(device)
model.eval() # inference mode: disables training-specific behavior like dropout

id2label = model.config.id2label  # loaded automatically, since it was saved during training