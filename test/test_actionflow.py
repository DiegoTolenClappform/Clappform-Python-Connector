# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.actionflow import Actionflow

class TestActionflow(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for App testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.actionflowid = 1
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for App testing ]=====")

    def test_actionFlow(self): # Need to ceck response for some reason no auth message comes back
        print("=====[ Starting actionflow ]=====")
        rep = Actionflow.Start(self.actionflowid)
        print(rep)
        assert rep is "Started action flow"
        print("=====[ Actionflow has been started ]=====")