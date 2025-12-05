from datetime import datetime, timedelta
import os
import secrets
from flask import request
from flask_smorest import Blueprint, abort
from app.models import db, User
from app.schemas import UserRegisterSchema, UserLoginSchema, UserInfoSchema
from werkzeug.exceptions import Unauthorized

blp = Blueprint("Auth", "auth", url_prefix="/api/auth", description="Authentication endpoints")

JWT_SECRET = os.getenv("JWT_SECRET", None)
if not JWT_SECRET:
    # Fallback to generated secret in memory (non-persistent). Recommend setting via env in production.
    JWT_SECRET = secrets.token_hex(32)

def _make_token(user: User) -> str:
    # Very lightweight signed token: user_id:expiry:signature
    # For simplicity here, use secrets-based signature (NOT for production).
    exp = int((datetime.utcnow() + timedelta(days=7)).timestamp())
    base = f"{user.id}:{exp}"
    sig = secrets.token_hex(8)
    return f"{base}:{sig}"

def _parse_token(token: str):
    try:
        user_id_s, exp_s, _sig = token.split(":")
        exp = int(exp_s)
        if exp < int(datetime.utcnow().timestamp()):
            raise Unauthorized("Token expired")
        user = User.query.get(int(user_id_s))
        if not user:
            raise Unauthorized("Invalid token")
        return user
    except Exception:
        raise Unauthorized("Invalid token")


# PUBLIC_INTERFACE
@blp.route("/register", methods=["POST"])
@blp.arguments(UserRegisterSchema, as_kwargs=True)
@blp.response(201, UserInfoSchema)
def register(email: str, password: str, name: str | None = None):
    """Register a new user and return user info.
    Request: {email, password, name?}
    Returns: user object.
    """
    if User.query.filter_by(email=email.lower()).first():
        abort(400, message="Email already registered")
    user = User(email=email.lower(), name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "email": user.email, "name": user.name}


# PUBLIC_INTERFACE
@blp.route("/login", methods=["POST"])
@blp.arguments(UserLoginSchema, as_kwargs=True)
def login(email: str, password: str):
    """Login user and return token and user info."""
    user = User.query.filter_by(email=email.lower()).first()
    if not user or not user.check_password(password):
        abort(401, message="Invalid credentials")
    token = _make_token(user)
    return {"token": token, "user": {"id": user.id, "email": user.email, "name": user.name}}


# PUBLIC_INTERFACE
@blp.route("/me", methods=["GET"])
@blp.response(200, UserInfoSchema)
def me():
    """Get current user info from Authorization: Bearer <token>."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, message="Missing token")
    token = auth.split(" ", 1)[1]
    user = _parse_token(token)
    return {"id": user.id, "email": user.email, "name": user.name}
