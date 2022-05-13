from flask import Blueprint, render_template, abort, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from app.db import db

from app.models.player import PlayerModel

player_blueprint = Blueprint('player', __name__, template_folder='templates')


class PlayerForm(FlaskForm):
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

    submit = SubmitField()


@player_blueprint.route("/player/<int:player_id>")
def player(player_id):
    player_id = int(player_id)
    player = PlayerModel.query.filter(
        PlayerModel.id == player_id).first_or_404()

    return render_template("player.html", player=player, form='')


@player_blueprint.route("/player/<int:player_id>/delete")
def delete_player(player_id):
    player_id = int(player_id)
    PlayerModel.query.filter(PlayerModel.id == player_id).delete()
    db.session.commit()
    return redirect("/")


@player_blueprint.route("/player/<int:player_id>/edit", methods=['GET', 'POST'])
def update_player(player_id):
    player_id = int(player_id)
    player = PlayerModel.query.filter(
        PlayerModel.id == player_id).first_or_404()

    form = PlayerForm(name_value=player.name, surname_value=player.surname, number_value=player.number,
                      nationality_value=player.nationality, position_value=player.position,
                      points_value=player.points, rebounds_value=player.rebounds,
                      assists_value=player.assists, steals_value=player.steals,
                      blocks_value=player.blocks, performance_index_rating_value=player.performance_index_rating)

    if request.method == 'POST':
        player_values = ['name', 'surname', 'number', 'nationality', 'position',
                         'points', 'rebounds', 'assists', 'steals', 'blocks', 'performance_index_rating']

        for index, value in enumerate(form.data.values()):
            print(player)
            if index < len(form.data) - 2:
                setattr(player, player_values[index], value)

        db.session.commit()

        return redirect(f"/player/{player_id}/edit")

    return render_template("player.html", player=player, form=form)


@player_blueprint.route("/player/create", methods=['GET', 'POST'])
def create_player():
    form = PlayerForm()

    if request.method == 'POST':
        player_values = ['name', 'surname', 'number', 'nationality', 'position',
                         'points', 'rebounds', 'assists', 'steals', 'blocks', 'performance_index_rating']

        for index, value in enumerate(form.data.values()):
            print(player)
            if index < len(form.data) - 2:
                setattr(player, player_values[index], value)

        player_instance = PlayerModel(form.name_value.data, form.surname_value.data, form.number_value.data,
                                      form.nationality_value.data, form.position_value.data, form.points_value.data,
                                      form.rebounds_value.data, form.assists_value.data, form.steals_value.data,
                                      form.blocks_value.data, form.performance_index_rating_value.data, 'Test')

        db.session.add(player_instance)
        db.session.commit()

        return redirect (f"/player/{player_instance.id}")

    return render_template("player.html", player=None, form=form)
