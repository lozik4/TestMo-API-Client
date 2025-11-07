from ._api import ApiClient


class BoundApi:
    def __init__(self, client: ApiClient):
        self.__client = client

    @property
    def _api(self) -> ApiClient:
        return self.__client
