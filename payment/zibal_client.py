import json

import requests


class Zibal:
    _payment_request_url = "https://gateway.zibal.ir/v1/request"
    _payment_verify_url = "https://gateway.zibal.ir/v1/verify"
    _payment_page_url = "https://gateway.zibal.ir/start/"

    def __init__(self, merchant_id='zibal'):
        self.merchant_id = merchant_id
        self._callback_url = f"http://127.0.0.1:8000/payment/verify/zibal/"

    def payment_request(self, amount, description='پرداختی کاربر'):
        payload = {
            "merchant": self.merchant_id,
            "amount": str(amount),
            "callbackUrl": self._callback_url,
            "description": description,
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()

    def payment_verify(self, trackId):
        payload = {
            "merchant": self.merchant_id,
            "trackId": trackId
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, trackId):
        return f'{self._payment_page_url}{trackId}'

