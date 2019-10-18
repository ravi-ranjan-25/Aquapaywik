from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class area(models.Model):
    areaid = models.CharField(max_length=10)
    areaName = models.CharField(max_length=256)

    def __str__(self):
        return self.areaid


class houseDetails(models.Model):
   
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    house_no = models.CharField(unique = True,max_length=256)
    street_name = models.CharField(max_length=256)
    pincode = models.IntegerField()
    time = models.DateTimeField(default = timezone.now())
    admin = models.BooleanField(default = 0)
    Area = models.ForeignKey(area, on_delete = models.CASCADE) 

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
    areaid = models.CharField(max_length=256,default=0)
    consumption = models.FloatField(default=0.00)
    time = models.DateTimeField(default = timezone.now())


class Complain(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    complaintxn = models.CharField(max_length=256,default = "COMP123")
    complain = models.CharField(max_length=256)
    time = models.DateTimeField(default = timezone.now())
    complainid = models.CharField(max_length=256) 
    status = models.BooleanField(default=0)

    def __str__(self):
        return self.complain     
   