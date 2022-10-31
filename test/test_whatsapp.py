# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.whatsapp import Whatsapp


class TestWhatsapp(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Whatsapp testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for Whatsapp testing ]=====")

    def test_read(self):
        print("=====[ Reading all Whatsapp ]=====")
        rep = Whatsapp.Read()
        print(rep)
        assert rep is not None
        print("=====[ Done reading all Whatsapp ]=====")

    def test_readOne(self):
        print("=====[ Reading one Whatsapp ]=====")
        rep = Whatsapp(1).ReadOne()
        print(rep)
        assert rep is not None
        print("=====[ Done reading one Whatsapp ]=====")

    def test_create(self):
        print("=====[ Sending Whatsapp ]=====")
        rep = Whatsapp.Create(
            user="d.tolen@clappform.com", content="Data has been updated"
        )
        print(rep)
        assert rep is not None
        print("=====[ Done sending Whatsapp ]=====")
