from django.contrib.auth import forms as auth_forms

from django import forms

from accounts.models import Profile


class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    pass


class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
