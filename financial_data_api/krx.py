import requests
import datetime
import re
import io
import pandas as pd

class Krx:
    DOWNLOAD_URL = "http://file.krx.co.kr/download.jspx"

    @staticmethod
    def generate_otp():
        # params
        # requests
        # otp = res.text
        # return otp
        pass

    @staticmethod
    def get_stock_data(otp: str):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "http://marketdata.krx.co.kr/mdi",
        }
        params = {
            "code": otp
        }
        res = requests.post(Krx.DOWNLOAD_URL, headers=headers, params=params)
        res.encoding = "utf-8-sig"
        
        stock_data = pd.read_csv(io.BytesIO(data.content), header=0, thousands=",").iloc[:, 0:3]

        return stock_data