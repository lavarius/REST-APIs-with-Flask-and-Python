import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

github = oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CONSUMER_KEY"),
    client_secret=os.getenv("GITHUB_CONSUMER_SECRET"),
    #request_token_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url='https://api.github.com/',
    #request_token_url=None,
    #access_token_method='POST',
    client_kwargs={'scope': 'user:email'}
)