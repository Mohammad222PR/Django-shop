from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from dashboard.mixins.dashboard import CustomerDashBoardMixin


# Create your views here.


class CustomerDashBoardHomeView(CustomerDashBoardMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/customer/home.html'
