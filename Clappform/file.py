from .settings import settings
from .auth import Auth
import os
import time
import pandas as pd

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
            elif file_type == "pickle":
                content.to_pickle(filepath,compression='gzip')
            else:
                with open(filepath, 'wb') as fd:
                    fd.write(bytes(content, 'utf-8'))
        else:
            return "File already exists"

        return "File Created"

    def Read(file_type = "", file_name = ""):
        # Use globals from worker, remove if worker allows these globals
        environment  = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "./data/azure/"

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        filepath = folderpath + "/" + file_name
        if file_type == "parquet":
            start = time.perf_counter()
            read_par_file = pd.read_parquet(filepath)
            end = time.perf_counter()
            loading_time = end - start
            print(read_par_file)
            print("Read parquet data", loading_time)
            return pd
        elif file_type == "pickle":
            start = time.perf_counter()
            read_par_file = pd.read_pickle(filepath)
            end = time.perf_counter()
            loading_time = end - start
            print(read_par_file)
            print("Read pickle data", loading_time)
            return pd
        else:
            f = open(filepath, "rb")
            return f.read()
