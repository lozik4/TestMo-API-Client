class Runs:

    def __init__(self, client):
        self.__client = client

    def validate_run_id(self):
        return self.__client.get("/user").json()
