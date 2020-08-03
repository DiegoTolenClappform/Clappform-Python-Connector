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
        else:
            raise Exception(response.json()["message"])
        

