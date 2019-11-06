import os

from flask import Flask, render_template

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api, Blueprint, abort
from flask_bcrypt import Bcrypt
from flask_jwt import JWT, jwt_required, current_identity


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "openapi"
    app.config["API_VERSION"] = "1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "api"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.23.11"
    app.config["SECRET_KEY"] = "super-secret"

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    from auth.services import authenticate, identity

    jwt = JWT(app, authenticate, identity)

    from auth.views import user_blueprint

    api.register_blueprint(user_blueprint)

    return app
