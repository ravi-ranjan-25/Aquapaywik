from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class area(models.Model):
    areaid = models.CharField(max_length=10,default="areaid")
    areaName = models.CharField(max_length=256)

    def __str__(self):
        return self.areaName


class houseDetails(models.Model):
   
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    house_no = models.CharField(unique = True,max_length=256)
    street_name = models.CharField(max_length=256)
    pincode = models.IntegerField()
    time = models.DateTimeField(default = timezone.now())


    def __str__(self):
        return self.house_no


class areaQuantity(models.Model):
    areaN = models.ForeignKey(area, on_delete = models.CASCADE)
    quantity = models.FloatField(default=0.00)
    time = models.DateTimeField(default = timezone.now())

   

class quality(models.Model):
    quality = models.FloatField(default= 0.00)        
    time = models.DateTimeField(default = timezone.now())

  
class userConsumption(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    consumption = models.FloatField(default=0.00)
    time = models.DateTimeField(default = timezone.now())


class Complain(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    complain = models.CharField(max_length=256)
    time = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.complain     
   