from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo Electronico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmacion de Contraseña'


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo Electronico'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Imagen'
        self.fields['phone'].label = 'Numero de Celular'
        self.fields['role'].label = 'Area de trabajo'
