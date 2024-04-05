from django.contrib.auth import forms as auth_forms

from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile


class CustomerPasswordChangeForm(auth_forms.PasswordChangeForm):
    pass


class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "avatar", "phone_number"]
