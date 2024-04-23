from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from dashboard.mixins import HasCustomerAccessPermission
from shop.models import WishList


class CustomerProductWishlistListView(
    HasCustomerAccessPermission, LoginRequiredMixin, ListView
):
    template_name = "dashboard/customer/wishlists/wishlist-list.html"
    paginate_by = 10

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = WishList.objects.filter(user=self.request.user).count()
        return context


class CustomerWishlistDeleteView(
    LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, DeleteView
):
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:customer:wishlist-list-product")
    success_message = "محصول با موفقیت از لیست حذف شد"

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)
