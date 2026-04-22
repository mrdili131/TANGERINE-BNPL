from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='branches')
    desc = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class User(AbstractUser):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=250, default='NULLED NAME')
    born_in = models.DateField(null=True,blank=True)
    passport_serial = models.CharField(max_length=9,default="")
    passport_pinfl = models.CharField(max_length=14,default="")
    passport_got_date = models.DateField(null=True,blank=True)
    passport_expiry_date = models.DateField(null=True,blank=True)
    desc = models.TextField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if (self.last_name and self.first_name and self.middle_name):
            self.full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        super().save(*args,**kwargs)