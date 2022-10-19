# Standard lib modules
import unittest
from unittest.mock import patch
import pandas as pd

from .context import Clappform
from .settings import settings
from Clappform.collection import _Collection
from Clappform.app import App


class TestDataFrame(unittest.TestCase):
    global_dataframe_data = ""

    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for dataframe testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.app_id = "test_app"
        self.collection_id = "test_collection"
        self.dataframe_data = ""
        self.dataframe_query = ""

        # Vars for setting up an app and collection.
        self.app_id = "test_app"
        self.app_name = "Test App"
        self.app_desc = "This app gives ... insights on ... subject."
        self.app_icon = "home-icon"

        self.collection_id = "test_collection"
        self.collection_name = "Test Collection"
        self.collection_desc = "This app gives ... insights on ... subject."
        self.collection_encryption = True
        self.collection_logging = True
        self.collection_sources = []
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)

    ##### NOTES #####
    # I am adding letters to functions so the system will execute the tests in a certain order.

    def test_aread(self):
        print("=====[ Reading collection and creating dataframe ]=====")
        for result in (
            App("clappform_logs")
            .Collection("api_logs")
            .DataFrame()
            .Read(original=True, n_jobs=1)
        ):
            if result is not None:
                TestDataFrame.global_dataframe_data = result
        print(TestDataFrame.global_dataframe_data)
        assert TestDataFrame.global_dataframe_data is not None
        print("=====[ Done reading collection and creating dataframe ]=====")

    def test_bsync(self):
        print("=====[ Syncing collection and dataframe ]=====")
        App("default").Collection().Create(
            slug=self.collection_id,
            name=self.collection_desc,
            description=self.collection_desc,
            encryption=self.collection_encryption,
            logging=self.collection_logging,
            sources=self.collection_sources,
        )
        resp = (
            App("default")
            .Collection(self.collection_id)
            .DataFrame()
            .Synchronize(dataframe=TestDataFrame.global_dataframe_data, n_jobs=0)
        )
        assert resp is True
        print("=====[ Done Syncing collection and dataframe ]=====")

    def test_cappend(self):
        print("=====[ Appending collection and dataframe ]=====")
        resp = (
            App("default")
            .Collection(self.collection_id)
            .DataFrame()
            .Append(dataframe=TestDataFrame.global_dataframe_data, n_jobs=1, show=False)
        )
        assert resp is True
        print("=====[ Done appending collection and dataframe ]=====")

    def test_dquery(self):
        print("=====[ Querying collection and dataframe ]=====")
        self.dataframe_query = (
            App("default")
            .Collection(self.collection_id)
            .DataFrame()
            .Query(filters={}, projection={}, sorting={}, original=True)
        )
        print(self.dataframe_data)
        assert self.dataframe_data is not None
        print("=====[ Done querying collection and dataframe ]=====")

    def test_zdeleteOne(
        self,
    ):  # Reason for the Z is so update goes first. unittesting works on alphabet
        print("=====[ Deleting one collection in enviroment ]=====")
        self.deleted_collection = App("default").Collection(self.collection_id).Delete()
        print(self.deleted_collection)
        assert self.deleted_collection is not None
        print("=====[ Done deleting one collection in enviroment ]=====")
