from flask import Blueprint, request, session, jsonify

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agent.router import handle_message
