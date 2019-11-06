from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt import JWT, jwt_required, current_identity

from app import db
from .models import User
from .serializers import UserCreateSchema, UserSchema

user_blueprint = Blueprint(
    "auth", "auth", url_prefix="/auth", description="Authentication"
)


@user_blueprint.route("/protected")
@jwt_required()
def protected_view():
    return {"details": f"Hello {current_identity}"}


@user_blueprint.route("/users")
class AuthViews(MethodView):
    @user_blueprint.arguments(UserCreateSchema)
    @user_blueprint.response(UserSchema(only=["email", "creation_date"]), code=201)
    def post(self, new_data):
        """Creates a new user"""
        db.session.add(new_data)
        db.session.commit()
        return new_data
