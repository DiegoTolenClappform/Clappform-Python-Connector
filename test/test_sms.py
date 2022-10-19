# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.sms import SMS


class TestSMS(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Mail testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for Mail testing ]=====")

    def test_read(self):
        print("=====[ Reading all SMS ]=====")
        rep = SMS.Read()
        assert rep is not None
        print("=====[ Done reading all SMS ]=====")

    def test_readOne(self):
        print("=====[ Reading one SMS ]=====")
        rep = SMS(1).ReadOne()
        assert rep is not None
        print("=====[ Done reading one SMS ]=====")

    def test_create(self):
        print("=====[ Sending SMS ]=====")
        rep = SMS.Create(user="d.tolen@clappform.com", content="Data has been updated")
        print(rep)
        assert rep is not None
        print("=====[ Done sending SMS ]=====")
