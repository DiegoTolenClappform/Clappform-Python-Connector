# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.file import File


class TestFile(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for File testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for File testing ]=====")

    def test_fileUpload(self):
        print("=====[ Testing File upload ]=====")
        # rep = File.Upload()
        # assert rep is not None
        print("=====[ Done testing File upload ]=====")

    def test_fileRead(self):
        print("=====[ Testing File reading ]=====")
        # rep = File.Read()
        # assert rep is not None
        print("=====[ Done testing File reading ]=====")

    def test_appendParquet(self):
        print("=====[ Testing File append ]=====")
        # rep = File.AppendParquet()
        # assert rep is not None
        print("=====[ Done testing File append ]=====")
