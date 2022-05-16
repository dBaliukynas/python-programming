from flask import Blueprint
from flask import render_template
from app.models.player import PlayerModel
from app.models.team import TeamModel
from app.models.season import SeasonModel

from app.routes.main import main_blueprint

@main_blueprint.route("/")
def base():
    players = PlayerModel.query.all()
    teams = TeamModel.query.order_by(TeamModel.name.asc()).all()
    seasons = SeasonModel.query.all()
    
    return render_template("base.html", players=players, teams=teams, seasons=seasons)