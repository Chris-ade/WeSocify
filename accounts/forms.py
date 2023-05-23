from django import forms
from .models import *

class login_form(forms.Form):
  """ 
  Creates a form for logging in users
  """
  username = forms.CharField(max_length=25)
  password = forms.CharField(widget=forms.PasswordInput)

class signup_form(forms.Form):
  """
  Creates a form for registering users
  """
  name = forms.CharField(max_length=25)
  username = forms.CharField(max_length=20)
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)
  cpass = forms.CharField(widget=forms.PasswordInput)

class settings_form(forms.Form):
  '''
  Creates a form for user profile settings
  '''
  cover = forms.FileField(required=False)
  avatar = forms.FileField(required=False)
  bio = forms.CharField(required=False, max_length=150, widget=forms.Textarea)
  location = forms.CharField(max_length=30, required=False)
  website = forms.CharField(max_length=30, required=False)