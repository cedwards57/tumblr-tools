import os
from dotenv import find_dotenv, load_dotenv
import flask
from src.add_blog_functions import get_approval, verify

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

oauth_token, oauth_token_secret = get_approval()

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/callback")
def callback():
    args = flask.request.args
    oauth_verifier = args.get("oauth_verifier")
    verify(oauth_token, oauth_token_secret, oauth_verifier)
    return flask.render_template("callback.html")

app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))