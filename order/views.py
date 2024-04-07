from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from order.models import UserAddress
from order.permissions import HasCustomerAccessPermission


# Create your views here.


class CheckOutOrderView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddress.objects.filter(user=self.request.user)
        return context