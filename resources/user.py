import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required
)
import redis
# from rq import Queue
# from tasks import send_user_registration_email
# from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema#, UserRegisterSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")
r = redis.Redis(host='redis', port=6379, db=0)

# connection = redis.from_url(
#     os.getenv("REDIS_URL")
# )  # Get this from Render.com or run in Docker
# queue = Queue("emails", connection=connection)
    
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()

        refresh_count_key = f"refresh_count:{current_user}"
        refresh_count = r.get(refresh_count_key)  # Get the refresh count from Redis

        if not refresh_count:
            refresh_count = 0
        else:
            # Data type conversion, byte -> int
            refresh_count = int(refresh_count.decode('utf-8'))
        
        if refresh_count < 3:
            # Increment the refresh count
            refresh_count += 1

            r.set(refresh_count_key, refresh_count)  # Store the updated count in Redis

            # Create a new access token with the "fresh" claim set to False
            new_token = create_access_token(identity=current_user, fresh=False)

            return {"access_token": new_token, "refresh_count": refresh_count}, 200
        else:
            # Revoke the refresh token by adding its JTI to the blocklist
            jti = get_jwt()["jti"]
            r.sadd("blocklist", jti)

            # Reset the refresh count for the current user when reauthenticating
            r.delete(refresh_count_key)  # Delete the refresh count key

            return {"message": "Refresh token revoked"}, 401


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            # or_(
            UserModel.username == user_data["username"]
                # UserModel.email == user_data["email"]
            # )
        ).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            # email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        # queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        r.sadd("blocklist", jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    """
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200