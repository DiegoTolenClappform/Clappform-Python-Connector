from .settings import settings
from .dataFrame import _DataFrame
from .item import _Item
from .auth import Auth
import requests
import math
import pandas as pd


class _Collection:
    app_id = None
    id = None

    def __init__(self, app, collection=None):
        self.app_id = app
        self.id = collection

    def DataFrame(self):
        return _DataFrame(self.app_id, self.id)

    def Item(self, item=None):
        return _Item(self.app_id, self.id, item)

    def ReadOne(self, extended=0, original=True):
        if extended not in range(4):
            raise ValueError(f"extended not in {list(range(4))}, got {extended}")
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(
            settings.baseURL
            + "api/collection/"
            + self.app_id
            + "/"
            + self.id
            + "?extended="
            + extended
            + "&original="
            + str(original).lower(),
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] != 200:
            raise Exception(response.json()["message"])

        result = response.json()

        if extended == True:
            print(extended)
            data = []

            currentLoop = 0
            maxLoops = 1
            while currentLoop < maxLoops:
                response = requests.get(
                    settings.baseURL
                    + "api/collection/"
                    + self.app_id
                    + "/"
                    + self.id
                    + "?extended="
                    + extended
                    + "&offset="
                    + str(currentLoop * 500)
                    + "&original="
                    + str(original).lower(),
                    headers={"Authorization": "Bearer " + settings.token},
                )

                if "total" in response.json().keys():
                    maxLoops = math.ceil(response.json()["total"] / 500)

                    for item in response.json()["data"]["items"]:
                        data.append(item["data"])

                currentLoop += 1

            result["data"] = data

        return result

    def Create(self, slug, name, description, encryption, logging, sources=[]):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(
            settings.baseURL + "api/collection/" + self.app_id,
            json={
                "slug": slug,
                "name": name,
                "description": description,
                "encryption": encryption,
                "logged": logging,
                "sources": sources,
            },
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return _Collection(self.app_id, id)
        else:
            raise Exception(response.json()["message"])

    def Update(
        self,
        slug=None,
        name=None,
        description=None,
        encryption=None,
        logging=None,
        sources=None,
    ):
        if not Auth.tokenValid():
            Auth.refreshToken()

        properties = {}
        if name is not None:
            properties["name"] = name

        if slug is not None:
            properties["slug"] = slug

        if description is not None:
            properties["description"] = description

        if encryption is not None:
            properties["encryption"] = encryption

        if logging is not None:
            properties["is_logged"] = logging

        if sources is not None:
            properties["sources"] = sources

        response = requests.put(
            settings.baseURL + "api/collection/" + self.app_id + "/" + self.id,
            json=properties,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return _Collection(self.app_id, id)
        else:
            raise Exception(response.json()["message"])

    def Delete(self, slug=None, app=None, delete_modules=None):
        if not Auth.tokenValid():
            Auth.refreshToken()

        properties = {}
        if slug is not None:
            properties["overwrite_collection"] = slug

        if app is not None:
            properties["overwrite_app"] = app

        if delete_modules is not None:
            properties["delete_modules"] = True

        response = requests.delete(
            settings.baseURL + "api/collection/" + self.app_id + "/" + self.id,
            json=properties,
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            if "data" in response.json():
                raise Exception(response.json())
            return True
        else:
            raise Exception(response.json()["message"])

    def Empty(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(
            settings.baseURL
            + "api/collection/"
            + self.app_id
            + "/"
            + self.id
            + "/dataframe",
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return True
        else:
            raise Exception(response.json()["message"])

    def Lock(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.put(
            settings.baseURL + "api/collection/" + self.app_id + "/" + self.id,
            json={"locked": True},
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return True
        else:
            raise Exception(response.json()["message"])

    def Unlock(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.put(
            settings.baseURL + "api/collection/" + self.app_id + "/" + self.id,
            json={"locked": False},
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return True
        else:
            raise Exception(response.json()["message"])

    def Query(self, data_source: str, query: list, name: str, slug: str, **kwargs):
        if not Auth.tokenValid():
            Auth.refreshToken()

        data = []

        currentLoop = 0
        maxLoops = 1
        while currentLoop < maxLoops:
            body = {
                "data_source": data_source,
                "query": query,
                "name": name,
                "slug": slug,
                "app": self.app_id,
                "collection": self.id,
            }
            for kwarg, value in kwargs.items():
                body[kwarg] = value

            response = requests.post(
                settings.baseURL
                + "api/query?offset="
                + str(currentLoop * 500)
                + "&original="
                + str(original).lower(),
                json=body,
                headers={"Authorization": "Bearer " + settings.token},
            )

            if "total" in response.json().keys():
                maxLoops = math.ceil(response.json()["total"] / 500)

                for item in response.json()["data"]:
                    if projection:
                        data.append(item)
                    else:
                        data.append(item["data"])

            currentLoop += 1

        return data
