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

def classify_message(text):
    """
    Classifies a single message into one of the three SkyGuard categories
    (SOS, MAINTENANCE, SERVICE) using the fine-tuned BERT model.
    Returns the predicted category as a string.
    """

    inputs = tokenizer(text, return_tensor = "pt", truncation = "true", padding = "max_length", max_length = 50)

    inputs_on_device = {}
    for key, value in inputs.items() :
        inputs_on_device[key] = value.to(device)

    inputs = inputs_on_device

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = outputs.logits.argmax(dim = 1).item()

    return id2label[predicted_id]
