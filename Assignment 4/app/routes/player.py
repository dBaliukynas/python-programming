from flask import Blueprint, render_template, abort
from app.models.player import PlayerModel

player_blueprint = Blueprint('player', __name__, template_folder='templates')

@player_blueprint.route("/player/<player_id>")
def player(player_id):
    player_id = int(player_id)
    if player_id < 0:
        abort(404)

    player = PlayerModel.query.filter(PlayerModel.id == player_id).first()

    return render_template("player.html", player=player)