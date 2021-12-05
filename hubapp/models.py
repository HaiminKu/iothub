from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Devices(models.Model):
    device_name = models.CharField(max_length=20, default="")
    type_choices = (
        ('sensor', 'sensor'),
        ('actuator', 'actuator'),
    )
    device_type = models.CharField(max_length=10, choices=type_choices)
    device_model = models.CharField(max_length=30, default="")
    last_updated = models.DateTimeField(auto_now=True)
    registered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devices',  on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.device_name

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=100)
    gender_type_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Not to say', 'Not to say'),
    )
    gender = models.CharField(max_length=10, choices=gender_type_choices)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following'
    )

class Activity(models.Model):
    activity_type_choices = (
        ('Follower', 'Follower'),
        ('Following', 'Following'),
        ('Add', 'Add'),
        ('Edit', 'Edit'),
        ('Delete', 'Delete')
    )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='creator')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='to')
    activity_type = models.CharField(max_length=20, choices=activity_type_choices)
    date = models.DateTimeField(auto_now_add=True)