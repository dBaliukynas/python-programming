from .base import base_blueprint
from .player import player_blueprint

def init_app(app):
    app.register_blueprint(base_blueprint)
    app.register_blueprint(player_blueprint)