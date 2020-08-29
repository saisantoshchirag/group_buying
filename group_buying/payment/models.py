from django.db import models

# Create your models here.
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    razorpayid = models.CharField(max_length=255,default="")
    razorpaypaymentid = models.CharField(max_length=255,default="")
    razorpaysignature = models.CharField(max_length=255, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."