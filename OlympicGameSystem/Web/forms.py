from django import forms
from django.contrib.auth.models import User
from models import Person
class UserForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(max_length = 100)
    password_confirm = forms.CharField(max_length = 100)
    email = forms.EmailField(max_length = 100)
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['user']
