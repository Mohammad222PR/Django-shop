from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.models import Product
from django.views.generic import TemplateView
from accounts.models import User
from dashboard.mixins.admin import HasAdminAccessPermission
from order.models import Order

# Create your views here.


class AdminDashBoardHomeView(
    HasAdminAccessPermission, LoginRequiredMixin, TemplateView
):
    template_name = "dashboard/admin/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = Product.objects.all().count()
        context["total_users"] = User.objects.all().count()
        context["total_orders"] = Order.objects.all().count()
        return context
