from django_webtest import WebTest

from django.contrib.auth.models import User
from django.shortcuts import reverse

from apps.shop import utils


class UserWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_user_registration(self):
        username = 'username2'
        first_name = 'First1'
        last_name = 'Last1'
        email = 'sometest2@email.ts'
        password = "password123451"

        form = self.app.get(reverse('users:register')).form
        form['username'] = username
        form['first_name'] = first_name
        form['last_name'] = last_name
        form['email'] = email
        form['password'] = password
        form['confirm'] = password
        form.submit()

        user = User.objects.filter(username=username).first()
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_user_login(self):
        user = utils.get_regular_user()
        form = self.app.get(reverse('users:login')).form
        form['username'] = user.username
        form['password'] = "asdkjfoih1222pkljkh"
        response = form.submit().follow()

        self.assertEqual(response.context['user'], user)
        self.assertIn(user.username, response)
        print(user.username in response)
