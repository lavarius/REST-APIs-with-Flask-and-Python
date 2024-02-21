import os
# import redis

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from settings import load_dotenv
# from rq import Queue

from db import db
from oa import oauth, github
# import redis
# from blocklist import BLOCKLIST

import models

from resources.user import blp as UserBlueprint
from resources.user import r
from resources.github_login import blp as GithubLoginBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # connection = redis.from_url(
    #     os.getenv("REDIS_URL")
    # )  # Get this from Render.com or run in Docker
    # app.queue = Queue("emails", connection=connection)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    var_db_url = {
        "local": "sqlite:///data.db",
        "cloud": os.getenv("DATABASE_URL"),
    }[os.getenv("ENV")]
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or var_db_url#os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(GithubLoginBlueprint)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize the OAuth object with the Flask app instance
    oauth.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "mark"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    jwt = JWTManager(app)


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return r.sismember("blocklist", jti)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    #api.register_blueprint(GithubLoginBlueprint)


    return app
