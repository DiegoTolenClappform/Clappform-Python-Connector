from .settings import settings
from .auth import Auth
import requests
import json

class Model:
    id = None

    def _init_(self, model = None):
        self.id = model

    def Create_App(app, version):
        if not Auth.tokenValid():
            Auth.refreshToken()

        URI = "https://raw.githubusercontent.com/bharkema/clappform_models/main/Apps/" + app +"/" + version + "/_config.json"

        # Read files from Github Repo
        # Get Config file
        gitresponse = requests.get(URI)
        if gitresponse.status_code != 200:
            return "FILE NOT FOUND"

        config_json = gitresponse.json()

        if config_json["deployable"] == False:
            return "NOT DEPLOYABLE"

        timestamp = 0
        # Check config and get timestamp files.
        if "timestamp" in config_json:
            timestamp = config_json["timestamp"]

        timestamp_string = str(timestamp)

        # Config prints
        # print(config_json["timestamp"])
        # print(config_json["API_version"])
        # print(config_json["enviroment"])
        # print(config_json["enviroment_version"])
        # print(config_json["deployable"])
        # End config prints

        app_URI = "https://raw.githubusercontent.com/bharkema/clappform_models/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_app.json"
        collection_URI = "https://raw.githubusercontent.com/bharkema/clappform_models/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_collections.json"
        permission_URI = "https://raw.githubusercontent.com/bharkema/clappform_models/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_permission.json"

        git_app_response = requests.get(app_URI)
        if git_app_response.status_code != 200:
            return "FILE NOT FOUND"

        app_json = git_app_response.json()

        git_collection_response = requests.get(collection_URI)
        if git_collection_response.status_code != 200:
            return "FILE NOT FOUND"

        collection_json = git_collection_response.json()

        git_permission_response = requests.get(permission_URI)
        if git_permission_response.status_code != 200:
            return "FILE NOT FOUND"

        permission_json = git_permission_response.json()

        # Debug prints
        # print(app_json)
        # print(collection_json)
        # print(permission_json)
        # End Debug prints

        # Check validity
        try:
            test = json.dumps(app_json)
        except:
            return "Not able to dump json. App data might be broken"

        try:
            test = json.dumps(collection_json)
        except:
            return "Not able to dump json. Collection data might be broken"

        try:
            test = json.dumps(permission_json)
        except:
            return "Not able to dump json. permission data might be broken"

        # Send files to API for recontruction.
        # Python code mostly done need to make endpoints in API and then finish it up here.

        return 200



