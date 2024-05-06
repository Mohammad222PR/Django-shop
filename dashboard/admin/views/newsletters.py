from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from dashboard.mixins.admin import HasAdminAccessPermission
from ..forms.reviews import ReviewForm
from dashboard.admin.mixins.reviews import ReviewUpdateFormMixin
from accounts.models import User, UserType
from ..forms.users import UserForm
from django.db.models import F, Q
from website.models import ContactUs, NewsLetter


class AdminNewslettersListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/newsletters/newsletters-list.html"
    paginate_by = 7

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = NewsLetter.objects.all().distinct()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(Q(email__icontains=search_q))
        if order_by := self.request.GET.get("order_by", None):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_newletters"] = self.get_queryset().count()
        return context


class AdminNewslettersDeleteView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView
):
    template_name = "dashboard/admin/newsletters/newsletters-delete.html"
    success_url = reverse_lazy("dashboard:admin:newsletters-list")
    success_message = "عضو مورد نظر با موفقیت حذف شد"

    def get_queryset(self):
        return NewsLetter.objects.all()
