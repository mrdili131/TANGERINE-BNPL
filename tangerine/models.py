from django.db import models
from users.models import *
import uuid
import datetime


gender = [
    ('male','Erkak'),
    ('female','Ayol')
]

class Shop(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=150)
    stir = models.CharField(max_length=15,default="NONE")
    desc = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    middle_name = models.CharField(max_length=50,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=30,choices=gender,default='male')
    
    passport_serial = models.CharField(max_length=9,unique=True)
    passport_pinfl = models.CharField(max_length=14,unique=True)
    passport_got_date = models.DateField(null=True,blank=True)
    passport_expiry_date = models.DateField(null=True,blank=True)
    passport_got_region = models.CharField(max_length=100,null=True,blank=True)

    income = models.DecimalField(max_digits=10,decimal_places=0,default=0)

    full_name = models.CharField(max_length=250, default='NULLED NAME')
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True,related_name='clients')
    desc = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.full_name

class Application(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    name = models.CharField(max_length=100)
    length = models.IntegerField(default=12)
    interest = models.IntegerField(default=0)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Contract(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    client = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=0,default=0)
    application = models.ForeignKey(Application,on_delete=models.SET_NULL,null=True,blank=True)
    shop = models.ForeignKey(Shop,on_delete=models.SET_NULL,null=True,blank=True)
    pay_day = models.IntegerField(default=datetime.datetime.now().day)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

class MonthlyPayment(models.Model):
    pass

class PhoneNumber(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    client = models.ForeignKey(Client,on_delete=models.CASCADE,related_name='numbers')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)