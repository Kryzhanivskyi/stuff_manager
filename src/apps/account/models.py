from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from apps import model_choices as mch


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True) # TODO validate age >= 18
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    city = models.ForeignKey("account.City", on_delete=models.SET_NULL, blank=True, null=True, related_name="users")
    vacations_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    sickness_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0)

    @property
    def is_hr(self):
        return self.groups.filter(name='HR').exists()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=64, unique=True,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class ContactUs(models.Model):
    email = models.EmailField('email address', blank=True)
    title = models.CharField(max_length=64)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Contact us"


class RequestDayOffs(models.Model):
    status = models.PositiveSmallIntegerField(
        null=False, blank=False,
        choices=mch.STATUSES,
        default=mch.STATUS_PENDING,
    )
    created = models.DateTimeField(default=datetime.now)
    status_changed = models.DateTimeField(default=datetime.now)
    from_date = models.DateTimeField(null=False, blank=False)
    to_date = models.DateTimeField(null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        null=False, blank=False,
        choices=mch.REQUEST_TYPES,
        default=mch.REQUEST_SICKNESS,
    )
    reason = models.CharField(max_length=256, blank=True, null=True,
                              default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dayoffs')

    class Meta:
        verbose_name_plural = "Request day offs"

    def __str__(self):
        return f'status: {self.get_status_display()}, user: {self.user_id}'
