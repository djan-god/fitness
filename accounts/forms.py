from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD'
        }),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password1',
            'password2',
            'date_of_birth',
        ]


class CustomUserChangeForm(UserChangeForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD'
        }),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'date_of_birth',
        ]
