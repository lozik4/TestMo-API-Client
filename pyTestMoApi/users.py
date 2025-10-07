# from .api_client import ApiClient
# from .utils import expands_validator, pagination_validator
#
#
# class Users:
#
#     def __init__(self):
#         self.client = ApiClient()
#         self.valid_expansions = ["groups", "roles", "users"]
#
#     def get_current_user(self):
#         return self.client.api_get("/user").json()
#
#     def get_users(self, page: int = 1, per_page: int = 100, expands: str = ""):
#         url = f"/users?page={page}"
#         url += pagination_validator(per_page)
#         url += expands_validator(expands, self.valid_expansions)
#         return self.client.api_get(url).json()
#
#     def get_users_by_id(self, user_id: int, expands: str = ""):
#         url = f"/users/{user_id}"
#         url += expands_validator(expands, self.valid_expansions)
#         return self.client.api_get(url).json()
#
#     def get_users_by_project_id(self, project_id: int, page: int = 1, per_page: int = 100):
#         url = f"/projects/{project_id}/users?page={page}"
#         url += pagination_validator(per_page)
#         return self.client.api_get(url).json()
