from .settings import settings
from .auth import Auth
import requests
import base64
import time
import json

class Actionflow:
    id = None

    def __init__(self, actionflow = None):
        self.id = actionflow

    def Start(actionflowid):
        if not Auth.tokenValid():
            Auth.refreshToken()

        json_body = {
            "actionflowid": actionflowid,
            "user": 2
        }

        response = requests.post(settings.baseURL + 'api/action_flow/start', json_body, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["message"]
        else:
            raise Exception(response.json()["message"])
