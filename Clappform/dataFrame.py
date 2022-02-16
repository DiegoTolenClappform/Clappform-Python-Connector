from requests.models import Response
from .settings import settings
import pandas as pd
import numpy as np
import json
import requests
import math
import re
import time
import multiprocessing
from threading import Thread
from .auth import Auth
from sys import getsizeof
from datetime import datetime


class _DataFrame:
    app_id = None
    collection_id = None

    def __init__(self, app, collection):
        self.app_id = app
        self.collection_id = collection

    def Read(self, original=True, itemsPerRun=100, n_jobs = 1):

        self.data = []
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(
            settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '?extended=true&offset=' + str(
                0) + '&limit=' + str(itemsPerRun) + '&original=' + str(original).lower(),
            headers={
                'Authorization': 'Bearer ' + settings.token
            })

        for item in response.json()["data"]["items"]:
            self.data.append(item["data"])

        def Worker(self, i, itemsPerRun, original):
            if not Auth.tokenValid():
                Auth.refreshToken()
            response = ""

            try:
                response = requests.get(
                    settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '?extended=true&offset=' + str(
                    i * itemsPerRun) + '&limit=' + str(itemsPerRun) + '&original=' + str(original).lower(),
                    headers={
                        'Authorization': 'Bearer ' + settings.token
                })
                for item in response.json()["data"]["items"]:
                    self.data.append(item["data"])
            except:
                print(response.status_code)

        if n_jobs > multiprocessing.cpu_count() or n_jobs < -1:
            print("The maximum CPU which can be used is: {0}".format(multiprocessing.cpu_count()))
            return

        if n_jobs == -1:
            n_jobs = 16
            # n_jobs = multiprocessing.cpu_count()

        if "total" in response.json().keys():
            threadlist = []
            for i in range(1, math.ceil(response.json()["total"] / itemsPerRun)):
                threadlist.append(Thread(target=Worker, args=(self, i, itemsPerRun, original)))
                if i % n_jobs == 0:
                    for thread in threadlist:
                        thread.start()
                    for thread in threadlist:
                        thread.join()
                    threadlist = []
            for thread in threadlist:
                thread.start()
            for thread in threadlist:
                thread.join()

        return pd.DataFrame(self.data)

    def Synchronize(self, dataframe, n_jobs=1):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe',
                                   headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] == 200:
            df = dataframe.copy()
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

            # removes all double spaces in column name
            dataframe.columns = dataframe.columns.str.replace('\s?\s+', ' ', regex=True)
            # Replaces all spaces with underscores
            dataframe.columns = dataframe.columns.str.replace(' ', '_')
            # Replaces all 'streepjes' with underscores
            dataframe.columns = dataframe.columns.str.replace('-', '_')
            # Removes all spaces at the start and end
            dataframe.columns = dataframe.columns.str.strip()

            exceptions = {'ü': 'u', 'ä': 'a', 'ö': 'o', 'ë': 'e', 'ï': 'i', '%': '_procent_', '&': '_and_'}

            for v, k in exceptions.items():
                df.columns = df.columns.str.replace(v, k)

            df.columns = df.columns.str.replace('__', '_')

            # removes all the values that Javascript doesnt allow
            dataframe.columns = dataframe.columns.str.replace('[^0-9_$a-z]', '', regex=True)

            # trimms all values
            dataframe = dataframe.applymap(lambda x: x.strip() if type(x) == str else x)
            dataframe = dataframe.applymap(lambda x: ' '.join(x.split()) if type(x) == str else x)

            for i in dataframe:
                l = i
                try:
                    if re.match(r'[^_$a-z]', i[0]) or re.match(r'_', i[-1]):
                        while re.match(r'[^_$a-z]', i[0]):
                            i = i[1:]
                            if re.match(r'_', i[0]):
                                i = i[1:]

                        while re.match(r'_', i[-1]):
                            i = i[:-1]
                        df.rename(columns={original: i}, inplace=True)

                except IndexError as error:
                    return 'the column {0} contains no letter, underscore or dollar sign'.format(l)
            try:
                dup_columns = dataframe.columns[dataframe.columns.duplicated()]
                if not dup_columns.any():
                    pass
                else:
                    raise TypeError
            except TypeError as error:
                dup_columns = list(set(dup_columns))
                return 'There are multiple column(s) %s' % dup_columns

            monthname = 'january|february|march|april|may|june|july|august|september|october|november|december'
            shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

            day = r'((3[01]){1}|([12][0-9]){1}|(0?[1-9]){1}){1}'
            month = r'((1[0-2]){1}|(0?[1-9]){1}){1}'
            year = r'([12]{1}[0-9]{3}){1}'
            hms = r'(([2][0-3]){1}|([0-1][0-9]){1}){1}(:[0-5]{1}[0-9]{1}){2}'

            date_dict = {
                r'\b(' + year + '-{1}' + month + '-{1}' + day + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
                r'\b(' + year + '-{1}' + day + '-{1}' + month + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
                r'\b(' + day + '/{1}' + month + '/{1}' + year + r')\b': '%d/%m/%Y',
                r'\b(' + month + '/{1}' + day + '/{1}' + year + r')\b': '%m/%d/%Y',
                r'\b(' + year + '/{1}' + month + '/{1}' + day + r')\b': '%Y/%m/%d',
                '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
                '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
                '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
                '(' + monthname + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
                '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + monthname + ')': '%Y, %d %B',
                '([12][0-9]{3}, (' + monthname + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
            }

            strings = []
            numbers = []
            dates = []
            lists = []

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

            for index, (first, second) in enumerate(zip(df.columns, dataframe.columns)):
                if first != second:
                    print(first, 'has been changed to', second)

            dataframe.reset_index(inplace=True, drop=True)
            response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, headers={
                'Authorization': 'Bearer ' + settings.token
            })

            if 'index' in dataframe:
                dataframe = dataframe.drop(columns=["index"])

            def Worker(self, amountSent, offset, dataframe, count):
                if not Auth.tokenValid():
                    Auth.refreshToken()
                if (count + 1) % amountSent is 0:
                    portion = dataframe.iloc[x - (amountSent - 1) - offset:x + 1 - offset]
                    portion.reset_index(inplace=True, drop=True)
                    if 'index' in portion:
                        portion = portion.drop(columns=["index"])
                    portion.index += offset + count + (amountSent + 1)
                    items = json.loads(portion.to_json(orient='index'))

                    response = requests.post(
                        settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe',
                        json=items, headers={
                            'Authorization': 'Bearer ' + settings.token
                        })
                elif len(dataframe.index) + offset == x + 1:
                    portion = dataframe.tail(
                        len(dataframe.index) - int(math.floor(len(dataframe.index) / amountSent)) * amountSent)
                    portion.reset_index(inplace=True, drop=True)
                    if 'index' in portion:
                        portion = portion.drop(columns=["index"])
                    portion.index += offset + count + (amountSent + 1)
                    items = json.loads(portion.to_json(orient='index'))
                    response = requests.post(
                        settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe',
                        json=items, headers={
                            'Authorization': 'Bearer ' + settings.token
                        })

                count += 1

            amountToSent = 100
            limit = 5000000 * 0.95 / 8

            averageSize = getsizeof(dataframe.to_json(orient="index")) / len(dataframe.index)
            amountSent = amountToSent if ((limit / averageSize) > amountToSent) else int(
                math.floor(limit / averageSize))

            offset = response.json()["data"]["items"]
            count = 0
            threadlist = []
            for x in range(0 + offset, len(dataframe.index) + offset):
                threadlist.append(Thread(target=Worker, args=(self, amountSent, offset, dataframe, count)))
                if i % n_jobs == 0:
                    for thread in threadlist:
                        thread.start()
                    for thread in threadlist:
                        thread.join()
                    threadlist = []
            for thread in threadlist:
                thread.start()
            for thread in threadlist:
                thread.join()

            return True
        else:
            raise Exception(response.json()["message"])

    def Append(self, dataframe, n_jobs = 1, show = False):
        if not Auth.tokenValid():
            Auth.refreshToken()
        df = dataframe.copy()
        dataframe = dataframe.fillna(value=np.nan)

        if n_jobs > multiprocessing.cpu_count() or n_jobs < -1:
            print("The maximum CPU which can be used is: {0}".format(multiprocessing.cpu_count()))
            return

        if not isinstance(show, bool):
            print("show is supposed to be a boolean")
            return

        if n_jobs == -1:
            n_jobs = 16
            # n_jobs = multiprocessing.cpu_count()

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
        dataframe.columns = dataframe.columns.str.replace('\s+', ' ', regex=True)
        # Replaces all spaces with underscores
        dataframe.columns = dataframe.columns.str.replace(' ', '_')
        # Replaces all 'streepjes' with underscores
        dataframe.columns = dataframe.columns.str.replace('-', '_')
        # Removes all spaces at the start and end
        dataframe.columns = dataframe.columns.str.strip()

        exceptions = {'ü': 'u', 'ä': 'a', 'ö': 'o', 'ë': 'e', 'ï': 'i', '%': '_procent_', '&': '_and_', ' ': '_', '-': '_'}

        for v, k in exceptions.items():
            dataframe.columns = dataframe.columns.str.replace(v, k)

        # removes all the values that Javascript doesnt allow
        dataframe.columns = dataframe.columns.str.replace('[^0-9_$a-z]', '', regex=True)

        dataframe.columns = dataframe.columns.str.replace('_+', '_')

        # trimms all values
        dataframe = dataframe.applymap(lambda x: x.strip() if type(x) == str else x)
        dataframe = dataframe.applymap(lambda x: ' '.join(x.split()) if type(x) == str else x)


        for i in dataframe:
            l = i
            try:
                while re.match('[^$a-z]', i[0]):
                    i = i[1:]

                while re.match('_', i[-1]):
                    i = i[:-1]
                dataframe.rename(columns={l: i}, inplace=True)

            except IndexError as error:
                return 'the column {0} contains no letter, underscore or dollar sign'.format(l)
        try:
            dup_columns = dataframe.columns[dataframe.columns.duplicated()]
            if not dup_columns.any():
                pass
            else:
                raise TypeError
        except TypeError as error:
            dup_columns = list(set(dup_columns))
            return 'There are multiple column(s) %s' % dup_columns

        monthname = 'january|february|march|april|may|june|july|august|september|october|november|december'
        shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

        day = r'((3[01]){1}|([12][0-9]){1}|(0?[1-9]){1}){1}'
        month = r'((1[0-2]){1}|(0?[1-9]){1}){1}'
        year = r'([12]{1}[0-9]{3}){1}'
        hms = r'(([2][0-3]){1}|([0-1][0-9]){1}){1}(:[0-5]{1}[0-9]{1}){2}'

        date_dict = {
            r'\b(' + year + '-{1}' + month + '-{1}' + day + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
            r'\b(' + year + '-{1}' + day + '-{1}' + month + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
            r'\b(' + day + '/{1}' + month + '/{1}' + year + r')\b': '%d/%m/%Y',
            r'\b(' + month + '/{1}' + day + '/{1}' + year + r')\b': '%m/%d/%Y',
            r'\b(' + year + '/{1}' + month + '/{1}' + day + r')\b': '%Y/%m/%d',
            '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
            '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
            '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
            '(' + monthname + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
            '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + monthname + ')': '%Y, %d %B',
            '([12][0-9]{3}, (' + monthname + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
        }

        strings = []
        numbers = []
        dates = []
        lists = []

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

        if show == True:
            for index, (first, second) in enumerate(zip(df.columns, dataframe.columns)):
                if first != second:
                    print(first, 'has been changed to', second)

        dataframe.reset_index(inplace=True, drop=True)
        response = requests.get(settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if 'index' in dataframe:
            dataframe = dataframe.drop(columns=["index"])

        def Worker(amountSent, offset, dataframe, x):
            if not Auth.tokenValid():
                Auth.refreshToken()

            if x + amountSent < len(dataframe.index):
                portion = dataframe.iloc[x:x + amountSent]
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                    portion = portion.drop(columns=["index"])
                portion.index += offset - 99
                items = json.loads(portion.to_json(orient='index'))
                response = requests.post(
                    settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe',
                    json=items, headers={
                        'Authorization': 'Bearer ' + settings.token
                    })

            elif x + amountSent >= len(dataframe.index):
                portion = dataframe.iloc[x:len(dataframe.index)]
                portion.reset_index(inplace=True, drop=True)
                if 'index' in portion:
                    portion = portion.drop(columns=["index"])
                portion.index += offset - 99
                items = json.loads(portion.to_json(orient='index'))
                response = requests.post(
                    settings.baseURL + 'api/metric/' + self.app_id + '/' + self.collection_id + '/dataframe',
                    json=items, headers={
                        'Authorization': 'Bearer ' + settings.token
                    })

        amountToSent = 100
        limit = 5000000 * 0.95 / 8

        averageSize = getsizeof(dataframe.to_json(orient="index")) / len(dataframe.index)
        amountSent = amountToSent if ((limit / averageSize) > amountToSent) else int(math.floor(limit / averageSize))

        offset = response.json()["data"]["items"]
        threadlist = []

        for x in range(0, len(dataframe.index), amountSent):
            offset = offset + amountSent
            threadlist.append(Thread(target=Worker, args=(amountSent, offset, dataframe, x)))
            if x % n_jobs == 0:
                for thread in threadlist:
                    thread.start()
                for thread in threadlist:
                    thread.join()
                threadlist = []
        for thread in threadlist:
            thread.start()
        for thread in threadlist:
            thread.join()

        return True

    def Query(self, filters={}, projection={}, sorting={}, original=True):
        if not Auth.tokenValid():
            Auth.refreshToken()

        monthname = 'january|february|march|april|may|june|july|august|september|october|november|december'
        shortmonts = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|march|april|june|july'

        day = r'((3[01]){1}|([12][0-9]){1}|(0?[1-9]){1}){1}'
        month = r'((1[0-2]){1}|(0?[1-9]){1}){1}'
        year = r'([12]{1}[0-9]{3}){1}'
        hms = r'(([2][0-3]){1}|([0-1][0-9]){1}){1}(:[0-5]{1}[0-9]{1}){2}'

        date_dict = {
            r'\b(' + year + '-{1}' + month + '-{1}' + day + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
            r'\b(' + year + '-{1}' + day + '-{1}' + month + ' ' + hms + r')\b': '%Y-%m-%d %H:%M:%S',
            r'\b(' + day + '/{1}' + month + '/{1}' + year + r')\b': '%d/%m/%Y',
            r'\b(' + month + '/{1}' + day + '/{1}' + year + r')\b': '%m/%d/%Y',
            r'\b(' + year + '/{1}' + month + '/{1}' + day + r')\b': '%Y/%m/%d',
            '((3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([12][0-9]{3}))': '%d-%m-%Y',
            '((1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])-([12][0-9]{3}))': '%m-%d-%Y',
            '(([12][0-9]{3})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0[1-9]))': '%Y-%m-%d',
            '(' + monthname + ' (3[01]|[12][0-9]|[1-9]), ([12][0-9]{3}))': '%B %d, %Y',
            '(([12][0-9]{3}), (3[01]|[12][0-9]|[1-9]) ' + monthname + ')': '%Y, %d %B',
            '([12][0-9]{3}, (' + monthname + ') (3[01]|[12][0-9]|[1-9]))': '%Y, %B %d',
        }

        r = r"(" + ")|(".join(date_dict) + ")"
        data = []

        if filters:
            temp_date_list = []
            temp_unix_list = []

            # convert to string
            filters = json.dumps(filters)
            print(filters)
            for k, v in date_dict.items():
                temp_date = re.findall(k, filters)
                for i in temp_date:
                    for dates in i:
                        if re.match(k, dates, flags=re.IGNORECASE):
                            temp_unix_list.append(time.mktime(datetime.strptime(dates, v).timetuple()))
                            temp_date_list.append(dates)

            print(temp_date_list)
            print(temp_unix_list)

            for index, (first, second) in enumerate(zip(temp_date_list, temp_unix_list)):
                filters = filters.replace("\"" + first + "\"", str(second))

            # dataframe[i] = dataframe[i].apply(
            #     lambda x: time.mktime(datetime.strptime(x, date_dict[k]).timetuple()) if type(x) == str and (
            #         re.match(k, x, flags=re.IGNORECASE)) else x)

            # load to dict
            filters = json.loads(filters)
            print(filters)

        currentLoop = 0
        maxLoops = 1
        while currentLoop < maxLoops:
            response = requests.post(
                settings.baseURL + 'api/metric/query?offset=' + str(currentLoop * 500) + '&original=' + str(
                    original).lower(), json={
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

    def DeleteItems(self, ItemIDArray=[]):
        if not Auth.tokenValid():
            Auth.refreshToken()
        
        if len(ItemIDArray) > 0:

            x = {
                "data": ItemIDArray
            }        
                    
            itemIDString = json.dumps(x)

            response = requests.delete(settings.baseURL + "api/item/" + self.app_id + "/" + self.collection_id +"/dataframe",
                        json={
                            "content": itemIDString
                        },
                        headers={
                            'Authorization': 'Bearer ' + settings.token
                        })
        else:
            raise Exception('No IDs to delete')

        return response
