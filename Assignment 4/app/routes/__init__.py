from .base import base_blueprint

def init_app(app):
    app.register_blueprint(base_blueprint)