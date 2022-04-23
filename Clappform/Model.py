from .settings import settings
from .auth import Auth
import requests

class Model:
    id = None

    def _init_(self, model = None)
        self.id = model

    def Create_App(app, version)
        if not Auth.tokenValid():
            Auth.refreshToken()
        
        URI = "https://raw.githubusercontent.com/bharkema/clappform_models/main/Apps/" + app +"/" + version + "/__config.json"

        

        # Read files from Github Repo
        gitresponse = requests.get()


        # Send files to API for recontruction.



