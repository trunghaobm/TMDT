from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = models.User
        fields = ['avatar', 'name', 'username', 'password', 'repassword',]
        
class LoginUserForm(CreateUserForm):
    class meta:
        model = models.User
        fields = ['username', 'password',]
