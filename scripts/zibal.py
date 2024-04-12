import json

import requests


class Zibal:
    _payment_request_url = "https://gateway.zibal.ir/v1/request"
    _payment_verify_url = "https://gateway.zibal.ir/v1/verify"
    _payment_page_url = "https://gateway.zibal.ir/start/"
    _callback_url = "https://gateway.zibal.ir/v1/verify"
    def __init__(self, merchant_id='zibal'):
        self.merchant_id = merchant_id

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
        return self._payment_page_url + str(trackId)


if __name__ == "__main__":
    zibal = Zibal(merchant_id="zibal")
    response = zibal.payment_request(amount=15000)

    print(response)
    input("proceed to generating payment url?")
    print(zibal.generate_payment_url(trackId=response["trackId"]))

    input("check the payment?")

    response = zibal.payment_verify(trackId=response["trackId"])
    print(response)
