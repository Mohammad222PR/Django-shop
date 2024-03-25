from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView

from website.forms import ContactForm
from website.models import ContactUs


# Create your views here.

class IndexView(TemplateView):
    template_name = 'website/index.html'


class AboutView(TemplateView):
    template_name = 'website/about.html'


class ContactUsView(View):
    form_class = ContactForm
    template_name = 'website/contact.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفیت ارسال شد')
            return redirect('website:contact')
        return render(request, self.template_name, {'form': form})
