from django import forms
from .models import ChatMessage

class ChatRooms(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = ChatMessage
        fields = ('image',)