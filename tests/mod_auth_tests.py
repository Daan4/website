from tests.app_tests import BaseTestCase
from app.mod_auth.models import *
from app.mod_auth.views import user_is_logged_in
from flask import url_for

USERNAME = 'username'
PASSWORD = 'password'
INVALID_USERNAME = 'wrong_username'
INVALID_PASSWORD = 'wrong_password'


class TestAuth(BaseTestCase):
    def setUp(self):
        super().setUp()
        User.create(username=USERNAME, password=PASSWORD)

    def login(self, username, password):
        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout', follow_redirects=True))

    def test_login(self):
        with self.client:
            self.login(INVALID_USERNAME, PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(USERNAME, INVALID_PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(INVALID_USERNAME, INVALID_PASSWORD)
            self.assertFalse(user_is_logged_in())
            self.login(USERNAME, PASSWORD)
            self.assertTrue(user_is_logged_in())

    def test_logout(self):
        with self.client:
            self.login(USERNAME, PASSWORD)
            self.assertTrue(user_is_logged_in())
            self.logout()
            self.assertFalse(user_is_logged_in())
