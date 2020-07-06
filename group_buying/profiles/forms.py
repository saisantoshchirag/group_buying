from django import forms
from .models import UserProfile

class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
