import json
import os

from functools import reduce
from operator import getitem


class MockApi(object):
    """
    Mock db for keeping data between tests.
    """
    data = None
    app = None
    filepath = "payment.server.json"
    fixturepath = "fixtures/server.mock.json"

    def __init__(self, *args, **kwargs):
        """
        Initialize.
        """
        self.data = self.load()
        return super().__init__()

    def load(self, *args, **kwargs):
        """
        Loads data from file.
        """
        with open(self.filepath) as db:
            data = json.load(db)
        return data

    def update(self, data, *args, **kwargs):
        """
        Puts data into file.
        """
        with open(self.filepath, 'w') as db:
            db.write(json.dumps(data))
        return True

    def get(self, *args, **kwargs):
        """
        Gets the value from file or raise.
        """
        return reduce(getitem, args, self.data)

    def put(self, *args, **kwargs):
        """
        Puts the nth value to preceeding keys in file.
        """
        data, val, keys = self.data, args[-1], args[:-1]
        reduce(getitem, keys[:-1], data)[keys[-1]] = val
        self.update(data)

    def reset(self):
        """
        Resets all Payment Gateway to be available.
        """
        with open(self.fixturepath) as fixture:
            self.update(json.load(fixture))
