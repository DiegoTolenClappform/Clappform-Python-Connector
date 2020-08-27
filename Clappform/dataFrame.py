from .settings import settings
import pandas as pd
import json
import requests
from .auth import Auth

class _DataFrame:
    app_id = None
    collection_id = None
    
    def __init__(self, app, collection):
        self.app_id = app
        self.collection_id = collection


    def Read(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', headers={
            'Authorization': 'Bearer ' + settings.token
        })

        data = response.json()["data"]

        if response.json()["code"] is 200:
            return pd.DataFrame(data["data"],
                index=data["indices"],
                columns=data["columns"])
        else:
            raise Exception(response.json()["message"])
        

    def Synchronize(self, dataframe):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.put(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=json.loads(dataframe.to_json(orient='index')), headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return True
        if response.status_code is 413:
            raise Exception("Size of the data exceeds the maximum of 5MB, please use the append method instead.")
        else:
            raise Exception(response.json()["message"])


    def Append(self, dataframe):
        if not Auth.tokenValid():
            Auth.refreshToken()
        
        jsonObject = json.loads(dataframe.to_json(orient='index'))

        for id in jsonObject:
            response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, json={
                "id": id,
                "data": jsonObject[id]
            }, headers={
                'Authorization': 'Bearer ' + settings.token
            })

            if response.json()["code"] is 200:
                continue
            else:
                raise Exception(response.json()["message"])

        return True
