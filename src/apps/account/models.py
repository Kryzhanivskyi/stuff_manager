from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)  # TODO validate age >= 18

    def __str__(self):
        return 'Name: {}    Last name: {}    Age: {}    Email: {} '.format(self.first_name, self.last_name, self.age, self.email)