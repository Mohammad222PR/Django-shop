import requests
import json
from django.conf import settings


def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain


def get_protocol():
    return 'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"

    def __init__(self, merchant_id=None):
        self.merchant_id = merchant_id or settings.MERCHANT_ID
        self._callback_url = f"http://127.0.0.1:8000/payment/verify/zarin/"

    def payment_request(self, amount, description="پرداختی کاربر"):
        payload = {
            "MerchantID": self.merchant_id,
            "Amount": str(amount),
            "CallbackURL": self._callback_url,
            "Description": description,
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def payment_verify(self, amount, authority):
        payload = {
            "MerchantID": self.merchant_id,
            "Amount": amount,
            "Authority": authority
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, authority):
        return f"{self._payment_page_url}{authority}"
