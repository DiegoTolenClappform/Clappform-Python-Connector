from .settings import settings
from .collection import _Collection
from .auth import Auth
import requests


class App:
    id = None

    def __init__(self, app=None):
        self.id = app

    def Collection(self, name=None):
        return _Collection(self.id, name)

    def Read(extended=False):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(
            settings.baseURL + "api/apps?extended=" + extended,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
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
            settings.baseURL + "api/app/" + self.id + "?extended=" + extended,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])

    def Create(id, name, description, opts: dict):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(
            settings.baseURL + "api/app",
            json={"id": id, "name": name, "description": description, "settings": opts},
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return App(id)
        else:
            raise Exception(response.json()["message"])

    def Update(self, name=None, description=None, opts=None):
        if not Auth.tokenValid():
            Auth.refreshToken()

        properties = {}
        if name is not None:
            properties["name"] = name

        if description is not None:
            properties["description"] = description

        if opts is not None:
            properties["settings"] = opts

        response = requests.put(
            settings.baseURL + "api/app/" + self.id,
            json=properties,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return App(id)
        else:
            raise Exception(response.json()["message"])

    def Delete(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(
            settings.baseURL + "api/app/" + self.id,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return True
        else:
            raise Exception(response.json()["message"])
