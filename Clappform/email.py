from .settings import settings
from .auth import Auth
import requests

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

class Email:
    id = None

    def __init__(self, email = None):
        self.id = email


    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/message?type=email', headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else:
                return []
        else:
            raise Exception(response.json()["message"])


    def ReadOne(self, extended = False):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(settings.baseURL + 'api/message/' + str(self.id) + '?extended=' + extended, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])


    def Create(recipientmail, recipientname, mailsubject, content):
        if not Auth.tokenValid():
            Auth.refreshToken()

        message = Mail()

        message.to = [
            To(
                email = recipientmail,
                name = recipientname,
            ),
        ]
        message.from_email = From(
            email="info@clappform.com",
            name="Clappform",
        )
        message.subject = mailsubject

        message.content = [
            Content(
                mime_type="text/html",
                content=content
            )
        ]

        SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))



