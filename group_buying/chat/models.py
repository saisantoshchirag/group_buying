from django.db import models
from datetime import datetime
class ChatRoom(models.Model):
    eid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=25)
class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.CharField(max_length=64)
    date = models.DateField(auto_now=True, db_index=True)
    time = models.TimeField(auto_now=True)
    text = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True,upload_to='images')
    document = models.FileField(blank=True,upload_to='files')
    def to_data(self):
        out = {}
        out['id'] = self.id
        out['from'] = self.user
        out['date'] = self.date.strftime('%H:%M:%S')
        out['text'] = self.text
        return out