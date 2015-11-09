from app import db, models


class Project(models.Base):
    name = db.Column(db.Text, index=True, unique=True)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Project: {}>'.format(self.name)
