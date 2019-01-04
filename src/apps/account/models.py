from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True) # TODO validate age >= 18
    city = models.ForeignKey("account.City", on_delete=models.SET_NULL())

#class City(models.Model):
#    name = 