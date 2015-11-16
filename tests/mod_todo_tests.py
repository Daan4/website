from tests.app_tests import BaseTestCase
from app.mod_todo.models import *
from flask import url_for
import datetime

TODO = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; Sin tantum modo ad indicia veteris memoriae cognoscenda, curiosorum. Duo Reges: constructio interrete. Tollenda est atque extrahenda radicitus. Atque ego: Scis me, inquam, istud idem sentire, Piso, sed a te opportune facta mentio est.'
CATEGORY = 'Category'
PRIORITY = 'Priority'
DO_BEFORE = datetime.datetime(2020, 12, 12)


class TestTodo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.disable_login = True
        super().setUpClass()
        cls.url = url_for('adminpanel.configure_module', bp_name='todo')

    def setUp(self):
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

    def test_create_todo_item(self):
        # Test adding an item
        self.create_todo_item(TODO, 1, 1, DO_BEFORE)
        todo_item = Todo.query.filter_by(todo=TODO).first()
        self.assertIsInstance(todo_item, Todo)
        self.assertEquals(todo_item.category_id, 1)
        self.assertEquals(todo_item.priority_id, 1)
        self.assertEquals(todo_item.do_before, DO_BEFORE)
        # Test that adding a todo item with empty todo fails
        self.create_todo_item('', 1, 1, DO_BEFORE)
        todo_item = Todo.query.filter_by(todo='').first()
        self.assertIsNone(todo_item)
