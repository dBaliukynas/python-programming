import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .db import db
from .models import player


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    Migrate(app, db)

    # with app.app_context():
    #     db.create_all()

    def __repr__(self):
        return f'<Student {self.firstname}>'

    @ app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
