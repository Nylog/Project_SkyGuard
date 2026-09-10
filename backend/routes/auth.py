from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.db_utils import get_user_by_username



auth_bp = Blueprint("auth", __name__)  # Authentication blueprint to decouple auth routes from the main app.py
