# Standard lib modules
import unittest
from unittest.mock import patch

from .context import Clappform
from .settings import settings
from Clappform.notification import Notification

class TestNotification(unittest.TestCase):
    def setUp(self):
        # Set up all needed vars
        print("=====[ Setting up vars for Notification testing ]=====")
        self.url = settings.baseURL
        self.username = settings.username
        self.password = settings.password
        Clappform.Auth(baseURL=self.url, username=self.username, password=self.password)
        print("=====[ Done setting up vars for Notification testing ]=====")

    def test_read(self):
        print("=====[ Reading all Notification ]=====")
        rep = Notification.Read()
        assert rep is not None
        print("=====[ Done reading all Notification ]=====")

    def test_readOne(self):
        print("=====[ Reading one Notification ]=====")
        rep = Notification(1).ReadOne()
        assert rep is not None
        print("=====[ Done reading one Notification ]=====")

    def test_create(self):
        print("=====[ Sending Notification ]=====")
        rep = Notification.Create(user='d.tolen@clappform.com', content='Data has been updated', url='/app/default')
        print(rep)
        assert rep is not None
        print("=====[ Done sending Notification ]=====")

    def test_update(self):
        print("=====[ Updating Notification ]=====")
        rep = Notification(1).Update(is_opened=True)
        print(rep)
        assert rep is not None
        print("=====[ Done updating Notification ]=====")

    def test_zdelete(self):
        print("=====[ Deleting Notification ]=====")
        rep = Notification(1).Delete()
        print(rep)
        assert rep is True
        print("=====[ Done deleting Notification ]=====")

