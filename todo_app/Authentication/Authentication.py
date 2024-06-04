import os

import requests

#Get variable to determin if running local development
LOCAL_ENV = os.environ.get("ENV")

#github details
if(LOCAL_ENV == "Local"):
    GITHUB_CLIENT_ID = os.environ.get("OAUTH_ID_L")
    GITHUB_CLIENT_SECRET = os.environ.get("OAUTH_KEY_L")
    GITHUB_CALLBACK_URL = os.environ.get("OAUTH_URL_L")
else:
    GITHUB_CLIENT_ID = os.environ.get("OAUTH_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("OAUTH_KEY")
    GITHUB_CALLBACK_URL = os.environ.get("OAUTH_URL")


def construct_github_url():
    return f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_CALLBACK_URL}&scope=user:email"


def exchange_code_for_token(code):

    token_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK_URL
    }
    headers = {'Accept': 'application/json'}

    response = requests.post(token_url, data=payload, headers=headers)
    if response.ok:
        return response.json().get('access_token')
    else:
        return None


def get_github_user(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
    }
    response = requests.get('https://api.github.com/user', headers=headers)
    if response.status_code == 200:
        return response.json()
    return None
