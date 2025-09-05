from django import forms
from django.contrib.auth.forms import UserCreationForm

from blog.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password1',
            'password2',
        ]

