import logging
from traceback import print_exc

import requests
import pandas as pd

class Krx:
    BASE_URL = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {"User-Agent": "Mozilla/5.0"}

    @staticmethod
    def get_ticker_data() -> pd.DataFrame:
        params = {
            "bld": "dbms/comm/finder/finder_stkisu",
            "mktsel": "ALL",
        }

        res = requests.post(Krx.BASE_URL, headers=Krx.headers, params=params)
        data = res.json()
        data = pd.DataFrame(data['block1']).iloc[:, 1:3]
        data = data.rename(columns={"short_code": "code", "codeName": "name"})
        
        return data
