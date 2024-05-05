import os
from .users import Users
from .sessions import Sessions
from .roles import Roles


class TestMoClient:
    def __init__(self, testmo_token: str = None, instance: str = None):
        self._set_env_variable('TESTMO_TOKEN', testmo_token)
        self._set_env_variable('TESTMO_INSTANCE', instance)
        self._users = Users()
        self._sessions = Sessions()
        self._roles = Roles()

    @staticmethod
    def _set_env_variable(var_name: str, value: str):
        if value:
            os.environ[var_name] = value
        if not os.getenv(var_name):
            raise ValueError(f"{var_name} is not set in environment variables")

    # Users
    def get_current_user(self):
        return self._users.get_current_user()

    def get_users(self, page: int = 1, per_page: int = 100, expands: str = ""):
        return self._users.get_users(page, per_page, expands)

    def get_users_by_id(self, user_id: int, expands: str = ""):
        return self._users.get_users_by_id(user_id, expands)

    def get_users_by_project_id(self, project_id: int, page: int = 1, per_page: int = 100):
        return self._users.get_users_by_project_id(project_id, page, per_page)

    # Sessions
    def get_session_info(self, session_id: int, expands: str = ""):
        return self._sessions.get_session_info(session_id, expands)

    def get_session_by_project(self, project_id: int, **kwargs):
        return self._sessions.get_session_by_project(project_id, **kwargs)

    # Roles
    def get_roles(self, page: int = 1, per_page: int = 100, expands: str = ""):
        return self._roles.get_roles(page, per_page, expands)

    def get_roles_by_id(self, role_id: int, expands: str = ""):
        return self._roles.get_role_by_id(role_id, expands)
