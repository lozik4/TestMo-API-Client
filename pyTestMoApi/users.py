from .api_client import ApiClient


class Users:

    def __init__(self):
        self.client = ApiClient()

    def get_current_user(self):
        return self.client.api_get("/user").json()

    def get_users(self, page: int = 1, per_page: int = 100, expands: str = ""):
        if per_page not in [15, 25, 50, 100]:
            raise ValueError("per_page must be 15 or 25 or 50 or 100")
        url = f"/users?page={page}&per_page={per_page}"

        valid_expansions = ["groups", "roles", "users"]
        if expands and not all(item in valid_expansions for item in expands.split(",")):
            raise ValueError("expands must be 'groups' or 'roles' or 'users' or None")
        elif expands != "":
            url += f"&expands={expands}"

        return self.client.api_get(url).json()
