import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class AuthRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_route(self):
        response = self.client.get(url_for('auth.signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_submission(self):
        response = self.client.post(url_for('auth.signup'), data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created.', response.data)

    def test_login_route(self):
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_login_form_submission(self):
        user = User(username='testuser', email='testuser@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(url_for('auth.login'), data={
            'email': 'testuser@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_logout_route(self):
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()