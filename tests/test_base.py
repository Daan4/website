from app import create_app, db
import unittest


class BaseTestCase(unittest.TestCase):
    disable_login = None
    app = None
    _ctx = None

    @classmethod
    def setUpClass(cls):
        if cls.disable_login is None:
            cls.disable_login = False
        cls.app = create_app('config.test_config', cls.disable_login)
        cls.client = cls.app.test_client()
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()
