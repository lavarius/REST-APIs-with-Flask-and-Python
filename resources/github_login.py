from flask import url_for, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from oa import github

blp = Blueprint('github_login', __name__, url_prefix='/github')

@blp.route("/login")
def login():
    redirect_uri = "http://localhost:5000/login/github/authorized"
    return github.authorize_redirect(redirect_uri)

@blp.route('/github/authorized')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user')
    user_info = resp.json()
    # Process the user_info and token as needed
    return 'Logged in successfully with GitHub'
# class GitHubLogin(MethodView):
#     @classmethod
#     def get(cls):
#         return github.authorize_redirect(callback="http://localhost:5000/login/github/authorized")