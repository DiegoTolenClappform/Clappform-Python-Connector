from .settings import settings
from .auth import Auth
import requests

class user:
    id = None

    def __init__(self, user = None):
        self.id = user

    def create(clappformuri, authpassword, email, firstname, lastname, phone, password):
        rep = requests.post(clappformuri + 'api/user/auth', json={
            'username': "public@clappform-system.com",
            'password': authpassword
        })

        token = rep.json()["data"]["access_token"]

        response = requests.post(clappformuri + 'api/user', json={
                'email': email,
                'first_name': firstname,
                'last_name': lastname,
                'phone': phone,
                'password': password,
                'roles': ["public"]
            }, headers={
                'Authorization': 'Bearer ' + token
            })

        if response.json()["code"] is 200:
            return "user created"
        else:
            raise Exception(response.json()["message"])