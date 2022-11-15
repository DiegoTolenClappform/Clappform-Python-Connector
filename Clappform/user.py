from .settings import settings
from .auth import Auth
import requests


class User:
    id = None

    def __init__(self, user=None):
        self.id = user

    def Create(email, firstname, lastname, phone, password, roles = ["public"], extra_information = {} ):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(
            settings.baseURL + "api/user",
            json={
                "email": email,
                "extra_information": extra_information,
                "first_name": firstname,
                "last_name": lastname,
                "phone": phone,
                "password": password,
                "roles": roles,
            },
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return response.json()
        else:
            return response.json()["message"]
