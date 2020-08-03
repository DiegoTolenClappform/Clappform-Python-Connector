from .settings import settings
from .auth import Auth
import requests

class SMS:
    id = None

    def __init__(self, sms = None):
        self.id = sms


    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/message?type=sms', headers={'Authorization': 'Bearer ' + settings.token})

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

    
    def Create(user, content):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/message?type=sms', json={
            "user": user,
            "content": content
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return SMS(id)
        else:
            raise Exception(response.json()["message"]) 

