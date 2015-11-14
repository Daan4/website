from app.models import BaseModel
from app import db
from sqlalchemy_utils import PasswordType


class User(BaseModel):
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
