from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView

from dashboard.admin.forms import AdminPasswordChangeForm
from dashboard.mixins.dashboard import AdminDashBoardMixin


# Create your views here.


class AdminDashBoardHomeView(AdminDashBoardMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/home.html'


class AdminSecurityEditView(AdminDashBoardMixin, LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, 'پسورد شما با موفقیت عوض شد')
        return super().form_valid(form)
