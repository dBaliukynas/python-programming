from flask import Blueprint
from flask import render_template

base_blueprint = Blueprint('base', __name__, template_folder='templates')


@base_blueprint.route("/")
def base():
    return render_template("base.html")