from django.db import models
from django.contrib.auth.models import User
from chat.models import ChatRoom
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image',blank=True,default='prof1.jpeg')
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField(default=0)
    room = models.ForeignKey(ChatRoom,on_delete=models.SET_NULL,blank=True,null=True)

class ChangePassword(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    code = models.IntegerField()
    date = models.DateTimeField(auto_now=True)