from app.db import db

class Player(db.Model):

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
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'<Player {self.name + " " + self.surname}>'
