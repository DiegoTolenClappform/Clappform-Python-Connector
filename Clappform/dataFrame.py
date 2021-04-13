from .settings import settings
import pandas as pd
import numpy as np
import json
import requests
import math
import re
import time
from .auth import Auth
from sys import getsizeof
from datetime import datetime

class _DataFrame:
    app_id = None
    collection_id = None
    
    def __init__(self, app, collection):
        self.app_id = app
        self.collection_id = collection


    def Read(self, original = True, itemsPerRun = 500):
        if not Auth.tokenValid():
            Auth.refreshToken()

        data = []

        currentLoop = 0
        maxLoops = 1
        while currentLoop < maxLoops:
            response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '?extended=true&offset=' + str(currentLoop * itemsPerRun) + '&limit=' + str(itemsPerRun) + '&original=' + str(original).lower(), headers={
                'Authorization': 'Bearer ' + settings.token
            })
            
            if "total" in response.json().keys():
                maxLoops = math.ceil(response.json()["total"] / itemsPerRun)

                for item in response.json()["data"]["items"]:
                    data.append(item["data"])
            
            currentLoop += 1

        return pd.DataFrame(data)

        
    def Synchronize(self, dataframe):
        if not Auth.tokenValid():
            Auth.refreshToken()

        dataframe = dataframe.fillna(value=np.nan)

        for i in dataframe:
            try:
                if type(i) is str:
                    pass
                else:
                    raise TypeError
            except TypeError as error:
                print('The column {0} is not a string'.format(i))
                return dataframe

        # Makes all the columns lowercase
        dataframe = dataframe.rename(columns=str.lower)

        try:
            dataframe = dataframe.applymap(lambda x: pd.to_numeric(x, errors='ignore'))
        except:
            pass

        # removes all dubble spaces in column name
        dataframe.columns = dataframe.columns.str.replace('\s+s+', ' ', regex=True)
        # Replaces all spaces with underscores
        dataframe.columns = dataframe.columns.str.replace(' ', '_')
        # Replaces all 'streepjes' with underscores
        dataframe.columns = dataframe.columns.str.replace('-', '_')
        # Removes all spaces at the start and end
        dataframe.columns = dataframe.columns.str.strip()
        # removes all the values that Javascript doesnt allow
        dataframe.columns = dataframe.columns.str.replace('[^0-9_$a-z]', '', regex=True)

        # trimms all values
        dataframe = dataframe.applymap(lambda x: x.strip() if type(x) == str else x)
        dataframe = dataframe.applymap(lambda x: ' '.join(x.split()) if type(x) == str else x)

        for i in dataframe:
            l = i
            try:
                while re.match('[^_$a-z]', i[0]):
                    i = i[1:]
                dataframe.rename(columns={l: i}, inplace=True)
                if i != l:
                    print('{0} has been changed to {1}'.format(l, i))

            except IndexError as error:
                return 'the column {0} contais no letter, underscore or dollar sign'.format(l)
        try:
            dup_columns = dataframe.columns[dataframe.columns.duplicated()]
            if not dup_columns.any():
                pass
            else:
                raise TypeError
        except TypeError as error:
            dup_columns = list(set(dup_columns))
            return 'There are multiple column(s) %s' % dup_columns

        months = 'january|february|march|april|may|june|july|august|september|october|november|december'
        shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

        date_dict = {'((3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/([12][0-9]{3}))': '%d/%m/%Y',
                     '((1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/([12][0-9]{3}))': '%m/%d/%Y',
                     '(([12][0-9]{3})/(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0[1-9]))': '%Y/%m/%d',
                     '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
                     '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
                     '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
                     '(' + months + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
                     '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + months + ')': '%Y, %d %B',
                     '([12][0-9]{3}, (' + months + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
                     }

        strings = numbers = dates = lists = []

        for i in dataframe:
            try:
                a = dataframe[i].unique()
            except:
                dataframe[i] = dataframe[i].apply(lambda x: [x] if type(x) is not np.ndarray else x)
                lists.append(i)
            else:
                r = r"(" + ")|(".join(date_dict) + ")"
                if all(isinstance(element, (np.int64, np.float64, int, float)) for element in a):
                    numbers.append(i)
                elif all(isinstance(element, str) for element in a):
                    temp = []
                    for aa in a:
                        if re.match(r, aa, flags=re.IGNORECASE):
                            temp.append(aa)
                    if len(a) == len(temp):
                        dates.append(i)
                    else:
                        strings.append(i)
                else:
                    dataframe[i] = dataframe[i].apply(str)
                    strings.append(i)

        for i in dates:
            for k in date_dict.keys():
                dataframe[i] = dataframe[i].apply(
                    lambda x: time.mktime(datetime.strptime(x, date_dict[k]).timetuple()) if type(x) == str and (
                        re.match(k, x, flags=re.IGNORECASE)) else x)

        response = requests.put(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=json.loads(dataframe.to_json(orient='index')), headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.status_code == 413:
            raise Exception('To much data')

        elif response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])

    def Append(self, dataframe):
        if not Auth.tokenValid():
            Auth.refreshToken()

        dataframe = dataframe.fillna(value=np.nan)

        for i in dataframe:
            try:
                if type(i) is str:
                    pass
                else:
                    raise TypeError
            except TypeError as error:
                print('The column {0} is not a string'.format(i))
                return dataframe

        # Makes all the columns lowercase
        dataframe = dataframe.rename(columns=str.lower)

        try:
            dataframe = dataframe.applymap(lambda x: pd.to_numeric(x, errors='ignore'))
        except:
            pass

        # removes all dubble spaces in column name
        dataframe.columns = dataframe.columns.str.replace('\s+s+', ' ', regex=True)
        # Replaces all spaces with underscores
        dataframe.columns = dataframe.columns.str.replace(' ', '_')
        # Replaces all 'streepjes' with underscores
        dataframe.columns = dataframe.columns.str.replace('-', '_')
        # Removes all spaces at the start and end
        dataframe.columns = dataframe.columns.str.strip()
        # removes all the values that Javascript doesnt allow
        dataframe.columns = dataframe.columns.str.replace('[^0-9_$a-z]', '', regex=True)

        # trimms all values
        dataframe = dataframe.applymap(lambda x: x.strip() if type(x) == str else x)
        dataframe = dataframe.applymap(lambda x: ' '.join(x.split()) if type(x) == str else x)

        for i in dataframe:
            l = i
            try:
                while re.match('[^_$a-z]', i[0]):
                    i = i[1:]
                dataframe.rename(columns={l: i}, inplace=True)
                if i != l:
                    print('{0} has been changed to {1}'.format(l, i))

            except IndexError as error:
                return 'the column {0} contais no letter, underscore or dollar sign'.format(l)
        try:
            dup_columns = dataframe.columns[dataframe.columns.duplicated()]
            if not dup_columns.any():
                pass
            else:
                raise TypeError
        except TypeError as error:
            dup_columns = list(set(dup_columns))
            return 'There are multiple column(s) %s' % dup_columns

        months = 'january|february|march|april|may|june|july|august|september|october|november|december'
        shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

        date_dict = {'((3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/([12][0-9]{3}))': '%d/%m/%Y',
                     '((1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/([12][0-9]{3}))': '%m/%d/%Y',
                     '(([12][0-9]{3})/(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0[1-9]))': '%Y/%m/%d',
                     '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
                     '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
                     '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
                     '(' + months + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
                     '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + months + ')': '%Y, %d %B',
                     '([12][0-9]{3}, (' + months + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
                     }

        strings = numbers = dates = lists = []

        for i in dataframe:
            try:
                a = dataframe[i].unique()
            except:
                dataframe[i] = dataframe[i].apply(lambda x: [x] if type(x) is not np.ndarray else x)
                lists.append(i)
            else:
                r = r"(" + ")|(".join(date_dict) + ")"
                if all(isinstance(element, (np.int64, np.float64, int, float)) for element in a):
                    numbers.append(i)
                elif all(isinstance(element, str) for element in a):
                    temp = []
                    for aa in a:
                        if re.match(r, aa, flags=re.IGNORECASE):
                            temp.append(aa)
                    if len(a) == len(temp):
                        dates.append(i)
                    else:
                        strings.append(i)
                else:
                    dataframe[i] = dataframe[i].apply(str)
                    strings.append(i)

        for i in dates:
            for k in date_dict.keys():
                dataframe[i] = dataframe[i].apply(
                    lambda x: time.mktime(datetime.strptime(x, date_dict[k]).timetuple()) if type(x) == str and (
                        re.match(k, x, flags=re.IGNORECASE)) else x)

        dataframe.reset_index(inplace=True, drop=True)
        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if 'index' in dataframe:
            dataframe = dataframe.drop(columns=["index"])

        amountToSent = 100
        limit = 5000000 * 0.95 / 8

        averageSize = getsizeof(dataframe.to_json(orient="index")) / len(dataframe.index)
        amountSent = amountToSent if ((limit / averageSize) > amountToSent) else int(math.floor(limit / averageSize))

        offset = response.json()["data"]["items"]
        count = 0
        for x in range(0 + offset, len(dataframe.index) + offset):
            if (count + 1) % amountSent is 0:
                portion = dataframe.iloc[x - (amountSent - 1) - offset:x + 1 - offset]
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                     portion = portion.drop(columns=["index"])
                portion.index += offset + count + (amountSent + 1)
                items = json.loads(portion.to_json(orient='index'))
                
                response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=items, headers={
                    'Authorization': 'Bearer ' + settings.token
                })
            elif len(dataframe.index) + offset == x + 1:
                portion = dataframe.tail(len(dataframe.index) - int(math.floor(len(dataframe.index) / amountSent)) * amountSent)
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                    portion = portion.drop(columns=["index"])
                portion.index += offset + count + (amountSent + 1)
                items = json.loads(portion.to_json(orient='index'))
                response = requests.post(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe', json=items, headers={
                    'Authorization': 'Bearer ' + settings.token
                })

            count += 1

        return True

    
    def Query(self, filters = {}, projection = {}, sorting = {}, original = True):
        if not Auth.tokenValid():
            Auth.refreshToken()

        data = []

        currentLoop = 0
        maxLoops = 1
        while currentLoop < maxLoops:
            response = requests.post(settings.baseURL + 'api/metric/query?offset=' + str(currentLoop * 500) + '&original=' + str(original).lower(), json={
                "app": self.app_id,
                "collection": self.collection_id,
                "filter": filters,
                "projection": projection,
                "sorting": sorting
            }, headers={
                'Authorization': 'Bearer ' + settings.token
            })

            if "total" in response.json().keys():
                maxLoops = math.ceil(response.json()["total"] / 500)

                for item in response.json()["data"]:
                    data.append(item["data"])

            currentLoop += 1

        return pd.DataFrame(data)