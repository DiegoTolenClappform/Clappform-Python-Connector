# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for App testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.app_id = "test_app"
        self.app_name = "Test App"
        self.app_desc = "This app gives ... insights on ... subject."
        self.app_opts = {"spam": "eggs"}
        self.app_updated_name = "test case update"
        self.created_app = ""
        self.updated_app = ""
        self.deleted_app = ""
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for App testing ]=====")

    def test_readAll(self):
        print("=====[ Reading all apps in enviroment ]=====")
        print(App.Read(extended=True))
        assert App.Read(extended=True) is not None
        print("=====[ Done reading all apps in enviroment ]=====")

    def test_readOne(self):
        print("=====[ Reading one app in enviroment ]=====")
        print(App("default").ReadOne(extended=True))
        assert App("default").ReadOne(extended=True) is not None
        print("=====[ Done reading one app in enviroment ]=====")

    def test_createOne(self):
        print("=====[ Creating one app in enviroment ]=====")
        self.created_app = App.Create(
            id=self.app_id,
            name=self.app_name,
            description=self.app_desc,
            opts=self.app_opts,
        )
        print(self.created_app)
        assert self.created_app is not None
        print("=====[ Done creating one app in enviroment ]=====")

    def test_updateOne(self):
        print("=====[ Updating one app in enviroment ]=====")
        self.updated_app = App(self.app_id).Update(name=self.app_updated_name)
        print(self.updated_app)
        assert self.updated_app is not None
        print("=====[ Done updating one app in enviroment ]=====")

    def test_zdeleteOne(
        self,
    ):  # Reason for the Z is so update goes first. unittesting works on alphabet
        print("=====[ Deleting one app in enviroment ]=====")
        self.deleted_app = Clappform.App("test_app").Delete()
        print(self.deleted_app)
        assert self.deleted_app is not None
        print("=====[ Done deleting one app in enviroment ]=====")
