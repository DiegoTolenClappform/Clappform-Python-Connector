# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from Clappform.app import App

class TestDataFrame(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for collection testing ]=====")
        self.url = "http://localhost/"
        self.username = ""
        self.password = ""
        self.app_id = "test_app"
        self.collection_id = "test_collection"
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)

    def test_read(self):
        print("=====[ Reading collection and creating dataframe ]=====")
        dataframe = App("clappform_logs").Collection("api_logs").DataFrame().Read(original=True, n_jobs = 1)
        print(dataframe)
        assert dataframe is not None
        print("=====[ Done reading collection and creating dataframe ]=====")