from typing import Literal, Sequence

from .._utils import Pagination, build_expands, BoundApi

Expands = Literal["groups", "roles", "users"]
ALLOWED_EXPANDS = ["groups", "roles", "users"]


class Runs(BoundApi):

    def validate_run_id(self):
        return self._api.get("/user").json()
