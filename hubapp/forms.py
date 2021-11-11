from django import forms
from .models import Devices
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm

class DeviceForm(forms.ModelForm):

    class Meta:
        model = Devices
        fields = ['id', 'device_name', 'device_type', 'device_model']
        widgets = {
            'device_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter your device name"}),
            'device_type': forms.Select(attrs={'class': "form-control", 'initial': "Select a device type"}),
            'device_model': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter your device model"}),
        }
        labels = {
            'device_name': 'Device Name',
            'device_type': 'Device Type',
            'device_model': 'Device Model',
        }

class UserForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',  'email']
