import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from agent.roles import is_allowed
from agent.graph import agent

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

    inputs = tokenizer(text, return_tensors = "pt", truncation = True, padding = "max_length", max_length = 50)

    inputs_on_device = {}
    for key, value in inputs.items() :
        inputs_on_device[key] = value.to(device)

    inputs = inputs_on_device

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = outputs.logits.argmax(dim = 1).item()

    return id2label[predicted_id]


def handle_message(text, role):
    """
    Full pipeline for an incoming message: classifies it, checks whether
    the given role is allowed to access that category, and either returns
    an access-denied response or forwards the message to the agent.
    """
    category = classify_message(text)

    if not is_allowed(role, category):

        return {
            "category" : category,
            "allowed" : False,
            "response" : f"Access denied: your role does not have permission to access {category} requests."
        }

    result = agent.invoke({"messages" : [("user", text)]})

    return {
        "category" : category,
        "allowed" : True,
        "response" : result["messages"][-1].content
    }

if __name__ == "__main__":
    text = "What's the status of flight SK315?"

    category = classify_message(text)
    print("Classified as:", category)

    result = agent.invoke({"messages": [("user", text)]})
    for msg in result["messages"]:
        print(type(msg).__name__, "-", msg.content if hasattr(msg, "content") else msg)