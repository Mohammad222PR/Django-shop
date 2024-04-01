from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse_lazy

from accounts.models import UserType


# Create your views here.


class DashBoardHomeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.superuser.value:
                return redirect(reverse_lazy("dashboard:admin:home"))
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy("dashboard:customer:home"))
            if request.user.type == UserType.support.value:
                return redirect(reverse_lazy("dashboard:support:home"))
        else:
            return redirect(reverse_lazy("accounts:login"))
        return super().dispatch(request, *args, **kwargs)
