from flask import Blueprint
from flask import render_template
from app.models.player import PlayerModel
from app.models.team import TeamModel

base_blueprint = Blueprint('base', __name__, template_folder='templates')

@base_blueprint.route("/")
def base():
    players = PlayerModel.query.all()
    teams = TeamModel.query.order_by(TeamModel.name.asc()).all()
    return render_template("base.html", players=players, teams=teams)