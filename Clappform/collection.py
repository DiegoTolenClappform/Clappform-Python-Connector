from .settings import settings
from .dataFrame import _DataFrame
from .item import _Item
from .auth import Auth
import requests

class _Collection:
    app_id = None
    id = None

    def __init__(self, app, collection = None):
        self.app_id = app
        self.id = collection

    
    def DataFrame(self):
        return _DataFrame(self.app_id, self.id)


    def Item(self, item = None):
        return _Item(self.app_id, self.id, item)


    def ReadOne(self, extended = False, original = True):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.id + '?extended=' + extended + '&original=' + str(original), headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])
        

    def Create(self, slug, name, description, encryption):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id, json={
            'slug': slug,
            'name': name,
            'description': description,
            'encryption': encryption
        }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return _Collection(self.app_id, id)
        else:
            raise Exception(response.json()["message"])


    def Update(self, slug = None, name = None, description = None, encryption = None):
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

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.id, json=properties, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return _Collection(self.app_id, id)
        else:
            raise Exception(response.json()["message"])


    def Delete(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/metric/' + self.app_id  + '/' + self.id, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])


    def Empty(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/metric/' + self.app_id  + '/' + self.id + '/dataframe', headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])

    
    def Lock(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.id, json={ "lock": True }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])


    def Unlock(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.id, json={ "lock": False }, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])


    def Query(self, filters = {}, projection = {}, sorting = {}, original = True):
        if not Auth.tokenValid():
            Auth.refreshToken()

        data = []

        loopCount = 1
        for x in range(0, loopCount):
            response = requests.post(settings.baseURL + 'api/metric/query?offset=' + str(x * 500) + '&original=' + str(original), json={
                "app": self.app_id,
                "collection": self.id,
                "filter": filters,
                "projection": projection,
                "sorting": sorting
            }, headers={
                'Authorization': 'Bearer ' + settings.token
            })
            loopCount = math.ceil(response.json()["total"] / 500)

            for item in response.json()["data"]["items"]:
                data.append(item["data"])

        return pd.DataFrame(data)