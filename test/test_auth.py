# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.auth import Auth as Auth


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Auth testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        print("=====[ Done setting up vars for Auth testing ]=====")

    def test_atokenInValid(self):
        print("=====[ Testing token check invalid ]=====")
        self.assertEqual(Auth.tokenValid(), False, "Should be False")
        print("=====[ Done testing token check invalid ]=====")

    def test_loginAuth(self):
        print("=====[ Testing login ]=====")
        rep = Auth(baseURL=self.url, username=self.username, password=self.password)
        print(rep)
        assert rep is not None
        print("=====[ Done testing login ]=====")
