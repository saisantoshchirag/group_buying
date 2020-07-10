from django.contrib import admin
from .models import ChatMessage,ChatRoom,Car,ChatUser
# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(Car)
admin.site.register(ChatMessage)
admin.site.register(ChatUser)