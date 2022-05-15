from datetime import datetime
from app.db import db


class PlayerModel(db.Model):
    def __init__(self, name, surname, number, nationality, position, points,
                 rebounds, assists, steals, blocks, performance_index_rating, image_source):

        self.name = name
        self.surname = surname
        self.number = number
        self.nationality = nationality
        self.position = position
        self.points = points
        self.rebounds = rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.performance_index_rating = performance_index_rating
        self.image_source = image_source
        self.created_at = datetime.now()

    __tablename__ = 'players'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    surname = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    number = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    nationality = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    position = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    points = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    rebounds = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    assists = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    steals = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    blocks = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    performance_index_rating = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    image_source = db.Column(
        db.String(256),
        index=False,
        unique=False,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'<Player {self.name + " " + self.surname}>'
