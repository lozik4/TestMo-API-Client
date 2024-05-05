import os
from .users import Users


class TestMoClient:
    def __init__(self, testmo_token: str = None, instance: str = None):
        if testmo_token:
            os.environ['TESTMO_TOKEN'] = testmo_token
        if instance:
            os.environ['TESTMO_INSTANCE'] = instance
        if not os.getenv('TESTMO_INSTANCE') or not os.getenv('TESTMO_TOKEN'):
            raise ValueError("TESTMO_INSTANCE or TESTMO_TOKEN not install in env params")

        self._users = Users()

    def get_current_user(self):
        return self._users.get_current_user()

    def get_users(self, page: int = 1, per_page: int = 100, expands: str = ""):
        return self._users.get_users(page, per_page, expands)
