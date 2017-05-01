from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import override_settings
from django_webtest import WebTest

from apps.shop import utils as utils
from . import mailchimp


@override_settings(LANGUAGE_CODE='en')
class UserWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def setUp(self):
        self.username = 'username2'
        self.first_name = 'First1'
        self.last_name = 'Last1'
        self.email = 'sometest2@email.ts'
        self.password = 'password123451'

    def test_registration(self):
        form = self.app.get(reverse('accounts:register')).forms['main-form']
        form['username'] = self.username
        form['first_name'] = self.first_name
        form['last_name'] = self.last_name
        form['email'] = self.email
        form['password'] = self.password
        form['confirm'] = self.password
        form.submit()

        user = User.objects.filter(username=self.username).first()
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        mailchimp.unsubscribe_user(self.email)
        self.assertNotIn(self.email, mailchimp.get_emails_list())

    def test_registration_username_already_registered(self):
        registered_user = utils.get_regular_user()
        form = self.app.get(reverse('accounts:register')).forms['main-form']
        form['username'] = registered_user.username
        form['first_name'] = self.first_name
        form['last_name'] = self.last_name
        form['email'] = self.email
        form['password'] = self.password
        form['confirm'] = self.password
        response = form.submit()

        self.assertIn('This username is already registered',
                      response.unicode_normal_body)

    def test_registration_email_already_registered(self):
        registered_user = utils.get_regular_user()
        form = self.app.get(reverse('accounts:register')).forms['main-form']
        form['username'] = self.username
        form['first_name'] = self.first_name
        form['last_name'] = self.last_name
        form['email'] = registered_user.email
        form['password'] = self.password
        form['confirm'] = self.password
        response = form.submit()

        self.assertIn('This email is already registered',
                      response.unicode_normal_body)

    def test_registration_passwords_do_not_match(self):
        form = self.app.get(reverse('accounts:register')).forms['main-form']
        form['username'] = self.username
        form['first_name'] = self.first_name
        form['last_name'] = self.last_name
        form['email'] = self.email
        form['password'] = self.password
        form['confirm'] = 'password_12345'
        response = form.submit()

        self.assertIn('Passwords do not match', response.unicode_normal_body)

    def test_subscribe_and_unsubscribe(self):
        form = self.app.get(reverse('accounts:register')).forms['main-form']
        form['username'] = self.username + '_1'
        form['first_name'] = self.first_name
        form['last_name'] = self.last_name
        test_email = ''.join(self.email.split('.')) + '.ua'
        form['email'] = test_email
        form['password'] = self.password
        form['confirm'] = self.password
        form.submit()

        self.assertIn(test_email, mailchimp.get_emails_list())

        mailchimp.unsubscribe_user(test_email)
        self.assertNotIn(test_email, mailchimp.get_emails_list())

    def test_login_and_logout(self):
        user = utils.get_regular_user()
        form = self.app.get(reverse('accounts:login')).forms['main-form']
        form['username'] = user.username
        form['password'] = 'some_secret_password_123'
        response = form.submit().follow()

        self.assertEqual(response.context['user'], user)

        logout = self.app.get(reverse('accounts:logout'))
        self.assertRedirects(
            response=logout,
            expected_url="/accounts/login/",
        )
        response = logout.follow()
        current_user = response.context['user']
        self.assertFalse(current_user.is_authenticated)

    def test_login_user_enter_wrong_username(self):
        form = self.app.get(reverse('accounts:login')).forms['main-form']
        form['username'] = 'wrong_username'
        form['password'] = 'some_secret_password_123'
        response = form.submit()

        self.assertIn('Wrong Username', response.unicode_normal_body)

    def test__login_user_enter_wrong_password(self):
        user = utils.get_regular_user()
        form = self.app.get(reverse('accounts:login')).forms['main-form']
        form['username'] = user.username
        form['password'] = "wrong_test_password"
        response = form.submit()

        self.assertIn('Wrong Password', response.unicode_normal_body)
