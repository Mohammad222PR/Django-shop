import requests
import json


class NovinoPay:
    _payment_request_url = "https://api.novinopay.com/payment/ipg/v2/request"
    _payment_verify_url = "https://api.novinopay.com/payment/ipg/v2/verification"
    _payment_page_url = "https://ipg.novinopay.com/StartPay/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, merchant_id="test"):
        self.merchant_id = merchant_id

    def payment_request(self, amount, description="پرداختی کاربر"):
        body = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "callback_url": self._callback_url,
            "description": description,
        }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        response = requests.post(
            self._payment_request_url, headers=headers, data=json.dumps(body)
        )

        return response.json()

    def payment_verify(self, amount, authority):
        body = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "authority": authority,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self._payment_verify_url, headers=headers, data=json.dumps(body)
        )
        return response.json()

    def generate_payment_url(self, authority):
        return f"{self._payment_page_url}{authority}"


if __name__ == "__main__":
    novinopay = NovinoPay(merchant_id="test")
    response = novinopay.payment_request(amount=15000)

    print(response)

    input("check the payment?")

    response = novinopay.payment_verify(amount=15000, authority=response["authority"])
    print(response)
