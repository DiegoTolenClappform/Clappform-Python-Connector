import json
import unittest
from unittest.mock import patch, MagicMock


from .context import Clappform
from Clappform.worker import Worker


class TestWorker(unittest.TestCase):
    """docstring for TestWorker."""

    def setUp(self):
        self.valid_dict = {
            "redis_uri": "redis://redis:6379",
            "userid": 1,
            "action_flow": 1,
            "env": "https://test.clappform.com",
        }
        self.worker = Worker(
            self.valid_dict["env"],
            self.valid_dict["action_flow"],
            self.valid_dict["userid"],
            self.valid_dict["redis_uri"],
        )
        Clappform.worker.os.getenv = MagicMock()

    def test_from_getenv_undefined(self):
        """Test if `from_getenv` raises TypeError undefined env var."""
        Clappform.worker.os.getenv.return_value = None
        value = "PLACEHOLDER"
        with self.assertRaises(TypeError):
            w = Worker.from_getenv(value)
        Clappform.worker.os.getenv.assert_called_once_with(value)

    def test_from_getenv_empty(self):
        """Test if `from_getenv` raises ValueError with empty env var."""
        Clappform.worker.os.getenv.return_value = ""
        with self.assertRaises(ValueError):
            w = Worker.from_getenv("PLACEHOLDER")

    def test_from_getenv_json_object(self):
        """Test if `from_getenv` checks for value to be json object."""
        # Only lists `[]` and objects `{}` are valid json values.
        Clappform.worker.os.getenv.return_value = '["spam", "eggs"]'
        with self.assertRaises(TypeError):
            w = Worker.from_getenv("PLACEHOLDER")

    def test_from_getenv_invalid_obj(self):
        """Test if `from_getenv` checks if certain keys exist."""
        for key in self.valid_dict.keys():
            invalid_dict = self.valid_dict.copy()
            invalid_dict.pop(key)
            Clappform.worker.os.getenv.return_value = json.dumps(invalid_dict)
            with self.assertRaises(KeyError):
                w = Worker.from_getenv("PLACEHOLDER")

    def test_from_getenv_valid_json_obj(self):
        """Test if `from_getenv` returns Worker class instance."""
        Clappform.worker.os.getenv.return_value = json.dumps(self.valid_dict)
        w = Worker.from_getenv("PLACEHOLDER")
        self.assertIsInstance(w, Worker)
