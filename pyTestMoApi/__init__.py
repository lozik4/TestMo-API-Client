from ._modules import (
    Attachments,
    AutomationCases,
    AutomationRuns,
    AutomationSource,
    Cases,
    Folders,
    Groups,
    Milestones,
    Projects,
    Results,
    Roles,
    Runs,
    Sessions,
    Users,
)
from ._utils import ApiClient


class TestMoClient:
    """Testmo API client.

    Example:
        client = TestMoClient("token", "instance")
        users = client.users.get_users()
        projects = client.projects.get_projects()
    """

    __slots__ = (
        "_client",
        "_runs",
        "_automation_runs",
        "_automation_sources",
        "_automation_cases",
        "_users",
        "_projects",
        "_groups",
        "_milestones",
        "_roles",
        "_sessions",
        "_results",
        "_cases",
        "_folders",
        "_attachments",
    )

    def __init__(self, testmo_token: str | None = None, instance: str | None = None):
        """Initialize the Testmo API client.

        Args:
            testmo_token: API token (or set TESTMO_TOKEN env var)
            instance: Instance name (or set TESTMO_INSTANCE env var)

        Raises:
            ValueError: If token or instance not provided
        """
        self._client = ApiClient(testmo_token, instance)
        self._users = Users(self._client)
        self._roles = Roles(self._client)
        self._projects = Projects(self._client)
        self._runs = Runs(self._client)
        self._results = Results(self._client)
        self._groups = Groups(self._client)
        self._milestones = Milestones(self._client)
        self._automation_runs = AutomationRuns(self._client)
        self._automation_sources = AutomationSource(self._client)
        self._automation_cases = AutomationCases(self._client)
        self._sessions = Sessions(self._client)
        self._cases = Cases(self._client)
        self._folders = Folders(self._client)
        self._attachments = Attachments(self._client)

    @property
    def users(self) -> Users:
        """Get the Users API module."""
        return self._users

    @property
    def roles(self) -> Roles:
        """Get the Roles API module."""
        return self._roles

    @property
    def projects(self) -> Projects:
        """Get the Projects API module."""
        return self._projects

    @property
    def runs(self) -> Runs:
        """Get the Runs API module."""
        return self._runs

    @property
    def results(self) -> Results:
        """Get the Results API module."""
        return self._results

    @property
    def groups(self) -> Groups:
        """Get the Groups API module."""
        return self._groups

    @property
    def milestones(self) -> Milestones:
        """Get the Milestones API module."""
        return self._milestones

    @property
    def automation_runs(self) -> AutomationRuns:
        """Get the AutomationRuns API module."""
        return self._automation_runs

    @property
    def automation_sources(self) -> AutomationSource:
        """Get the AutomationSource API module."""
        return self._automation_sources

    @property
    def automation_cases(self) -> AutomationCases:
        """Get the AutomationCases API module."""
        return self._automation_cases

    @property
    def sessions(self) -> Sessions:
        """Get the Sessions API module."""
        return self._sessions

    @property
    def cases(self) -> Cases:
        """Get the Cases API module."""
        return self._cases

    @property
    def folders(self) -> Folders:
        """Get the Folders API module."""
        return self._folders

    @property
    def attachments(self) -> Attachments:
        """Get the Attachments API module."""
        return self._attachments
