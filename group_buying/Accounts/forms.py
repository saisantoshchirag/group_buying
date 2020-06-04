from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
choices = [
    ('dealer','dealer'),
    ('user','user'),
]

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserCreationForm(forms.ModelForm):
    print('u form entered')
    first_name = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 're-enter the password'}))
    choice = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError(
                "passwords does not match"
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email


