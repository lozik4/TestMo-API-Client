import os
from ._modules import Users
from ._modules import Projects


# from .sessions import Sessions
# from .roles import Roles
# from .runs import Runs
# from .milestones import Milestones
# from .groups import Groups
# from .automation_sources import AutomationSources
# from .automation_runs import AutomationRuns


class TestMoClient:
    def __init__(self, testmo_token: str = None, instance: str = None):
        self._set_env_variable('TESTMO_TOKEN', testmo_token)
        self._set_env_variable('TESTMO_INSTANCE', instance)
        self.users = Users()
        self.projects = Projects()
        # self._sessions = Sessions()
        # self._roles = Roles()
        # self._runs = Runs()
        # self._projects = Projects()
        # self._milestones = Milestones()
        # self._groups = Groups()
        # self._automation_sources = AutomationSources()
        # self._automation_runs = AutomationRuns()

    @staticmethod
    def _set_env_variable(var_name: str, value: str):
        if value:
            os.environ[var_name] = value
        if not os.getenv(var_name):
            raise ValueError(f"{var_name} is not set in environment variables")

    # Sessions
    # def get_session_info(self, session_id: int, expands: str = ""):
    #     return self._sessions.get_session_info(session_id, expands)
    #
    # def get_session_by_project(self, project_id: int, **kwargs):
    #     return self._sessions.get_session_by_project(project_id, **kwargs)
    #
    # # Roles
    # def get_roles(self, page: int = 1, per_page: int = 100, expands: str = ""):
    #     return self._roles.get_roles(page, per_page, expands)
    #
    # def get_roles_by_id(self, role_id: int, expands: str = ""):
    #     return self._roles.get_role_by_id(role_id, expands)
    #
    # # Runs
    # def get_project_runs(self, project_id: int, page: int = 1, per_page: int = 100):
    #     return self._runs.get_project_runs(project_id, page, per_page)
    #
    # def get_run_info(self, run_id: int, expands: str = ""):
    #     return self._runs.get_run_info(run_id, expands)
    #
    #
    # # Milestones
    # def get_project_milestones(self, project_id: int, page: int = 1, per_page: int = 100):
    #     return self._milestones.get_project_milestones(project_id, page, per_page)
    #
    # def get_milestone_info(self, milestone_id: int, expands: str = ""):
    #     return self._milestones.get_milestone_info(milestone_id, expands)
    #
    # # Groups
    # def get_groups(self, page: int = 1, per_page: int = 100):
    #     return self._groups.get_groups(page, per_page)
    #
    # def get_group_info(self, group_id: int, expands: str = ""):
    #     return self._groups.get_group_info(group_id, expands)
    #
    # # AutomationSources
    # def get_automation_sources(self, project_id: int, page: int = 1, per_page: int = 100):
    #     return self._automation_sources.get_automation_sources(project_id, page, per_page)
    #
    # def get_automation_source_info(self, source_id: int, expands: str = ""):
    #     return self._automation_sources.get_automation_source_info(source_id, expands)
    #
    # # AutomationRuns
    # def get_automation_runs(self, project_id: int, page: int = 1, per_page: int = 100):
    #     return self._automation_runs.get_automation_runs(project_id, page, per_page)
    #
    # def get_automation_run_info(self, run_id: int, expands: str = ""):
    #     return self._automation_runs.get_automation_run_info(run_id, expands)


___all__ = ["TestMoClient"]