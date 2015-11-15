from app import db
from app.models import BaseModel


class Todo(BaseModel):
    todo = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('todostatus.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('todocategory.id'))
    closed_on = db.Column(db.DateTime)
    do_before = db.Column(db.DateTime)
    priority = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Todo item: {}>'.format(self.id)


class TodoCategory(BaseModel):
    category = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Todo category: {}'.format(self.category)


class TodoStatus(BaseModel):
    status = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Todo status: {}'.format(self.status)


class TodoPriority(BaseModel):
    priority = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Todo priority: {}'.format(self.priority)
