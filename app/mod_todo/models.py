from app import db
from app.models import BaseModel


class Todo(BaseModel):
    todo = db.Column(db.Text, index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('todostatus.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('todocategory.id'))
    priority_id = db.Column(db.Integer, db.ForeignKey('todopriority.id'))
    closed_on = db.Column(db.DateTime)
    do_before = db.Column(db.DateTime)

    def __repr__(self):
        return '<Todo item: {}>'.format(self.id)


class TodoCategory(BaseModel):
    category = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Todo category: {}'.format(self.category)


class TodoStatus(BaseModel):
    status = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Todo status: {}'.format(self.status)


class TodoPriority(BaseModel):
    name = db.Column(db.String(64), unique=True, index=True)
    priority = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Todo priority: {}'.format(self.priority)
