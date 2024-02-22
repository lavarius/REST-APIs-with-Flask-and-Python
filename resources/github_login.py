from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import github

from models import UserModel
from schemas import UserSchema

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
        
        user = UserModel.find_by_username(github_username)

        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
