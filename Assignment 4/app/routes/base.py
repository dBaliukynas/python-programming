from flask import Blueprint
from flask import render_template
from app.models.player import PlayerModel

base_blueprint = Blueprint('base', __name__, template_folder='templates')

@base_blueprint.route("/")
def base():
    players = PlayerModel.query.all()
    return render_template("base.html", players=players)