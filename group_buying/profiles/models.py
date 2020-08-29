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
    is_dealer = models.BooleanField('dealer status',default=False)
    is_user = models.BooleanField('user status',default=True)
    is_admin = models.BooleanField('admin status',default=False)
    is_subscribed = models.BooleanField('subscription status',default=False)
    subscription_start = models.DateTimeField(blank=True,null=True)
    subscription_end = models.DateTimeField(blank=True,null=True)
    phone_verified = models.BooleanField(default=False)

class ChangePassword(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    code = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

