from tests.app_tests import BaseTestCase
from app.mod_auth.models import *
from app.mod_auth.views import user_is_logged_in
from flask import url_for


TEST_USERNAME = 'username'
TEST_PASSWORD = 'password'
TEST_INVALID_USERNAME = 'wrong_username'
TEST_INVALID_PASSWORD = 'wrong_password'


class TestAuth(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_user = User(username=TEST_USERNAME, password=TEST_PASSWORD)
        db.session.add(test_user)
        db.session.commit()

    def login(self, username, password):
        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout', follow_redirects=True))

    def test_login(self):
        with self.client:
            self.login(TEST_INVALID_USERNAME, TEST_PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(TEST_USERNAME, TEST_INVALID_PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(TEST_INVALID_USERNAME, TEST_INVALID_PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(TEST_USERNAME, TEST_PASSWORD)
            self.assertTrue(user_is_logged_in())

    def test_logout(self):
        with self.client:
            self.login(TEST_USERNAME, TEST_PASSWORD)
            self.assertTrue(user_is_logged_in())
            self.logout()
            self.assertFalse(user_is_logged_in())
