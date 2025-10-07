# from .api_client import ApiClient
# from .utils import expands_validator
#
#
# class Sessions:
#
#     def __init__(self):
#         self.client = ApiClient()
#         self.valid_expansions = ["configs", "field_values", "issues",
#                                  "milestones", "states", "statuses",
#                                  "templates", "users"]
#
#     def get_session_info(self, session_id: int, expands: str = ""):
#         url = f"/sessions/{session_id}?"
#         url += expands_validator(expands, self.valid_expansions)
#         return self.client.api_get(url).json()
#
#     def get_session_by_project(self, project_id: int, **kwargs):
#         url = f"/projects/{project_id}/sessions?"
#         if kwargs.get("expands"):
#             url += expands_validator(kwargs.pop("expands"), self.valid_expansions)
#         url += self.validate_and_serialize_parameters(**kwargs)
#         return self.client.api_get(url).json()
#
#     @staticmethod
#     def validate_and_serialize_parameters(**kwargs):
#
#         valid_types = {
#             "page": int,
#             "per_page": int,
#             "sort": str,
#             "order": str,
#             "assignee_id": str,
#             "closed_after": str,
#             "closed_before": str,
#             "config_id": str,
#             "created_after": str,
#             "created_before": str,
#             "created_by": str,
#             "is_closed": str,
#             "milestone_id": str,
#             "state_id": str,
#             "tags": str,
#             "template_id": str,
#         }
#
#         valid_values = {
#             "per_page": [15, 25, 50, 100],
#             "sort": ["sessions:created_at", "sessions:closed_at"],
#             "order": ["asc", "desc"],
#         }
#
#         for parameter, value in kwargs.items():
#             if parameter in valid_types and not isinstance(value, valid_types[parameter]):
#                 raise TypeError(f"Invalid type for {parameter}. Expected {valid_types[parameter]}.")
#
#             if parameter in valid_values and value not in valid_values[parameter]:
#                 raise ValueError(f"Invalid value for {parameter}. Expected one of {valid_values[parameter]}.")
#
#         return "&" + "&".join(f"{k}={str(v).lower()}" for k, v in kwargs.items())
