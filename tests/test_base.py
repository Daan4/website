from app import create_app, db
import unittest


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.disable_login
        except AttributeError:
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
        db.get_engine(cls.app).dispose()

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()