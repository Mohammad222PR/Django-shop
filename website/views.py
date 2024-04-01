from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView

from shop.models import Product, ProductStatus
from website.forms import ContactForm, NewsLetterForm
from website.models import ContactUs, NewsLetter


# Create your views here.


class IndexView(TemplateView):
    template_name = "website/index.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactUsView(View):
    """
    ContactUsView is for users to be able to communicate with us and raise their problems and questions
    """

    form_class = ContactForm
    template_name = "website/contact.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفیت ارسال شد")
            next_page = request.POST.get("next", "website:contact")
            return redirect(next_page)
        messages.error(request, "پیام ارسال نشد")
        return render(request, self.template_name, {"form": form})


class NewsletterView(View):
    """
    Newsletter View for sending email for Newsletter
    note:
    this view have one validation
    this validation check objects and if any object have same as the email sent
    raise error and redirect to main page
    """

    form_class = NewsLetterForm
    template_list_name = [
        "website/index.html",
        "shop/product-detail",
        "shop/product-grid",
    ]

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "با موفقیت ثبت نام کردید برای شما اخبار را ارسال خواهیم کرد"
            )

            # If 'next' parameter is not provided, redirect to the referrer page
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        return render(request, self.template_list_name, {"form": form})
