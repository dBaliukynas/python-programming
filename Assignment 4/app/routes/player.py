from flask import Blueprint, render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField

from app.models.player import PlayerModel

player_blueprint = Blueprint('player', __name__, template_folder='templates')


class TestForm(FlaskForm):
    name_value = StringField()
    surname_value = StringField()
    number_value = IntegerField()
    nationality_value = StringField()
    position_value = StringField()
    points_value = FloatField()
    rebounds_value = FloatField()
    assists_value = FloatField()
    steals_value = FloatField()
    blocks_value = FloatField()
    performance_index_rating_value = FloatField()

    submit = SubmitField('Submit')


@player_blueprint.route("/player/<player_id>")
@player_blueprint.route("/player/<player_id>/edit", methods=['GET', 'POST'])
def player(player_id):
    player_id = int(player_id)
    player = PlayerModel.query.filter(PlayerModel.id == player_id).first()

    if player is None:
        abort(404)

    name = player.name
    form = TestForm(name_value=player.name, surname_value=player.surname, number_value=player.number,
                    nationality_value=player.nationality, position_value=player.position, 
                    points_value=player.points, rebounds_value=player.rebounds, 
                    assists_value=player.assists, steals_value=player.steals,
                    blocks_value=player.blocks, performance_index_rating_value=player.performance_index_rating)

    return render_template("player.html", player=player, name=name, form=form)
