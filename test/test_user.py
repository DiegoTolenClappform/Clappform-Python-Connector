# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for user testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.email = settings.usertestingemail
        self.new_password = settings.usertestingpassword
        self.firstname = "Bowen"
        self.lastname = "Harkema"
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for user testing ]=====")

    def test_createUser(self):
        print("=====[ Testing user creation ]=====")
        rep = User.Create(
            clappformuri=self.url,
            email=self.email,
            firstname=self.firstname,
            lastname=self.lastname,
            phone="+31600000000",
            password=self.new_password,
        )
        print(rep)
        assert rep is not None
        print("=====[ Done testing user creation ]=====")
