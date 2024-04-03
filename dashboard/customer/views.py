from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.contrib.auth import views as auth_views

from dashboard.customer.forms import CustomerPasswordChangeForm
from dashboard.mixins.dashboard import CustomerDashBoardMixin


# Create your views here.


class CustomerDashBoardHomeView(CustomerDashBoardMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/home.html'


class CustomerSecurityEditView(CustomerDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin,
                               auth_views.PasswordChangeView):
    template_name = 'dashboard/customer/profile/security-edit.html'
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message = "بروز رسانی پسورد با موفقیت انجام شد"
