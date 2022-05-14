# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for App testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for App testing ]=====")

    def test_createUser(self):
        print("Working on..")
