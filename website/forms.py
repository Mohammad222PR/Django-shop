from django import forms
from django.shortcuts import redirect

from website.models import ContactUs, NewsLetter


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["first_name", "last_name", "email", "phone_number", "message"]


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if NewsLetter.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل در سیستم موجود است")
        return email
