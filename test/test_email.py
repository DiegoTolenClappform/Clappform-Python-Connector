# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.email import Email


class TestMail(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Mail testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        self.template_id = settings.twilliotemplate
        self.recipientname = "Tester"
        self.recipientmail = "newob01@hotmail.nl"
        self.mailsubject = "Your Example Order Confirmation"
        self.content = ""
        self.sender = "Clappform"
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for Mail testing ]=====")

    def test_read(self):
        print("=====[ Reading all mail ]=====")
        rep = Email.Read()
        assert rep is not None
        print("=====[ Done reading all mail ]=====")

    def test_readOne(self):
        print("Currently is readone from mail disabled as it is not being used")
        # print("=====[ Reading one mail ]=====")
        # rep = Email(1).ReadOne()
        # assert rep is not None
        # print("=====[ Done reading one mail ]=====")

    def test_create(self):
        templatejson = {
            "BODY": self.content,
            "SENDER": self.sender,
            "TO": self.recipientname,
            "SUBJECT": self.mailsubject,
        }

        tojson = {"name": self.recipientname, "email": self.recipientmail}

        fromjson = {
            "name": "Automatic testing pypi package",
            "email": "info@clappform.com",
        }
        print("=====[ Sending email ]=====")
        self.assertEqual(
            Email.Create(
                templateid=self.template_id,
                tojson=tojson,
                templatejson=templatejson,
                fromjson=fromjson,
            ),
            "Mail is send",
            "Should be correct message",
        )
        print("=====[ Done sending email ]=====")
