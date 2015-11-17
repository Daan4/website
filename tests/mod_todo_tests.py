from tests.app_tests import BaseTestCase
from app.mod_todo.models import *
from flask import url_for
import datetime

TODO = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; Sin tantum modo ad indicia veteris memoriae cognoscenda, curiosorum. Duo Reges: constructio interrete. Tollenda est atque extrahenda radicitus. Atque ego: Scis me, inquam, istud idem sentire, Piso, sed a te opportune facta mentio est.'
TODO2 = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; Sin tantum modo'
CATEGORY = 'Category'
PRIORITY = 'Priority'
DO_BEFORE = datetime.datetime(2020, 12, 12)


class TestTodo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.disable_login = True
        super().setUpClass()
        cls.url = url_for('adminpanel.configure_module', bp_name='todo')
        TodoCategory.create(category=CATEGORY)
        TodoPriority.create(name=PRIORITY, priority=0)

    def create_todo_item(self, todo, category_id, priority_id, do_before):
        return self.client.post(url_for('todo.index'), data=dict(
            todo=todo,
            category=category_id,
            priority=priority_id,
            do_before=do_before,
            create='Create'
        ))

    def delete_todo_items(self, todo_ids):
        return self.client.get(url_for('todo.index', delete=','.join([str(x) for x in todo_ids])))

    def complete_todo_items(self, todo_ids):
        return self.client.get(url_for('todo.index', complete=','.join([str(x) for x in todo_ids])))

    def test_create_todo_item(self):
        # Test adding an item
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        todo_item = Todo.query.filter_by(todo=TODO).first()
        self.assertIsInstance(todo_item, Todo)
        self.assertEquals(todo_item.category_id, 1)
        self.assertEquals(todo_item.priority_id, 1)
        self.assertEquals(todo_item.do_before, DO_BEFORE)
        # Test that adding an empty item fails
        self.create_todo_item('', 1, 1, DO_BEFORE)
        todo_item = Todo.query.filter_by(todo='').first()
        self.assertIsNone(todo_item)

    def test_delete_todo_item(self):
        # Test deleting a single item
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        self.delete_todo_items([1])
        todo = Todo.query.filter_by(id=1).first()
        self.assertIsNone(todo)
        # Test deleting multiple items
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        self.create_todo_item(TODO2, 1, 1, DO_BEFORE)
        self.delete_todo_items([2, 3])
        todo = Todo.query.filter(Todo.id.in_([2, 3])).all()
        self.assertEquals(todo, [])

    def test_complete_todo_item(self):
        # Test completing a single item
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        self.complete_todo_items([1])
        todo = Todo.query.filter_by(id=1).first()
        timedelta = datetime.datetime.now() - todo.closed_on
        self.assertLess(timedelta, datetime.timedelta(seconds=0.1))
        # Test trying to complete the same item again doesn't change the closed on time.
        old_closed_on = todo.closed_on
        self.complete_todo_items([1])
        todo = Todo.query.filter_by(id=1).first()
        self.assertEquals(old_closed_on, todo.closed_on)
        # Test completing multiple items
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        self.create_todo_item(TODO2, 1, 1, DO_BEFORE)
        self.complete_todo_items([2, 3])
        todo = Todo.query.filter(Todo.id.in_([2, 3])).all()
        for item in todo:
            self.assertIsNotNone(item.closed_on)