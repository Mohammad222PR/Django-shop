from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from review.models import Review, ReviewStatus
from dashboard.admin.forms import ProductForm, ProductImageForm
from dashboard.mixins.admin import HasAdminAccessPermission
from ..forms.reviews import ReviewForm
from dashboard.admin.mixins.reviews import ReviewUpdateFormMixin

class AdminReviewsListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/reviews/reviews-list.html"
    queryset = Review.objects.all().distinct()
    context_object_name = "reviews"
    paginate_by = 7

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = self.queryset
        request = self.request
        if order_by := request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by).distinct()
            except FieldError:
                pass
        if status := request.GET.get("status"):
            queryset = queryset.filter(status=status).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = Review.objects.all().distinct().count()
        context["status_types"] = ReviewStatus.choices
        return context


class AdminReviewsUpdateView(
    HasAdminAccessPermission ,ReviewUpdateFormMixin,LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/reviews/reviews-update.html"
    queryset = Review.objects.all()
    form_class = ReviewForm
    context_object_name = "review"
    success_message = "نظر با موفقیت بروز رسانی شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:reviews-update", kwargs={"pk": self.get_object().pk}
        )

    