from .settings import settings
from .auth import Auth
import requests
import json
from github import Github
import time

class Model:
    id = None

    def _init_(self, model = None):
        self.id = model

    def Create_App(app, version):
        if not Auth.tokenValid():
            Auth.refreshToken()
        gitUrl = "https://raw.githubusercontent.com/bharkema/clappform_models"
        URI = gitUrl + "/main/Apps/" + app +"/" + version + "/_config.json"
        gitresponse = requests.get(URI)
        if gitresponse.status_code != 200:
            print("ERROR: FILE NOT FOUND")

        # Check if app is delpoyable
        config_json = gitresponse.json()
        print(config_json)

        if config_json["deployable"] == False:
            print("NOT DEPLOYABLE RAISING ERROR")
            raise Exception('Not deployable')

        version_url = settings.baseURL + "api/version"
        version_response = requests.get(version_url,headers={
                'Authorization': 'Bearer ' + settings.token
        })
        if version_response.status_code != 200:
            print("Not able to get version")
            print(version_response.json())
            raise Exception('Not deployable')

        version_json = version_response.json()["data"]
        if(config_json["web_aplication_version"] != version_json["web_app"]):
            print("NOT DEPLOYABLE")
            raise Exception('Not deployable')

        if(config_json["web_server_version"] != version_json["web_serv"]):
            print("NOT DEPLOYABLE")
            raise Exception('Not deployable')

        if(config_json["api_version"] != version_json["api"]):
            print("NOT DEPLOYABLE")
            raise Exception('Not deployable')

        # App is deployable. Start getting config data from Github.
        timestamp = 0
        # Check config and get timestamp files.
        if "timestamp" in config_json:
            timestamp = config_json["timestamp"]

        timestamp_string = str(timestamp)

        # Start by creating all URLS to use
        app_URI = gitUrl + "/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_app.json"
        collection_URI = gitUrl + "/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_collections.json"
        permission_URI = gitUrl + "/main/Apps/" + app +"/" + version + "/" + timestamp_string + "_permission.json"

        git_app_response = requests.get(app_URI)
        if git_app_response.status_code != 200:
            print("ERROR CODE NOT 200 FILE NOT FOUND")
            raise Exception('Not deployable')

        app_json = git_app_response.json()

        git_collection_response = requests.get(collection_URI)
        if git_collection_response.status_code != 200:
            print("ERROR CODE NOT 200 FILE NOT FOUND")
            raise Exception('Not deployable')

        collection_json = git_collection_response.json()

        git_permission_response = requests.get(permission_URI)
        if git_permission_response.status_code != 200:
            print("ERROR CODE NOT 200 FILE NOT FOUND")
            raise Exception('Not deployable')

        permission_json = git_permission_response.json()

        # Check validity of json downloads by dumping if something goes wring JSON is not correct.
        try:
            test = json.dumps(app_json, separators=(',', ':'))
        #     print(test)
        except:
            print("Not able to dump json. App data might be broken")
        try:
            test = json.dumps(collection_json, separators=(',', ':'))
        #     print(test)
        except:
            print("Not able to dump json. Collection data might be broken")
        try:
            test = json.dumps(permission_json, separators=(',', ':'))
        #     print(test)
        except:
            print("Not able to dump json. permission data might be broken")

        # Send files to API for recontruction.
        url = settings.baseURL + "api/transfer/app"
        response = requests.post(url, json={
            "app_json": json.dumps(app_json, separators=(',', ':')),
            "collection_json": json.dumps(collection_json, separators=(',', ':')),
            "permission_json": json.dumps(permission_json, separators=(',', ':'))
        },headers={
                'Authorization': 'Bearer ' + settings.token
        })

        # return response so pypi user can still let his code run.
        print(response.json())

        return response.json()

    def GenerateApp(self, gitAccessToken, app, version):
        if not Auth.tokenValid():
            Auth.refreshToken()

        # Get app and collection data
        appData = requests.get(settings.baseURL + 'api/app/' + app + '?extended=true', headers={'Authorization': 'Bearer ' + settings.token})
        collectionData = appData.json()["data"]
        collectionData = appData["collections"]
        collectionData = json.dumps(collectionData)
        appData = json.dumps(appData)

        # Get current version of api used
        versionData = requests.get(settings.baseURL + 'api/version/', headers={'Authorization': 'Bearer ' + settings.token})
        versionData = versionData.json()["data"]

        g = Github(gitAccessToken)
        repo = g.get_repo("bharkema/Clappform_models")
        branch = repo.get_branch(branch="main")
        branch.commit

        t = time.time()
        timestamp_int = int(t)
        timestamp = str(timestamp_int)
        commitMessage = "New App"
        configData = {
            "timestamp": timestamp_int,
            "created_by": __USERNAME__,
            "enviroment": settings.baseURL,
            "api_version": versionData["data"]["api"],
            "web_application_version": versionData["data"]["web_application"],
            "web_server_version": versionData["data"]["web_server"],
            "deployable": "true"
        }
        appFilePath = "Apps/" + app + "/" + version +"/ "+ timestamp + "_app.json"
        repo.create_file(appFilePath, commitMessage, appData, branch="main")

        collectionFilePath = "Apps/" + app + "/" + version +"/ "+ timestamp + "_collections.json"
        repo.create_file(collectionFilePath, commitMessage, collectionData, branch="main")

        permissionFilePath = "Apps/" + app + "/" + version +"/ "+ timestamp + "_permission.json"
        repo.create_file(permissionFilePath, commitMessage, "[{}]", branch="main")

        configFilePath = "Apps/" + app + "/" + version +"/_config.json"
        repo.create_file(configFilePath, commitMessage, json.dumps(configData), branch="main")

        return 200

