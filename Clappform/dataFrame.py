from .settings import settings
import pandas as pd
import json
import requests
import math
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

        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        data = []

        loopCount = math.ceil(response.json()["data"]["items"] / 500)
        for x in range(0, loopCount):
            response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '?extended=true&offset=' + str(x * 500), headers={
                'Authorization': 'Bearer ' + settings.token
            })

            for item in response.json()["data"]["items"]:
                data.append(item["data"])

        return pd.DataFrame(data)

        
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
        
        
    def Append(self, dataframe):
        if not Auth.tokenValid():
            Auth.refreshToken()
        
        dataframe.reset_index(inplace=True, drop=True)
        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if 'index' in dataframe:
            dataframe = dataframe.drop(columns=["index"])

        offset = response.json()["data"]["items"]
        count = 0
        for x in range(0 + offset, len(dataframe.index) + offset):
            if (count + 1) % 100 is 0:
                portion = dataframe.iloc[x - 99 - offset:x + 1 - offset]
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                     portion = portion.drop(columns=["index"])
                
                portion.index += offset + count - 99
                items = json.loads(portion.to_json(orient='index'))
                
                response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=items, headers={
                    'Authorization': 'Bearer ' + settings.token
                })
            elif len(dataframe.index) + offset == x + 1:
                portion = dataframe.tail(len(dataframe.index) - int(math.floor(len(dataframe.index) / 100.0)) * 100)
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                    portion = portion.drop(columns=["index"])
                
                portion.index += offset + count - 99
                items = json.loads(portion.to_json(orient='index'))
                
                response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=items, headers={
                    'Authorization': 'Bearer ' + settings.token
                })

            count += 1

        return True