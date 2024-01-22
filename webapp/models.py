from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=20, unique=True, null=True)
    # avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'username'


class TimeInOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.date.today())
    time_start = models.CharField(max_length=50, null=True, blank=True, default=datetime.datetime.now().strftime('%I:%M %p'))
    time_end = models.CharField(max_length=50, null=True, blank=True)
    l_hd = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        ordering = ['user', 'date']


class GeneratedReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.date.today())
    time_start = models.CharField(max_length=50, null=True, blank=True)
    time_end = models.CharField(max_length=50, null=True, blank=True)
    l_hd = models.CharField(max_length=125, blank=True, null=True)

