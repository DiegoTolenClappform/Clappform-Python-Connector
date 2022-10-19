from .settings import settings
from .auth import Auth
import requests


class User:
    id = None

    def __init__(self, user=None):
        self.id = user

    def Create(clappformuri, email, firstname, lastname, phone, password):
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.post(
            clappformuri + "api/user",
            json={
                "email": email,
                "first_name": firstname,
                "last_name": lastname,
                "phone": phone,
                "password": password,
                "roles": ["public"],
            },
            headers={"Authorization": "Bearer " + settings.token},
        )

        if response.json()["code"] == 200:
            return response.json()
        else:
            return response.json()["message"]
