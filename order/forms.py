from django import forms
from django.utils.translation import gettext_lazy as _
from order.models import Order, UserAddress


class CheckOutOrderForm(forms.Form):
    address_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get('address_id')
        user = self.request.user
        try:
            address = UserAddress.objects.get(id=address_id, user=user)
        except UserAddress.DoesNotExist:
            raise forms.ValidationError(_('ادرس انتخواب شده معتبر نمیباشد'))
        return address
