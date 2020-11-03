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
    email = forms.EmailField(max_length=200, help_text='Required',widget = forms.TextInput(attrs={'autocomplete':'off', 'placeholder': 'Email'}))
    username = forms.CharField(max_length=200, help_text='Required',widget = forms.TextInput(attrs={'autocomplete':'off', 'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=200, help_text='Required',widget = forms.PasswordInput(attrs={'autocomplete':'off', 'placeholder': 'Password','data-toggle': 'password','id':'pass1'}))
    password2 = forms.CharField(max_length=200, help_text='Required',widget = forms.PasswordInput(attrs={'autocomplete':'off', 'placeholder': 'Confirm Password','data-toggle': 'password','id':'pass2'}))
    
    # email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
            
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

