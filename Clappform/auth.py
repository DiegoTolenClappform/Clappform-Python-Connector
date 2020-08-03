from .settings import settings
import requests
import base64
import time
import json

class Auth:
    def __init__(self, baseURL, username, password):
        settings.baseURL = baseURL
        global __USERNAME__
        global __PASSWORD__
        __USERNAME__ = username
        __PASSWORD__ = password
        

    def tokenValid():
        if '__TOKEN__' in globals():
            token_data = json.loads(base64.b64decode(__TOKEN__.split(".")[1] + "=="))
            return token_data["exp"] + 3600 > int(time.time())
        else:
            return False


    def refreshToken():
        response = requests.post(settings.baseURL + 'api/user/auth', json={
            'username': __USERNAME__,
            'password': __PASSWORD__
        })
        
        settings.token = response.json()["data"]["token"]

