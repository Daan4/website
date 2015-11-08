from app import db
from sqlalchemy_utils import PasswordType


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(64), index=True, unique=True)
    is_online = db.Column(db.Boolean)
    game = db.Column(db.String(128), index=True)
    viewers = db.Column(db.Integer)

    def __repr__(self):
        return '<Twitch channel: {}>'.format(self.channel)
