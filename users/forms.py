from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[A-Za-z]\d{9}@unison\.mx$'

        if not re.match(pattern, email):
            raise forms.ValidationError(
                "Invalid email address. It must start with a character, followed by 9 digits, an '@', and then "
                "'unison.mx'.")

        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password(self):
        return None
