from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy

from accounts.models import UserType
from dashboard.mixins.dashboard import AdminDashBoardMixin


# Create your views here.


class AdminDashBoardHomeView(AdminDashBoardMixin, LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/admin/home.html'
