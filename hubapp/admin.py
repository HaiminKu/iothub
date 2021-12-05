from django.contrib import admin
from .models import Devices, CustomUser, Activity

admin.site.register(Devices)
admin.site.register(CustomUser)
admin.site.register(Activity)