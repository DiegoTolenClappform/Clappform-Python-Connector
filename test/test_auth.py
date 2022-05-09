# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from Clappform.auth import Auth as Auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Auth testing ]=====")
        self.url = "http://localhost/"
        self.username = ""
        self.password = ""
        print("=====[ Done setting up vars for Auth testing ]=====")

    def test_tokenInValid(self):
        print("=====[ Testing token check invalid ]=====")
        self.assertEqual(Auth.tokenValid(), False, "Should be False")
        print("=====[ Done testing token check invalid ]=====")

