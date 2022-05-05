from .settings import settings
from .auth import Auth
import os

class File:
    id = None

    def __init__(self, file = None):
        self.id = file

    def Upload(content, file_type, file_name, overwrite=False):
        # Use globals from worker, remove if worker allows these globals
        environment  = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "./data/azure/"

        if not Auth.tokenValid():
            Auth.refreshToken()

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        os.makedirs(folderpath, exist_ok = True)

        filepath = folderpath + "/" + file_name

        if overwrite or not os.path.exists(filepath):
            if file_type == "parquet":
                content.to_parquet(filepath,compression='gzip')
            else:
                with open(filepath, 'wb') as fd:
                    fd.write(bytes(content, 'utf-8'))
                    print("File Created")
        else:
            print("File already exists")

        return "File Created"

    def Read(file_type = "", file_name = "") -> bytes:
        # Use globals from worker, remove if worker allows these globals
        environment  = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "./data/azure/"

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        filepath = folderpath + "/" + file_name

        f = open(filepath, "rb")
        return f.read()





