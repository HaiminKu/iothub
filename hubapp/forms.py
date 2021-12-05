from django import forms
from .models import Devices
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm, PasswordChangeForm

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['gender'].required = True

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2',  'first_name', 'last_name', 'email', 'nickname', 'gender']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        duplicate_email = CustomUser.objects.filter(email=email)
        if duplicate_email.exists():
            raise forms.ValidationError('This email address already exists.')
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'nickname', 'gender']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Current Password'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })