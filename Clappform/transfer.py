from .settings import settings
from .auth import Auth
from .app import App
import requests
import json
from github import Github
from datetime import date
import time
import base64
from simplecrypt import encrypt, decrypt
import os
import pandas as pd

class Transfer:
    id = None

    def __init__(self, transfer = None):
        self.id = transfer

    def CreateApp(app, version, gitAccessToken = "", password=""):
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

        if config_json["deployable"] == False:
            print("NOT DEPLOYABLE RAISING ERROR")
            raise Exception('ERROR: Not deployable')

        version_url = settings.baseURL + "api/version"
        version_response = requests.get(version_url,headers={
                'Authorization': 'Bearer ' + settings.token
        })

        if version_response.status_code != 200:
            print(version_response)
            raise Exception('ERROR: Can\'t retrieve framework version')

        # # Temporarily turned off
        # version_json = version_response.json()["data"]
        # if(config_json["web_application_version"] != version_json["web_application"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('ERROR: Web_application version does not comply. Current: ' + version_json["web_application"] + ' , Source: ' + config_json["web_application_version"] + '.')

        # if(config_json["web_server_version"] != version_json["web_server"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('ERROR: Web_server version does not comply. Current: ' + version_json["web_server"] + ' , Source: ' + config_json["web_server"] + '.')

        # if(config_json["api_version"] != version_json["api"]):
        #     print("NOT DEPLOYABLE")
        #     raise Exception('ERROR: API version does not comply. Current: ' + version_json["api"] + ' , Source: ' + config_json["api"] + '.')

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

        form_template_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_form_template.json"
        try:
            gitresponse = repo.get_contents(form_template_URI)
            temp = base64.b64decode(gitresponse.content)
            formtemplate_json = json.loads(temp)
        except:
            print("ERROR: Form templates file not found")

        action_flow_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_action_flows.json"
        try:
            gitresponse = repo.get_contents(action_flow_URI)
            temp = base64.b64decode(gitresponse.content)
            actionflow_json = json.loads(temp)
        except:
            print("ERROR: Action Flow file not found")

        import_entry_URI = "/app/" + app +"/" + version + "/" + timestamp_string + "_import_entry.json"
        try:
            gitresponse = repo.get_contents(import_entry_URI)
            temp = base64.b64decode(gitresponse.content)
            import_json = json.loads(temp)
        except:
            print("ERROR: Import entry file not found")

        # Send files to API for recontruction.
        url = settings.baseURL + "api/transfer/app"
        response = requests.post(url, json={
            "apps": json.dumps(app_json, separators=(',', ':')),
            "collections": json.dumps(collection_json, separators=(',', ':')),
            "form_templates": json.dumps(formtemplate_json, separators=(',', ':')),
            "action_flows": json.dumps(actionflow_json, separators=(',', ':')),
            "import_entry": json.dumps(import_json, separators=(',', ':'))
        },headers={
            'Authorization': 'Bearer ' + settings.token
        })

        # Append Data sets to the collections
        if response.status_code == 200:
            if password != "":
                collection_data = json.dumps(collection_json)
                for collection in collection_data:
                    g = Github(gitAccessToken)
                    Datablob_uri = "/app/" + app +"/" + version + "/" + timestamp_string + "_" + collection["slug"] + ".csv"

                    gitresponse = repo.get_contents(Datablob_uri)
                    url_download = gitresponse.download_url
                    rep = requests.get(url_download)
                    decrypted_data = decrypt(password, rep.content).decode('utf8')

                    f = open(collection["slug"] + '.csv', "a")
                    f.write(decrypted_data)
                    f.close()

                    df = pd.read_csv(collection["slug"] + '.csv', header=0)
                    os.remove(collection["slug"] + '.csv')

                    App(app).Collection(collection["slug"]).DataFrame().Append(dataframe=df, n_jobs=1, show = False)

        # return response so pypi user can still let his code run.
        try:
            response = response.json()
            print(response)
        except:
            response = {}
            pass
        return response

    def PublishApp(app = "", gitAccessToken = "", password=""):
        if not Auth.tokenValid():
            Auth.refreshToken()

        # Get app and collection data
        try:
            responseApp = App(app).ReadOne(extended=True)
            collectionData = responseApp["collections"]
        except:
            return 404

        # Get form_template and action_flow data used by app
        form_templates = []
        action_flows = []
        for group in responseApp["groups"]:
            for page in group["pages"]:
                for row in page["rows"]:
                    for module in row["modules"]: # Check for form templates
                        if module["type"]["type"] == "Questionnaire":
                            form_id = module["selection"]["template"]["id"]
                            # Curl request to get data of all form templates
                            response = requests.get(settings.baseURL + 'api/form_template/' + str(form_id) + '?extended=true', headers={'Authorization': 'Bearer ' + settings.token})
                            form_templates.append(response.json()["data"])
                        elif module["type"]["type"] == "Data Table":
                            if "id" in module["selection"]["add"]["template"]:
                                form_id = module["selection"]["add"]["template"]["id"]
                                # Curl request to get data of all form templates
                                response = requests.get(settings.baseURL + 'api/form_template/' + str(form_id) + '?extended=true', headers={'Authorization': 'Bearer ' + settings.token})
                                form_templates.append(response.json()["data"])
                    for module in row["modules"]: # Check for form templates
                        action_buttons_present = "actionButtons" in module["selection"]
                        if(action_buttons_present):
                            for actions in module["selection"]["actionButtons"]:
                                for attribute, value in actions.items():
                                    if attribute =="actions":
                                        for keys in value:
                                            if keys["actionflow"]["id"] != None:
                                                action_flow_id = keys["actionflow"]["id"]
                                                response = requests.get(settings.baseURL + 'api/actionflow/' + str(action_flow_id) + '?extended=true', headers={'Authorization': 'Bearer ' + settings.token})
                                                action_flows.append(response.json()["data"])

        # Get import_entry data used by app
        import_entries = []
        try:
            response = requests.get(settings.baseURL + 'api/import?extended=true', headers={'Authorization': 'Bearer ' + settings.token})
            response = response.json()["data"]
            for ie in response:
                for coll in collectionData:
                    if ie["collection"] == coll["slug"]:
                        import_entries.append(ie)
        except:
            pass

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
        try:
            versionData = responseVersion.json()["data"]
        except:
            return

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
            "deployable": "true",
        }

        # Dumping data when password is entered
        if password != "":
            for collection in collectionData:
                data_empty = []
                dataframe_copy = pd.DataFrame(data_empty)
                for result in App(app).Collection(collection["slug"]).DataFrame().Read(original=True, n_jobs = 0):
                    dataframe_copy = pd.concat([dataframe_copy, result], axis=0)

                dataframe_copy.to_csv(collection["slug"] + '.csv')
                data = ""
                with open(collection["slug"] + '.csv', 'r') as file:
                    data = file.read()

                encrypted_data = encrypt(password, data)
                os.remove(collection["slug"] + '.csv')

                FilePath = "app/" + app + "/" + version +"/"+ timestamp + "_" + collection["slug"] + ".csv"
                repo.create_file(FilePath, commitMessage, encrypted_data, branch="main")

        # Create App file
        responseApp = '[' + json.dumps(responseApp) + ']'
        appFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_app.json"
        repo.create_file(appFilePath, commitMessage, responseApp, branch="main")

        # Create Collection file
        collectionData = json.dumps(collectionData)
        collectionFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_collections.json"
        repo.create_file(collectionFilePath, commitMessage, collectionData, branch="main")

        # Create Form Template file
        form_templates = json.dumps(form_templates)
        formtempateFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_form_template.json"
        repo.create_file(formtempateFilePath, commitMessage, form_templates, branch="main")

        # Create Action Flow file
        action_flows = json.dumps(action_flows)
        actionflowFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_action_flows.json"
        repo.create_file(actionflowFilePath, commitMessage, action_flows, branch="main")

        # Create Import entry file
        import_entries = json.dumps(import_entries)
        importentryFilePath = "app/" + app + "/" + version +"/"+ timestamp + "_import_entry.json"
        repo.create_file(importentryFilePath, commitMessage, import_entries, branch="main")

        # Create Config file
        configData = json.dumps(configData)
        configFilePath = "app/" + app + "/" + version +"/_config.json"
        repo.create_file(configFilePath, commitMessage, configData, branch="main")

        return 200

    def DeleteApp(app = "", version = "", gitAccessToken = "" ):
        g = Github(gitAccessToken)
        repo = g.get_repo("bharkema/Clappform_models")
        contents = repo.get_contents("app/" + app + "/" + version)
        for x in contents:
            repo.delete_file(x.path, "removed: " + x.path , x.sha, branch="main")

        return True