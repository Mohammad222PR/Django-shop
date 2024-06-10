from django.db.models import Sum, Avg
from django.utils.timezone import now
from django.views.generic import TemplateView
from shop.models import Product, ProductStatus
from order.models import Order, OrderStatus, OrderItem
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.models import Product
from accounts.models import User
from dashboard.mixins.admin import HasAdminAccessPermission
from order.models import Order



class AdminChartOrderView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name = "dashboard/admin/chart/chart_order.html"

    def get_total_order_price_per_month(self):
        return {
            f"chart_order_{month}": Order.objects.filter(
                created_date__year=now().year,
                created_date__month=month,
                status__in=[
                    OrderStatus.success.value,
                    OrderStatus.posted.value,
                    OrderStatus.delivered.value,
                ],
            ).aggregate(total_price=Sum("total_price"))["total_price"]
            or 0
            for month in range(1, 13)
        }

    def get_total_products_sold_per_month(self):
        return {
            f"chart_order_{month}": OrderItem.objects.filter(
                order__created_date__month=month,
                order__created_date__year=now().year,
                order__status__in=[
                    OrderStatus.success.value,
                    OrderStatus.posted.value,
                    OrderStatus.delivered.value,
                ],
            ).aggregate(total_products_sold=Sum("quantity"))["total_products_sold"]
            or 0
            for month in range(1, 13)
        }

    def get_famous_products(self):
        avg_famous_products = (
            Product.objects.aggregate(avg_famous=Avg("famous_percent"))["avg_famous"]
            or 0
        )
        return Product.objects.filter(
            status=ProductStatus.published.value,
            famous_percent__gte=avg_famous_products,
        )

    def total_user_created_account(self):
        return {
            f"chart_user_{month}": User.objects.filter(
                created_date__year=now().year, created_date__month=month
            ).count()
            for month in range(1, 13)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "total_order_price_per_month": self.get_total_order_price_per_month(),
                "famous_products": self.get_famous_products(),
                "total_products_sold_per_month": self.get_total_products_sold_per_month(),
                "total_user_created_account": self.total_user_created_account(),
            }
        )
        return context
