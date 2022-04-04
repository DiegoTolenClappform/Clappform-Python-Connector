from .settings import settings
from .auth import Auth
import requests
import os

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


    def Create(templateid, tojson, templatejson, fromjson):
        if not Auth.tokenValid():
            Auth.refreshToken()
            
        data = { 
            "template_id" : templateid,
            "personalizations": [{ 
                "to": [tojson],
                "dynamic_template_data": templatejson
            }],
            "from": fromjson
        }            
        
        rep = requests.post('https://api.sendgrid.com/v3/mail/send', json=data, headers={'Authorization': 'Bearer ' + os.getenv("SENDGRID_API_KEY")})

        if rep.json()["code"] is 202:
            return "email has been send."
        else:
            raise Exception(rep.json()["message"])

