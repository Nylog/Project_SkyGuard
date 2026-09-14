import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from agent.roles import is_allowed
from agent.graph import build_agent

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


def handle_message(text, role, history = None):
    """
    Full pipeline for an incoming message: uses the last couple of user
    messages as context when classifying the current message, checks whether
    the given role is allowed to access that category, and either returns
    an access-denied response or forwards the full conversation history to the agent.
    """

    history = history or []

    # Last 2 user messages before this one, used only to give the classifier
    # a bit of context — not the full history, since BERT was trained on
    # short standalone phrases, not long conversations.
    recent_user_messages = []

    for h in history :
        if h[0] == "user":
            recent_user_messages.append(h[1])

    recent_user_messages = recent_user_messages[-2:]

    classification_input = " ".join(recent_user_messages + [text])


    category = classify_message(classification_input)

    if not is_allowed(role, category):

        return {
            "category" : category,
            "allowed" : False,
            "response" : f"Access denied: your role does not have permission to access {category} requests."
        }

    # The agent, gets the FULL conversation history, since it's a general-purpose LLM well suited to multi-turn context.

    conversation = []

    for h in history:
        conversation.append((h[0], h[1]))

    conversation.append(("user", text))

    agent = build_agent(role)
    result = agent.invoke({"messages" : conversation})

    return {
        "category" : category,
        "allowed" : True,
        "response" : result["messages"][-1].content
    }


# if __name__ == "__main__":
#     text = "What's the status of flight SK315?"

#     category = classify_message(text)
#     print("Classified as:", category)

#     agent = build_agent(role)
#     result = agent.invoke({"messages": [("user", text)]})
#     for msg in result["messages"]:
#         print(type(msg).__name__, "-", msg.content if hasattr(msg, "content") else msg)

# if __name__ == "__main__":
#     print(handle_message("Calculate fuel for flight SK315 with 150 passengers", "admin"))
#     print(handle_message("Calculate fuel for flight SK315 with 150 passengers", "guest"))



# print(classify_message("hi i lost my baggage flight number was SK315"))