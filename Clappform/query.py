from .settings import settings
import pandas as pd
import requests
import math
import time
import json
from .auth import Auth


class Query:
    id = None

    def __init__(self, query=None):
        self.id = query

    def ReadData(self, body={}):
        self.data = []
        if not Auth.tokenValid():
            Auth.refreshToken()

        body = json.dumps(body, indent=2)

        response_total = requests.request(
            "POST",
            settings.baseURL + "api/dataframe/read_data?total_count=true",
            headers={"Authorization": "Bearer " + settings.token},
            data=body,
        )
        if response_total.json()["code"] == 200:
            for i in range(
                0, math.ceil(response_total.json()["data"][0]["total_results"] / 500)
            ):
                if not Auth.tokenValid():
                    Auth.refreshToken()
                response = ""

                res_data = []
                try:
                    response = requests.request(
                        "POST",
                        settings.baseURL + "api/dataframe/read_data",
                        headers={"Authorization": "Bearer " + settings.token},
                        data=body,
                    )
                    for item in response.json()["data"]:
                        res_data.append(item)

                    # Sleep for elapsed time to not get marked as DDOS
                    time.sleep(response.elapsed.total_seconds())
                    yield pd.DataFrame(res_data)
                except requests.exceptions.RequestException as exception:
                    resp = exception.response
                    print(resp.status_code)
