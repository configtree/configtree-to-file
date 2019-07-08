import requests
import json

BASE_PATH = "http://host.docker.internal:8000"


class Client(object):
    """
    ConfigTree API client
    """

    def __init__(self, email=None, orgslug=None, password=None):
        self.email = email
        self.orgslug = orgslug
        self.password = password
        self.access_token = None
        self.refresh = None

    def get_auth_token(self):
        data = {
            "email": self.email,
            "organizationSlug": self.orgslug,
            "password": self.password
        }

        response = requests.post(
            url=BASE_PATH + "/v1/login/",
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(data)
        )

        jsonrsp = json.loads(response.content)
        if 200 <= response.status_code <= 299:
            self.access_token = jsonrsp.get('access', None)
            self.refresh = jsonrsp.get('refresh', None)
            return jsonrsp
        return {"error": "Failed to get token. Please make sure username, password, and orgslug are correct"}

    def get_config(self, application=None, environment=None, version=None):

        params = {
            "applicationName": application,
            "environmentName": environment,
        }

        if version:
            params["versionName"] = version

        response = requests.get(
            url=BASE_PATH + "/v1/" + self.orgslug + "/versions/",
            params=params,
            headers={"Authorization": "Bearer " + self.access_token}
        )

        jsonrsp = json.loads(response.content)
        if 200 <= response.status_code <= 299:
            return jsonrsp.get('configuration', dict()).get('document', dict())
        return {"error": "Could not retrieve configurations. Please make sure the application, " +
                         "environment and version is correct"}

