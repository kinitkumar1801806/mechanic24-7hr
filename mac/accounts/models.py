from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_Accounts(models.Model):
    myuser=models.OneToOneField(User,unique=True,on_delete=models.CASCADE)
    address=models.CharField(max_length=300,default="")
    phone=models.IntegerField(default=0)
    image = models.ImageField(upload_to='shop/images/', default=" ")
    bio=models.CharField(max_length=3000,default="")
    vehicle=models.CharField(max_length=3000,default="")
    model=models.CharField(max_length=300,default="")
    dob=models.CharField(max_length=100,default="")

class Mechanic_Accounts(models.Model):
    mymechanic=models.OneToOneField(User,unique=True,on_delete=models.CASCADE)
    address=models.CharField(max_length=300,default="")
    phone=models.IntegerField(default=0)
    aadhar=models.IntegerField(default=0)
    mechanic_id=models.CharField(max_length=15,default='')
    image = models.ImageField(upload_to='shop/images/', default="")
    ratings=models.FloatField(default=0)
    expertat=models.CharField(max_length=1000,default="")
    avg_amt=models.IntegerField(default=0)
    bio=models.CharField(max_length=3000,default="")
    dob=models.CharField(max_length=100,default="")
    totalcustomer=models.IntegerField(default=0)
    totalsatisfiedcustomer=models.IntegerField(default=0)
    timeperiod=models.CharField(max_length=100,default="1 year")
    Experience=models.CharField(max_length=100,default="Beginner")

class Contact(models.Model):
    user_name=models.CharField(max_length=100,default='')
    mechanic_name=models.CharField(max_length=100,default='')
    mechanic_id=models.CharField(max_length=100,default='')
    rate=models.IntegerField(default=0)
    satisfied=models.CharField(max_length=100,default='')