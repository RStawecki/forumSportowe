from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    # no need to add the email field here, because I changed the user model - added email field there
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')