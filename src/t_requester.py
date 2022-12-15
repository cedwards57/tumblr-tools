import os
from dotenv import find_dotenv, load_dotenv, set_key
env_file = find_dotenv()
load_dotenv(env_file)
import requests
import random
import string
import json
from requests_oauthlib import OAuth1
from authlib.integrations.requests_client import OAuth1Auth
from urllib.parse import parse_qs, urlencode
from src.t_error import TumblrError

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

class TAuthorizer():
    '''OAuth2 authentication for Tumblr API v2'''
    def __init__(self):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.url = 'https://www.tumblr.com'
        self.auth2_url_base = 'https://www.tumblr.com/oauth2'
        self.headers = {'Authorization': 'Bearer ' + self.consumer_key}
    
    def get_authorize_url(self):
        scope = 'basic%20write%20offline_access'
        state = ''.join(random.choices(string.ascii_uppercase, k=15))
        # redir = 'http://localhost:8080/re'
        url = f'{self.auth2_url_base}/authorize?client_id={self.consumer_key}&response_type=code&scope={scope}&state={state}'
        return url
    
    def get_token(self, code, state):
        url = 'https://api.tumblr.com/v2/oauth2/token'
        response = requests.post(url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': consumer_key,
            'client_secret': consumer_secret
        })
        self.access_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']
        # blog_url = (t.get("/user/info"))['user']['blogs'][0]['url']
        # blog_url = urlparse(url).netloc.split('.')[0]

        blog_url = requests.get(
            'https://api.tumblr.com/v2/user/info',
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'User-Agent': 'Perikit',
                'Content-Type': 'application/json'
                })
        blog_url = blog_url.json()['response']['user']['name']

        set_key(env_file, f"{blog_url.upper()}_ACCESS_TOKEN", self.access_token)
        set_key(env_file, f"{blog_url.upper()}_REFRESH_TOKEN", self.refresh_token)
    
    def _check_response(self, response):
        if response.status_code != 200 and response.status_code != 201:
            raise TumblrError(response)



class TRequester():
    '''Request wrapper for Tumblr API v2'''
    def __init__(self, consumer_key, consumer_secret, access_token, refresh_token, blog_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.headers = {
            'User-Agent': 'Perikit',
            # 'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        self.blog_url = blog_url
        self.params = {'api_key': consumer_key}
        self.refresh_token = refresh_token
        self.base_url = 'https://api.tumblr.com/v2'
    
    def request(self, endpoint, method='GET', blog_url=None, params=None, extra_path_param=None):
        base_url = self.base_url
        params.update(self.params)
        if blog_url is not None:
            url = f'{base_url}/blog/{blog_url}{endpoint}'
        else:
            url = f'{base_url}{endpoint}'
        if extra_path_param is not None:
            url = f'{url}/{extra_path_param}'
        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        if method == 'POST':
            response = requests.post(url, headers=self.headers, data=params)
        self._check_response(response)
        try:
            response = response.json()['response']
        except:
            response = response.content # for images
        return response
    
    def get(self, endpoint, blog_url=None, params=None, extra_path_param=None):
        return self.request(endpoint, method='GET', blog_url=blog_url, params=params, extra_path_param=extra_path_param)
    
    def post(self, endpoint, blog_url=None, params=None, extra_path_param=None):
        return self.request(endpoint, method='POST', blog_url=blog_url, params=params, extra_path_param=extra_path_param)
    
    def refresh_tokens(self):
        url = 'https://api.tumblr.com/v2/oauth2/token'
        response = requests.post(url, data={
            'grant_type': 'refresh_token',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
            'refresh_token': self.refresh_token
        })
        if response.status_code != 200 and response.status_code != 201:
            raise Exception('Tried and failed to refresh OAuth2 token.')
        self.headers['Authorization'] = f'Bearer {response.json()["access_token"]}'
        self.refresh_token = response.json()['refresh_token']

        set_key(env_file, f"{self.blog_url.upper()}_ACCESS_TOKEN", response.json()['access_token'])
        set_key(env_file, f"{self.blog_url.upper()}_REFRESH_TOKEN", self.refresh_token)
    
    def _check_response(self, response):
        if response.status_code != 200 and response.status_code != 201:
            if response.status_code == 401:
                self.refresh_tokens()
            else:
                raise TumblrError(response)
            