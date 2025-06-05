from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
            'placeholder': 'Choose a username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2') 