from app import db
from app.models import BaseModel


class Todo(BaseModel):
    todo = db.Column(db.Text, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('todo_category.id'))
    priority_id = db.Column(db.Integer, db.ForeignKey('todo_priority.id'))
    closed_on = db.Column(db.DateTime)
    do_before = db.Column(db.DateTime)

    def __repr__(self):
        return '<Todo item: {}>'.format(self.id)

    def get_category(self):
        return TodoCategory.query.filter_by(id=self.category_id).first().category

    def get_priority(self):
        return TodoPriority.query.filter_by(id=self.priority_id).first().name

    def complete(self):
        self.closed_on = db.func.current_timestamp()
        db.session.commit()


class TodoCategory(BaseModel):
    category = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Todo category: {}'.format(self.category)


class TodoPriority(BaseModel):
    name = db.Column(db.String(64), unique=True, index=True)
    priority = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Todo priority: {}'.format(self.priority)
