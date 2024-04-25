from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import customUser


class RegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control my-2 p-3 rounded rounded-3 w-75',
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'e-Mail',
        'class': 'form-control my-2 p-3 rounded rounded-3 w-75',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control my-2 p-3 rounded rounded-3 w-75',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control my-2 p-3 rounded rounded-3 w-75',
    }))

    class Meta:
        model = customUser
        fields = ['username', 'email', 'password1', 'password2',]
