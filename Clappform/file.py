from .settings import settings
from .auth import Auth
import os
import time
import numpy as np
import pandas as pd
import requests
import base64
import pyarrow as pa
import pyarrow.parquet as pq
from pandas import json_normalize


class File:
    id = None

    def __init__(self, file=None):
        self.id = file

    def Upload(content, file_type, file_name, overwrite=False):
        # Use globals from worker, remove if worker allows these globals
        environment = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "/data/azure/"

        if not Auth.tokenValid():
            Auth.refreshToken()

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        os.makedirs(folderpath, exist_ok=True)

        filepath = folderpath + "/" + file_name

        if overwrite or not os.path.exists(filepath):
            if file_type == "parquet":
                content.to_parquet(filepath + ".gzip", compression="gzip")
            elif file_type == "pickle":
                content.to_pickle(filepath + ".gzip", compression="gzip")
            elif file_type == "csv":
                content.to_csv(filepath + ".gzip", compression="gzip")
            else:
                with open(filepath + "." + file_type, "wb") as fd:
                    fd.write(bytes(content, "utf-8"))
        else:
            return "File already exists"

        return "File Created"

    def Read(file_type="", file_name=""):
        # Use globals from worker, remove if worker allows these globals
        environment = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "/data/azure/"

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        filepath = folderpath + "/" + file_name

        if file_type == "parquet" or file_type == "pickle" or file_type == "csv":
            start = time.perf_counter()
            if file_type == "parquet":
                read_par_file = pd.read_parquet(filepath + ".gzip")
            elif file_type == "pickle":
                read_par_file = pd.read_pickle(filepath + ".gzip")
            elif file_type == "csv":
                read_par_file = pd.read_csv(filepath + ".gzip")
            end = time.perf_counter()
            loading_time = end - start
            print("Read " + file_type + " data in: ", loading_time)
            return read_par_file
        else:
            f = open(filepath + "." + file_type, "rb")
            return f.read()

    def AppendParquet(content, file_type, file_name, writer):
        # Use globals from worker, remove if worker allows these globals
        environment = "local"
        WORKER_PERSISTENT_STORAGE_PATH = "/data/azure/"

        if not Auth.tokenValid():
            Auth.refreshToken()

        folderpath = WORKER_PERSISTENT_STORAGE_PATH + environment + "/" + file_type
        filepath = folderpath + "/" + file_name + ".gzip"
        os.makedirs(folderpath, exist_ok=True)
        table = pa.Table.from_pandas(content)
        if writer is None:
            writer = pq.ParquetWriter(filepath, table.schema)
        writer.write_table(table=table)

        return writer

    def UploadDataFrameToAzure(
        srcdata,
        filename,
        exportType="excel",
        AzureFileShare="AZURE",
        AzureFolderPath=["file_upload", "clapp_pypi"],
    ):
        ## Check token validity ##
        if not Auth.tokenValid():
            Auth.refreshToken()
        """
        Options for exportType: json, excel & csv.
        Options for AzureFileShare: AZURE, PDF_AZURE, SFTP_AZURE & GENERAL_PDF.
        [{
            "srcdata": "pandas dataframe",
            "filename": "Export_file",
            "AzureFileShare": "SFTP_AZURE",
            "AzureFolderPath": ["upload"],
            "exportType": "excel, json or csv",
        }]
        """

        ## Convert dataframe data ##
        print("Converting DataFrame to ", exportType)
        if exportType == "excel":
            filename = filename + ".xlsx"

            # To Excel to base 64
            srcdata.to_excel(filename)
            with open(filename, "rb") as excel_file:
                base_64_data = base64.b64encode(excel_file.read())

        elif exportType == "csv":
            filename = filename + ".csv"

            # To CSV to base 64
            srcdata.to_csv(filename)
            with open(filename, "rb") as csv_file:
                base_64_data = base64.b64encode(csv_file.read())

        elif exportType == "json":
            filename = filename + ".json"

            # To JSON to base 64
            json_df = srcdata.to_json(orient="records")
            base_64_data = base64.b64encode(bytes(json_df, "utf-8"))

        json_request = {
            "location": AzureFileShare,
            "folder_path": AzureFolderPath,
            "file_name": filename,
        }
        json_request["content"] = base_64_data.decode("utf-8")

        ## Upload using API File routing ##
        response = requests.post(
            settings.baseURL + "api/file",
            json=json_request,
            headers={"Authorization": "Bearer " + settings.token},
        )

        final_file_name = response.json()["data"]["file_name"]
        return final_file_name
