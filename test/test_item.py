# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.app import App


class TestItem(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Item testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.app_id = "clappform_logs"
        self.collection_slug = "api_logs"
        self.item_name = "0"
        self.test_collection_slug = "test_collection_pypi"
        self.test_app_id = "default"
        self.test_item_id = "test_item"
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for Item testing ]=====")

    def test_readOne(self):
        print("=====[ Testing Item readOne ]=====")
        rep = (
            App(self.app_id)
            .Collection(self.collection_slug)
            .Item(self.item_name)
            .ReadOne()
        )
        print(rep)
        assert rep is not None
        print("=====[ Done testing Item readOne ]=====")

    def test_create(self):  # Test not able to see create function
        print("=====[ Testing Item create ]=====")
        App(self.test_app_id).Collection().Create(
            slug=self.test_collection_slug,
            name="Test Collection",
            description="This collection stores data about ... and is used in ...",
            encryption=False,
            logging=False,
            sources=[
                {"name": "Online resource", "link": "https://www.example.com/"},
                "Name without link",
            ],
        )
        rep = (
            Clappform.App(self.test_app_id)
            .Collection(self.test_collection_slug)
            .Item()
            .Create(id=self.test_item_id, data={"test_var": "value"})
        )
        print(rep)
        assert rep is not None
        print("=====[ Done testing Item create ]=====")

    def test_update(self):
        print("=====[ Testing Item update ]=====")
        rep = (
            Clappform.App(self.test_app_id)
            .Collection(self.test_collection_slug)
            .Item(self.test_item_id)
            .Update(data={"name": "new value"})
        )
        print(rep)
        assert rep is not None
        print("=====[ Done testing Item update ]=====")

    def test_zdelete(
        self,
    ):  # Reason for the Z is so update goes first. unittesting works on alphabet
        print("=====[ Testing Item delete ]=====")
        rep = (
            App(self.test_app_id)
            .Collection(self.test_collection_slug)
            .Item(self.test_item_id)
            .Delete()
        )
        print(rep)
        Clappform.App(self.test_app_id).Collection(self.test_collection_slug).Delete()
        assert rep is True
        print("=====[ Done testing Item delete ]=====")
