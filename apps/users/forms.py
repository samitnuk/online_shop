from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(label="* Логін")
    first_name = forms.CharField(label="Ім'я", required=False)
    last_name = forms.CharField(label="Прізвище", required=False)
    email = forms.EmailField(label="* Email")
    password = forms.CharField(label="* Пароль",
                               widget=forms.PasswordInput())
    confirm = forms.CharField(label="* Пароль повторно",
                              widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такий логін вже зареєстровано')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такий email вже зареєстровано')
        return email

    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if password != confirm:
            raise forms.ValidationError('Паролі не співпадають')
        return password


class LoginForm(forms.Form):
    username = forms.CharField(label="Логін")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.add_error('username',
                           forms.ValidationError('Неправильний логін'))
        else:
            if password and not user.check_password(password):
                self.add_error('password',
                               forms.ValidationError('Неправильний пароль'))
        return cleaned_data
