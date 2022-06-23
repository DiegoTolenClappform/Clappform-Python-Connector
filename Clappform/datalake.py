from .settings import settings
from .dataFrame import _DataFrame
from .item import _Item
from .auth import Auth
import requests
import pandas as pd


class DataLake:
    app_id = None
    collection_id = None

    def __init__(self, app=None, collection=None):
        self.app_id = app
        self.id = collection

    def GetAllCollections(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(f'{settings.baseURL}api/metric/get_all_collections/datalake',
                                   headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else:
                return []
        else:
            raise Exception(response.json()["message"])

    def GetAddPermissions(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(f'{settings.baseURL}api/metric/add_permissions/datalake',
                                   headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else:
                return []
        else:
            raise Exception(response.json()["message"])

    def DeleteApp(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + f'api/metric/delete_app/{self.app_id}',
                                   headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])

    def DeleteCollection(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + f'api/metric/delete_collection/{self.app_id}/{self.collection_id}',
                                   headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                raise Exception(response.json())
            return True
        else:
            raise Exception(response.json()["message"])
