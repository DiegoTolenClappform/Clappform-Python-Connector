from .settings import settings
from .auth import Auth
from .app import App
import requests
import json
from github import Github
from datetime import date
import time
import base64

class Transfer:
    id = None

    def __init__(self, transfer = None):
        self.id = transfer

    def CreateApp(app, version, gitAccessToken = ""):
        if not Auth.tokenValid():
            Auth.refreshToken()

        g = Github(gitAccessToken)
        repo = g.get_repo("ClappFormOrg/framework_models")

        try:
            gitresponse = repo.get_contents("/app/" + app + "/" + version + "/_config.json")
            content = base64.b64decode(gitresponse.content)
        except:
            print("ERROR: Config file not found")
            return

        # Check if app is delpoyable
        config_json = json.loads(content)
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

        # Temporarily turned off
        # version_json = version_response.json()["data"]
        # if(config_json["web_application_version"] != version_json["web_application"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('Not deployable')

        # if(config_json["web_server_version"] != version_json["web_server"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('Not deployable')

        # if(config_json["api_version"] != version_json["api"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('Not deployable')

        # App is deployable. Start getting config data from Github.
        timestamp = 0
        # Check config and get timestamp files.
        if "timestamp" in config_json:
            timestamp = config_json["timestamp"]

        timestamp_string = str(timestamp)

        app_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_app.json"
        try:
            gitresponse = repo.get_contents(app_URI)
            temp = base64.b64decode(gitresponse.content)
            app_json = json.loads(temp)
        except:
            print("ERROR: App file not found")

        collection_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_collections.json"
        try:
            gitresponse = repo.get_contents(collection_URI)
            temp = base64.b64decode(gitresponse.content)
            collection_json = json.loads(temp)
        except:
            print("ERROR: Collection file not found")

        permission_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_permission.json"
        try:
            gitresponse = repo.get_contents(permission_URI)
            temp = base64.b64decode(gitresponse.content)
            permission_json = json.loads(temp)
        except:
            print("ERROR: Permission file not found")


        # Read app, if app exists delete it
        try:
            responseApp = App(app).ReadOne(extended=False)
            responseApp = App(app).Delete()
        except:
            pass

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

    def PublishApp(app = "", gitAccessToken = ""):
        if not Auth.tokenValid():
            Auth.refreshToken()

        # Get app and collection data
        responseApp = App(app).ReadOne(extended=True)
        collectionData = responseApp["collections"]

        g = Github(gitAccessToken)
        repo = g.get_repo("ClappFormOrg/framework_models")
        # Generate version for app,
        today = date.today()
        version = today.strftime("%y%m%d") # yymmdd

        # Check if app with version already exists, if it does, append number
        versionInUse = True
        additional = 1
        while versionInUse:
            try:
                gitresponse = repo.get_contents("/app/" + app + "/" + version + "/_config.json")
                if additional == 1:
                    version = version + "-" + str(additional)
                else:
                    version = version[:-1]
                    version = version + str(additional)
                additional+=1
            except:
                versionInUse = False
                pass
                break

        # Get current version of framework api, web_application and web_server
        responseVersion = requests.get(settings.baseURL + 'api/version/', headers={'Authorization': 'Bearer ' + settings.token})
        versionData = responseVersion.json()["data"]

        branch = repo.get_branch(branch="main")
        branch.commit

        t = time.time()
        timestamp_int = int(t)
        timestamp = str(timestamp_int)
        commitMessage = app + " - " + version + " published"

        configData = {
            "timestamp": timestamp_int,
            "created_by": settings.username,
            "enviroment": settings.baseURL,
            "api_version": versionData["api"],
            "web_application_version": versionData["web_application"],
            "web_server_version": versionData["web_server"],
            "deployable": "true"
        }
        appFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_app.json"
        repo.create_file(appFilePath, commitMessage, '[' + json.dumps(responseApp) + ']', branch="main")

        collectionFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_collections.json"
        repo.create_file(collectionFilePath, commitMessage, json.dumps(collectionData), branch="main")

        permissionFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_permission.json" # Restore requires permission file
        repo.create_file(permissionFilePath, commitMessage, "[{}]", branch="main")

        configFilePath = "app/" + app + "/" + version +"/_config.json"
        repo.create_file(configFilePath, commitMessage, json.dumps(configData), branch="main")

        return 200
