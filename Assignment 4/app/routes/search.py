from flask import Blueprint, render_template, current_app, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


from app.db import db

from app.routes.main import main_blueprint

from app.models.player import PlayerModel


class SearchForm(FlaskForm):
    search_field = StringField(validators=[DataRequired()])
    submit = SubmitField()


@main_blueprint.context_processor
def inject_global_template_variables():
    header_form = SearchForm()
    return dict(header_form=header_form)


@main_blueprint.route("/search", methods=['GET'])
def search():
    header_form = SearchForm(request.args)
    search_value = header_form.data['search_field']
    print(search_value)
    players = PlayerModel.query.filter(PlayerModel.name.like(
        search_value + '%') |
        PlayerModel.surname.like(search_value + '%') |
        PlayerModel.number.like(search_value + '%') |
        PlayerModel.nationality.like(search_value + '%')).all()
    print(players)

    return render_template("search.html", players=players)
