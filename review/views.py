from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import SubmitReviewForm
from .models import Review
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.


class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = Review
    form_class = SubmitReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data.get("product")
        messages.success(
            self.request,
            "دیدگاه شما با موفقیت ثبت شد و پس از بررسی نمایش داده خواهد شد",
        )
        return redirect(
            reverse_lazy("shop:product-detail", kwargs={"slug": product.slug})
        )

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get("HTTP_REFERER"))

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
