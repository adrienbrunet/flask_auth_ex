from werkzeug.security import safe_str_cmp

from .models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)
