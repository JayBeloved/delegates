from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('finance', 'Finance'),
        ('delegate_affairs', 'Delegate Affairs'),
    ]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control form-select'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role')
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].label = "Confirm Password"
        self.fields['password2'].help_text = None
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].label = "Password"
        self.fields['password1'].help_text = None
    