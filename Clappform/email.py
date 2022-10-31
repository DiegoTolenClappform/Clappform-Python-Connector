from .settings import settings
from .auth import Auth
import requests
import os
import json


class Email:
    id = None

    def __init__(self, email=None):
        self.id = email

    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(
            settings.baseURL + "api/message?type=email",
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else:
                return []
        else:
            raise Exception(response.json()["message"])

    def ReadOne(self, extended=False):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(
            settings.baseURL + "api/message/" + str(self.id) + "?extended=" + extended,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])

    def Create(templateid, tojson, templatejson, fromjson):
        if not Auth.tokenValid():
            Auth.refreshToken()

        data = {
            "template_id": templateid,
            "personalizations": [
                {"to": [tojson], "dynamic_template_data": templatejson}
            ],
            "from": fromjson,
        }

        response = requests.get(
            settings.baseURL + "api/message/key",
            headers={"Authorization": "Bearer " + settings.token},
        )
        if response.status_code != 200:
            return "Not able to get API key"

        rep = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=data,
            headers={"Authorization": "Bearer " + response.json()["data"]["API_key"]},
        )

        if rep.status_code is 202:
            return "Mail is send"
        else:
            return rep.json()
