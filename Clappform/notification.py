from .settings import settings
from .auth import Auth
import requests

class Notification:
    id = None

    def __init__(self, task = None):
        self.id = task


    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/message?type=notification', headers={'Authorization': 'Bearer ' + settings.token})

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
    
    
    def Create(user, content, url):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/message?type=notification', json={
            "user": user,
            "url": url,
            "content": content
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return Notification(id)
        else:
            raise Exception(response.json()["message"]) 


    def Update(self, is_opened):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.put(settings.baseURL + 'api/message/' + self.id, json={
            "is_opened": is_opened
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return Notification(id)
        else:
            raise Exception(response.json()["message"])


    def Delete(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/message/' + self.id, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])


