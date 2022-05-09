# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from Clappform.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for App testing ]=====")
        self.url = "http://localhost/"
        self.username = ""
        self.password = ""
        self.app_id = "test_app"
        self.app_name = "Test App"
        self.app_desc = "This app gives ... insights on ... subject."
        self.app_icon = "home-icon"
        self.app_updated_name = "test case update"
        self.created_app = ""
        self.updated_app = ""
        self.deleted_app = ""
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for App testing ]=====")

    def test_createUser(self):
        print("Working on..")
