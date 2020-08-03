from .settings import settings
from .auth import Auth
import requests

class _Item:
    app_id = None
    collection_id = None
    id = None

    def __init__(self, app, collection, item = None):
        self.app_id = app
        self.collection_id = collection
        self.id = item


    def ReadOne(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id  + '/' + self.collection_id + '/' + self.id, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])
        

    def Create(self, id, data):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, json={
            'id': id,
            'data': data
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return _Item(self.app_id, self.collection_id, id)
        else:
            raise Exception(response.json()["message"]) 


    def Update(self, data):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id  + '/' + self.collection_id + '/' + self.id, json={
            "data": data
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return _Item(self.app_id, self.collection_id, id)
        else:
            raise Exception(response.json()["message"])


    def Delete(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/metric/' + self.app_id  + '/' + self.collection_id + '/' + self.id, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])

