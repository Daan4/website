from app import db
from app.models import BaseModel


class Stream(BaseModel):
    channel = db.Column(db.String(64), index=True, unique=True)
    is_online = db.Column(db.Boolean)
    game = db.Column(db.String(128), index=True)
    viewers = db.Column(db.Integer)

    def __repr__(self):
        return '<Twitch channel: {}>'.format(self.channel)
