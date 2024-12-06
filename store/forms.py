from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class UserRegisterForm(UserCreationForm): # we want to create an email section in our user registration form, so we have to make a class
    email = forms.EmailField() # default argument is required = True

    class Meta: # gives nested name space for configurations and keeps configurations in one place
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ['username', 'email']