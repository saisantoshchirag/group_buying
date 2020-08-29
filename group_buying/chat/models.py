from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
class Car(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=25,null=True)
    brand = models.CharField(max_length=25,null=True)
    version = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    image = models.CharField(max_length=100)
    mileage = models.IntegerField(null=True)
    fuel_type = models.CharField(max_length=20,null=True)
    seating_capacity = models.IntegerField(null=True)
    body_style = models.CharField(max_length=20,null=True)
    fuel_tank_capacity = models.IntegerField(null=True)

class ChatRoom(models.Model):
    eid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    vehicle = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    max_limit = models.IntegerField()
    # car  = models.ForeignKey(Car,on_delete=models.CASCADE)

class ChatUser(models.Model):
    chat = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

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

