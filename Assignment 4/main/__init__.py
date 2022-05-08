import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE='mysql:///admin:DrundrA2_@localhost:3306/euroleague' +
        # os.path.join(app.instance_path, 'main.mysql'),
    )

    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:DrundrA2_@localhost:3306/euroleague'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database = SQLAlchemy(app)

    class Student(database.Model):
        id = database.Column(database.Integer, primary_key=True)
        firstname = database.Column(database.String(100), nullable=False)
        lastname = database.Column(database.String(100), nullable=False)
        email = database.Column(database.String(
            80), unique=True, nullable=False)
        age = database.Column(database.Integer)
        bio = database.Column(database.Text)

    # database.create_all()

    def __repr__(self):
        return f'<Student {self.firstname}>'

    if test_config is None:

        app.config.from_pyfile('config.py', silent=True)
    else:

        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @ app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

# def test_connection(app):
#     with app.app_context():
#         mysql = MySQL(app)
#         conn = mysql.connection
#         cursor = conn.cursor()

#         cursor.execute(''' CREATE TABLE Persons (
#     PersonID int,
#     LastName varchar(255),
#     FirstName varchar(255),
#     Address varchar(255),
#     City varchar(255)
# ); ''')

#         mysql.connection.commit()

#         cursor.close()
