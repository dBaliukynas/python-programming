from flask import Blueprint, render_template, current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField

from app.db import db

from app.routes.main import main_blueprint


class SearchForm(FlaskForm):
    submit = SubmitField()


@main_blueprint.context_processor
def inject_global_template_variables():
    form = SearchForm()
    return dict(form=form)


@main_blueprint.route("/search", methods=['GET', 'POST'])
def search():
    return render_template("search.html")
