from datetime import datetime
from app.db import db


class SeasonModel(db.Model):
    def __init__(self, name):

        self.name = name
        self.created_at = datetime.now()

    __tablename__ = 'seasons'
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
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'<Season {self.name}>'
