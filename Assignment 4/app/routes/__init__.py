from flask import Blueprint

from app.routes.main import main_blueprint

import app.routes.base
import app.routes.player
import app.routes.search


def init_app(app):

    app.register_blueprint(main_blueprint)
