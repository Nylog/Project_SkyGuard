from flask import Flask

app = Flask(__name__)
app.secret_key = "skyguard-dev-secret" # Used by Flask to cryptographically sign session cookies


if __name__ == "__main__" :
    app.run(debug = True)
