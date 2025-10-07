# from .api_client import ApiClient
# from .utils import expands_validator, pagination_validator
#
#
# class Projects:
#     def __init__(self):
#         self.client = ApiClient()
#         self.valid_expansions = ["users"]
#
#     def get_projects(self, page: int = 1, per_page: int = 100):
#         url = f"/projects?page={page}"
#         url += pagination_validator(per_page)
#         return self.client.api_get(url).json()
#
#     def get_project_info(self, project_id: int, expands: str = ""):
#         url = f"/projects/{project_id}?"
#         url += expands_validator(expands, self.valid_expansions)
#         return self.client.api_get(url).json()
