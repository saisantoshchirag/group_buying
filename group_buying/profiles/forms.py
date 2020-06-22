from django import forms
from .models import UserProfile

class UpdateForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form1'}))
    class Meta:
        model = UserProfile
        fields = ('image','state','city','pincode','gender','phone_number')
