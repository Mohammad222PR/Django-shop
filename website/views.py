from typing import Any
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from shop.models import ProductCategory
from shop.models import Product, ProductStatus
from website.forms import ContactForm, NewsLetterForm
from website.models import ContactUs, NewsLetter
from meta.views import MetadataMixin

# Create your views here.

class GeneralMeta(MetadataMixin):
    locale = 'fa_IR'

    def get_meta_url(self, context=None):
        return self.request.build_absolute_uri()
    
    def get_meta_og_title(self, context=None):
        return self.title
    
    def get_meta_twitter_title(self, context=None):
        return self.title
    
    def get_meta_schemaorg_title(self, context=None):
        return self.title
    
class IndexView(GeneralMeta,TemplateView):
    title = 'سایت فروشگاهی فرانتد'
    description = 'فروش انواع محصولات بهداشتی و پوشاک-'

    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        return context


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
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "پیام شما با موفیت ارسال شد")
            next_page = request.POST.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect("website:home")

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


class MegaMenuView(TemplateView):
    template_name = "inc/mega_menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        return context


def custom_404(request, exception):
    return render(request, '404/404.html', status=404)




    
