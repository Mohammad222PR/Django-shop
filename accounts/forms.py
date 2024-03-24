from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import User


class AuthenticationForm(auth_forms.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("کار بر تایید نشده است")


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confrim Password', widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('ایمیل شما در شبکه موجود است لطفا ایمیل دیگری استفاده کنید')
        return email

    def clean(self):
        cd = super().clean()
        password = cd.get('password1')
        password2 = cd.get('password2')
        if password and password2 and password != password2:
            raise ValidationError('پسورد شما هماهنگ نیست لطفا دوباره تلاش کنید')
