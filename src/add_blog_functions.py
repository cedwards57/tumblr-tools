import os
from dotenv import find_dotenv, load_dotenv, set_key
env_file = find_dotenv()
load_dotenv(env_file)
from tumblpy import Tumblpy

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")


def get_approval():
    '''Generates the URL and initial tokens to authorize the app to access your blog.'''
    t = Tumblpy(consumer_key, consumer_secret)
    auth_props = t.get_authentication_tokens(callback_url='http://localhost:8080/callback')
    auth_url = auth_props['auth_url']
    print('Connect with Tumblr via: %s' % auth_url)
    oauth_token = auth_props["oauth_token"]
    oauth_token_secret = auth_props['oauth_token_secret']
    return oauth_token, oauth_token_secret

def verify(oauth_token, oauth_token_secret, oauth_verifier):
    '''After the app has been authorized, this saves the finalized OAuth tokens which allow ongoing API usage with read/write access.'''
    t = Tumblpy(consumer_key, consumer_secret,
                oauth_token, oauth_token_secret)

    authorized_tokens = t.get_authorized_tokens(oauth_verifier)
    final_oauth_token = authorized_tokens['oauth_token']
    final_oauth_token_secret = authorized_tokens['oauth_token_secret']

    t = Tumblpy(consumer_key, consumer_secret,
                final_oauth_token, final_oauth_token_secret)
    url = (t.post("user/info"))['user']['blogs'][0]['url']
    url = url.split("://", 1)[1]
    url = url.split(".", 1)[0]
    if final_oauth_token is not None:
        set_key(env_file, f"{url.upper()}_OAUTH_TOKEN", final_oauth_token)
        set_key(env_file, f"{url.upper()}_OAUTH_TOKEN_SECRET", final_oauth_token_secret)
    else:
        print("Error: Nothing returned for the final OAuth tokens.")
