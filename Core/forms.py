from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class User_Login_Form(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    "placeholder": "Your username"
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    "placeholder": "Your password"
  }))
