import os
from ._modules import Users
from ._modules import Projects
from ._utils import ApiClient
from ._modules import Runs


class TestMoClient:
    """Testmo API client.

    Example:
        client = TestMoClient("token", "instance")
        users = client.users.get_users()
        projects = client.projects.get_projects()
    """
    __slots__ = ('_api', '_runs', '_users', '_projects')

    def __init__(self, testmo_token: str = None, instance: str = None):
        """Initialize the Testmo API client.

        Args:
            testmo_token: API token (or set TESTMO_TOKEN env var)
            instance: Instance name (or set TESTMO_INSTANCE env var)

        Raises:
            ValueError: If token or instance not provided
        """
        self._set_env_variable('TESTMO_TOKEN', testmo_token)
        self._set_env_variable('TESTMO_INSTANCE', instance)
        self._api = ApiClient()
        self._runs = Runs(self._api)
        self._users = Users(self._api)
        self._projects = Projects(self._api)

    @property
    def runs(self) -> Runs:
        """Get the Runs API module."""
        return self._runs

    @property
    def users(self) -> Users:
        """Get the Users API module."""
        return self._users

    @property
    def projects(self) -> Projects:
        """Get the Projects API module."""
        return self._projects

    @staticmethod
    def _set_env_variable(var_name: str, value: str) -> None:
        if value:
            os.environ[var_name] = value
        if not os.getenv(var_name):
            raise ValueError(f"{var_name} is not set in environment variables")
