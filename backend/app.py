from flask import Flask

from routes.auth import auth_bp
from routes.chat import chat_bp

app = Flask(__name__)
app.secret_key = "skyguard-dev-secret" # Used by Flask to cryptographically sign session cookies


app.register_blueprint(auth_bp) # Register the blueprints so their routes (/login, /logout)
app.register_blueprint(chat_bp) # Register the blueprints so their routes (/chat)


if __name__ == "__main__" :
    app.run(debug = True)  # debug=True enables autoreload on code changes

