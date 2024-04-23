from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import SubmitReviewForm
from .models import Review
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.


class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ["POST"]
    model = Review
    form_class = SubmitReviewForm

    def form_valid(self, form):
        product = form.cleaned_data.get("product")
        messages.success(
            self.request, "نظر شما با موفقیت ثبت شد بعد از بررسی نشان داده میشود"
        )
        return redirect(
            reverse_lazy("shop:product-detail", kwargs={"slug": product.slug})
        )

    def form_invalid(self, form):
        messages.error(
            self.request, "خطایی سمت دیدگاه اتفاق افتاد"
        )
        return redirect(reverse_lazy(self.request.META.get("HTTP_REFERER")))
