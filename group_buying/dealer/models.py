from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserProfile
# Create your models here.
class Dealer(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    profile = models.OneToOneField(UserProfile,on_delete=models.PROTECT)
    kyc_verified = models.BooleanField('kyc status',default=False)
    aadhar = models.FileField(upload_to='aadhar_images')
    pan = models.FileField(upload_to='pan_images')
    gts = models.FileField(upload_to='gts')
    registration = models.FileField(upload_to='registration')
    manager = models.CharField(max_length=75)
    manage_mobile = models.IntegerField()
    manager_email = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)
    account_number = models.IntegerField()
    ifsc_code = models.CharField(max_length=50)