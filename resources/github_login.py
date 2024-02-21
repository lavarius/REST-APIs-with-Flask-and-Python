from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from oa import github

blp = Blueprint('github_login', __name__, url_prefix='/login')

@blp.route("/github")
class GitHubLogin(MethodView):
    @classmethod
    def get(cls):
        redirect_uri = "http://localhost:5000/login/github/authorized"
        return github.authorize_redirect(redirect_uri)

@blp.route('/github/authorized')
class GitHubAuthorize(MethodView):
    @classmethod
    def get(cls):
        # Use authorize_access_token() to fetch the access token
        github.authorize_access_token()
        # g.access_token = resp.get('access_token')
        github_user = github.get('user')
        github_username = github_user.json().get('login')  # Adjusted this line from .data['login']
        return github_username
