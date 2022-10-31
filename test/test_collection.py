# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.app import App


class TestCollection(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for collection testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.collection_id = "test_collection"
        self.collection_name = "Test Collection"
        self.collection_desc = "This app gives ... insights on ... subject."
        self.collection_encryption = True
        self.collection_logging = True
        self.collection_sources = []
        self.collection_updated_name = "test case update"
        self.created_collection = ""
        self.updated_collection = ""
        self.deleted_collection = ""
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for collection testing ]=====")

    def test_readOne(self):
        print("=====[ Reading one collection in enviroment ]=====")
        print(App("clappform_logs").Collection("api_logs").ReadOne(extended=True))
        assert (
            App("clappform_logs").Collection("api_logs").ReadOne(extended=True)
            is not None
        )
        print("=====[ Done reading one collection in enviroment ]=====")

    def test_createOne(self):
        print("=====[ Creating one collection in enviroment ]=====")
        self.created_collection = (
            App("default")
            .Collection()
            .Create(
                slug=self.collection_id,
                name=self.collection_desc,
                description=self.collection_desc,
                encryption=self.collection_encryption,
                logging=self.collection_logging,
                sources=self.collection_sources,
            )
        )
        print(self.created_collection)
        assert self.created_collection is not None
        print("=====[ Done creating one collection in enviroment ]=====")

    def test_updateOne(self):
        print("=====[ Updating one collection in enviroment ]=====")
        self.updated_collection = (
            App("default")
            .Collection(self.collection_id)
            .Update(name=self.collection_updated_name)
        )
        print(self.updated_collection)
        assert self.updated_collection is not None
        print("=====[ Done updating one collection in enviroment ]=====")

    def test_zdeleteOne(
        self,
    ):  # Reason for the Z is so update goes first. unittesting works on alphabet
        print("=====[ Deleting one collection in enviroment ]=====")
        self.deleted_collection = App("default").Collection(self.collection_id).Delete()
        print(self.deleted_collection)
        assert self.deleted_collection is not None
        print("=====[ Done deleting one collection in enviroment ]=====")

    def test_lock(self):
        print("=====[ Locking one collection in enviroment ]=====")
        test = App("default").Collection(self.collection_id).Lock()
        print(test)
        assert test is not None
        print("=====[ Done locking one collection in enviroment ]=====")

    def test_unLock(self):
        print("=====[ Unlocking one collection in enviroment ]=====")
        test = App("default").Collection(self.collection_id).Unlock()
        print(test)
        assert test is not None
        print("=====[ Done unlocking one collection in enviroment ]=====")

    def test_empty(self):
        print("=====[ Emptying one collection in enviroment ]=====")
        test = App("default").Collection(self.collection_id).Empty()
        print(test)
        assert test is not None
        print("=====[ Done emptying one collection in enviroment ]=====")

    def test_query(self):
        print("=====[ Querying one collection in enviroment ]=====")
        test = (
            App("clappform_logs")
            .Collection("api_logs")
            .Query(filters={}, projection={}, sorting={}, original=True)
        )
        print(test)
        assert test is not None
        print("=====[ Done querying one collection in enviroment ]=====")

    def test_dataFrame(self):
        print("=====[ Getting dataframe of one collection in enviroment ]=====")
        test = App("clappform_logs").Collection("api_logs").DataFrame()
        print(test)
        assert test is not None
        print("=====[ Done getting dataframe of one collection in enviroment ]=====")
