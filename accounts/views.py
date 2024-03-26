from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate
from accounts.admin import User
from accounts.forms import AuthenticationForm, RegisterForm
from accounts.mixins import RegisterViewMixin


# ____________START____________#
class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(RegisterViewMixin, View):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(email=cd['email'], password=cd['password'])
            user = authenticate(username=cd['email'], password=cd['password'])
            login(request, user)
            messages.success(request, 'اکانت شما با موفیت ساخته شد', 'success')
            return redirect('website:home')
        return render(request, self.template_name, {'form': form})


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = 'accounts/email/registration/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    success_url = reverse_lazy("accounts:password_reset_confirm")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
