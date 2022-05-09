import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from .db import db
from .models import *
from .routes.base import base_blueprint

# routes = Blueprint('routes', __name__)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    app.register_blueprint(base_blueprint)

    bootstrap = Bootstrap5(app)

    db.init_app(app)
    Migrate(app, db)

    return app
