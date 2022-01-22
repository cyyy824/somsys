from django.db import models
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from .models import OAUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})


class RegisterForm(UserCreationForm):
    realname = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "用户名", "class": "form-control"})
        self.fields['realname'].widget = widgets.TextInput(
            attrs={'placeholder': "实名", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "密码", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "重复密码", "class": "form-control"})

#    def save(self, commit = True):
#        user = OAUser.objects.create_user(
#            self.cleaned_data['username'],
#            self.cleaned_data['realname'],
#            self.cleaned_data['password1']
#        )
#        return user

    class Meta:
        model = OAUser
        fields = ["username", "realname", 'password1', 'password2']
