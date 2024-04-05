from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, UpdateView

from accounts.models import Profile
from dashboard.admin.forms.profiles import AdminPasswordChangeForm, AdminProfileEditForm
from dashboard.mixins.dashboard import AdminDashBoardMixin


# Create your views here.



class AdminSecurityEditView(
    AdminDashBoardMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    auth_views.PasswordChangeView,
):
    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "بروز رسانی پسورد با موفقیت انجام شد"


class AdminProfileEditView(
    AdminDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/profile/profile-edit.html"
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class AdminProfileDeleteAvatarView(
    AdminDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/profile/profile-edit.html"
    fields = ("avatar",)
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "تصویر پروفایل با موفقیت حذف شد"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        profile = self.get_object()
        profile.avatar = "images/profile/customer/avatars/default/OIP.jfif"
        profile.save()
        return redirect(self.success_url)
