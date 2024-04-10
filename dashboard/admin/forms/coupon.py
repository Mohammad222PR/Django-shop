from django import forms
from django.utils import timezone

from order.models import Coupon


class CouponValidationForm(forms.ModelForm):
    expired_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))

    class Meta:
        model = Coupon
        fields = [
            "code",
            "discount_percent",
            "max_limit_usage",
            "expired_date"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
        self.fields['max_limit_usage'].widget.attrs['class'] = 'form-control'

    def clean_discount_percent(self):
        discount_percent = self.cleaned_data['discount_percent']
        if discount_percent <= 0:
            raise forms.ValidationError('مقدار انتخواب شده برای درصد تخفیف نمیتواند برابر با صفر باشد')
        return discount_percent

    def clean_expired_date(self):
        expired_date = self.cleaned_data['expired_date']
        if expired_date == timezone.now():
            raise forms.ValidationError('کد تخفیف نمیتواند برابر با امروز باشد')
        return expired_date

