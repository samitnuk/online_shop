from django_webtest import WebTest

from django.contrib.auth.models import User
from django.shortcuts import reverse

from apps.shop import utils


class UserWebTests(WebTest):

    def test_user_registration(self):
        username = 'username1',
        first_name = 'First1',
        last_name = 'Last1',
        email = 'sometest1@email.ts',
        password = "password123451",

        form = self.app.get(reverse('users:register')).form
        form['username'] = username
        form['first_name'] = first_name
        form['last_name'] = last_name
        form['email'] = email
        form['password'] = password
        form.submit()

        user = User.objects.filter(username=username).first()
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
