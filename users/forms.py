from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, UserSetting


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=24)
    last_name = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone"]


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ["notification_emails", "notification_sms"]
        labels = {
            "notification_emails": "Receive email notifications",
            "notification_sms": "Receive text notifications (phone number required)",
        }
        widgets = {
            "notification_emails": forms.CheckboxInput(),
            "notification_sms": forms.CheckboxInput(),
        }
