from flask import Blueprint, request, session, jsonify

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agent.router import handle_message

from db.db_utils import get_all_flights

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods = ["POST"])
def chat():
    """
    Receives a chat message from the logged-in user, forwards it to the
    agent pipeline along with the user's role and recent conversation
    history, and returns the response.
    Returns a 401 if no user is currently logged in.
    """

    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401 # ensure the request comes from an authenticated session


    # Extract payload and user role for contextual processing
    data = request.get_json() 
    text = data.get("message")
    role = session["role"]

    history = session.get("history", []) # conversation so far in this session
    
    result = handle_message(text, role, history)


    # Append this turn to the session history, so future messages have context
    history.append(["user", text])
    history.append(["assistant", result["response"]])
    session["history"] = history


    return jsonify(result)