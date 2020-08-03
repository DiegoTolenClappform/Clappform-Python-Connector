from .settings import settings
from .auth import Auth
import requests

class Task:
    id = None

    def __init__(self, task = None):
        self.id = task


    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/task', headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else: 
                return []
        else:
            raise Exception(response.json()["message"])

    
    def ReadOne(self, extended = False):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(settings.baseURL + 'api/task/' + str(self.id) + '?extended=' + extended, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])
    
    
    def Create(name, description, user, is_completed = None, is_archived = None, due_date = None):
        if not Auth.tokenValid():
            Auth.refreshToken()

        properties = {
            "name": name,
            "description": description,
            "user": user
        }

        if is_completed is not None:
            properties["is_completed"] = is_completed

        if is_archived is not None:
            properties["is_archived"] = is_archived

        if due_date is not None:
            properties["due_date"] = due_date

        response = requests.post(settings.baseURL + 'api/task', json=properties, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return Task(id)
        else:
            raise Exception(response.json()["message"]) 


    def Update(self, name = None, description = None, user = None, is_completed = None, is_archived = None, due_date = None):
        if not Auth.tokenValid():
            Auth.refreshToken()

        properties = {}
        if name is not None:
            properties["name"] = name

        if description is not None:
            properties["description"] = description

        if user is not None:
            properties["user"] = user

        if is_completed is not None:
            properties["is_completed"] = is_completed

        if is_archived is not None:
            properties["is_archived"] = is_archived

        if due_date is not None:
            properties["due_date"] = due_date

        response = requests.put(settings.baseURL + 'api/task/' + self.id, json=properties, headers={
            'Authorization': 'Bearer ' + settings.token
        })

        if response.json()["code"] is 200:
            return Task(id)
        else:
            raise Exception(response.json()["message"])


    def Delete(self):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.delete(settings.baseURL + 'api/task/' + self.id, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return True
        else:
            raise Exception(response.json()["message"])


