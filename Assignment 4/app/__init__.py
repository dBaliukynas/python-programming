import os
import sys

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

from .db import db
from .models import *
from . import routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    routes.init_app(app)

    bootstrap = Bootstrap5(app)

    db.init_app(app)
    Migrate(app, db)

    return app
