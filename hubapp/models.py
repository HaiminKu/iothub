from django.db import models

# Create your models here.

class Devices(models.Model):
    device_name = models.CharField(max_length=20, default="")
    type_choices = (
        ('sensor', 'sensor'),
        ('actuator', 'actuator'),
    )
    device_type = models.CharField(max_length=10, choices=type_choices)
    device_model = models.CharField(max_length=30, default="")
    last_updated = models.DateField(auto_now=True)
    registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.device_name

