import os
from dotenv import find_dotenv, load_dotenv
import webbrowser
import flask
# from src.add_blog_functions import get_approval, verify, get_auth_url, get_token
from src.t_requester import TAuthorizer

def flask_app():
    load_dotenv(find_dotenv())
    app = flask.Flask(__name__)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    a = TAuthorizer()
    webbrowser.open(a.get_authorize_url())

    

    @app.route("/")
    def index():
        # args = flask.request.args
        # oauth_verifier = args.get("oauth_verifier")
        # verify(oauth_token, oauth_token_secret, oauth_verifier)
        return "This page is blank."
    
    @app.route("/callback")
    def callback():
        args = flask.request.args
        code = args.get('code')
        state = args.get('state')
        # print(code, state)
        a.get_token(code,state)
        # oauth_verifier = args.get("oauth_verifier")
        # verify(oauth_token, oauth_token_secret, oauth_verifier)
        return "Done. Close this window and hit CTRL+C in the terminal!"
        
    return app

def run_app():
    app = flask_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))

if __name__ == "__main__":
    run_app()