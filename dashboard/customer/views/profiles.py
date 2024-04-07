from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, UpdateView

from accounts.models import Profile
from dashboard.customer.forms.profiles import (
    CustomerPasswordChangeForm,
    CustomerProfileEditForm,
)
from dashboard.mixins.dashboard import CustomerDashBoardMixin


# Create your views here.


class CustomerSecurityEditView(
    CustomerDashBoardMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    auth_views.PasswordChangeView,
):
    template_name = "dashboard/customer/profile/security-edit.html"
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message = "بروز رسانی پسورد با موفقیت انجام شد"


class CustomerProfileEditView(
    CustomerDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/customer/profile/profile-edit.html"
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class CustomerProfileDeleteAvatarView(
    CustomerDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/customer/profile/profile-edit.html"
    fields = ("avatar",)
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "تصویر پروفایل با موفقیت حذف شد"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        profile = self.get_object()
        profile.avatar = "images/profile/customer/avatars/default/OIP.jfif"
        profile.save()
        return redirect(self.success_url)
