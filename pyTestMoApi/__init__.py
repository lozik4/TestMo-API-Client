from ._modules import Users, Projects, Runs
from ._utils import ApiClient


class TestMoClient:
    """Testmo API client.

    Example:
        client = TestMoClient("token", "instance")
        users = client.users.get_users()
        projects = client.projects.get_projects()
    """
    __slots__ = (
        "_api",
        "_runs",
        "_automation_runs",
        "_automation_sources",
        "_users",
        "_projects",
        "_groups",
        "_milestones",
        "_roles",
        "_sessions",
    )

    def __init__(self, testmo_token: str = None, instance: str = None):
        """Initialize the Testmo API client.

        Args:
            testmo_token: API token (or set TESTMO_TOKEN env var)
            instance: Instance name (or set TESTMO_INSTANCE env var)

        Raises:
            ValueError: If token or instance not provided
        """
        self._api = ApiClient(testmo_token, instance)
        self._users = Users(self._api)
        self._projects = Projects(self._api)
        self._runs = Runs(self._api)

    @property
    def users(self) -> Users:
        """Get the Users API module."""
        return self._users

    @property
    def projects(self) -> Projects:
        """Get the Projects API module."""
        return self._projects

    @property
    def runs(self) -> Runs:
        """Get the Runs API module."""
        return self._runs
