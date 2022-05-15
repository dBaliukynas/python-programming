from datetime import datetime
from app.db import db


class TeamModel(db.Model):
    def __init__(self, name, wins, losses, win_streak, loss_streak, leaderboard_position, image_source):

        self.name = name
        self.wins = wins
        self.losses = losses
        self.win_streak = win_streak
        self.loss_streak = loss_streak
        self.leaderboard_position = leaderboard_position
        self.image_source = image_source
        self.created_at = datetime.now()

    __tablename__ = 'teams'
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

    wins = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True
    )
    losses = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True
    )
    win_streak = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    loss_streak = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    leaderboard_position = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True
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
        return f'<Team {self.name}>'
