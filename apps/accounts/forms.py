from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .mailchimp import subscribe_user


class RegistrationForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    first_name = forms.CharField(label=_('First Name'), required=False)
    last_name = forms.CharField(label=_('Last Name'), required=False)
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput())
    confirm = forms.CharField(label=_('Confirm Password'),
                              widget=forms.PasswordInput())
    subscribed = forms.BooleanField(label=_('Subscribe to newsletters'),
                                    initial=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                _('This username is already registered'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered'))
        return email

    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if password != confirm:
            raise forms.ValidationError(_('Passwords do not match'))
        return password

    def save(self):
        cd = self.cleaned_data
        user = User.objects.create_user(
            username=cd['username'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
            email=cd['email'],
            password=cd['password'],
        )
        user.save()

        if cd['subscribed']:
            subscribe_user(cd['email'])

        return user


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.add_error('username',
                           forms.ValidationError(_('Wrong Username')))
        else:
            if password and not user.check_password(password):
                self.add_error('password',
                               forms.ValidationError(_('Wrong Password')))
        return cleaned_data
