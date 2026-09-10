from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.db_utils import get_user_by_username



auth_bp = Blueprint("auth", __name__)  # Authentication blueprint to decouple auth routes from the main app.py


@auth_bp.route("/login", methods = ["POST"])
def login():
    """
    Verifies the submitted username and password against the database.

    On success, stores the user's username and role in the session and
    returns a json object containing the success status and user's role.
    On failure, returns a json object indicating invalid credentials.
    """
    
    data = request.get_json()  # parse the incoming JSON body (expects {"username": ..., "password": ...}
    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username) # look up the user in the database

    # check_password_hash re-hashes the submitted password and compares it to
    # the stored hash — it never decrypts the stored hash 
    if user is None:
        return jsonify({"success": False, "message" : "Invalid username or password"})

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "message" : "Invalid username or password"})

    # Store the logged-in user's identity in the signed session cookie,
    # so future requests (e.g. sending a chat message) know who they're from.
    session["username"] = user["username"]
    session["role"] = user["role"]

    return jsonify({"success": True, "role": user["role"]})


@auth_bp.route("/logout", methods = ["POST"])
def logout():
    """
    Clears the current session, logging the user out
    """

    session.clear() # remove all session data, effectively logging the user out
    return jsonify({"success" : True})

