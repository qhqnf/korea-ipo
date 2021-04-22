import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Tuple
load_dotenv()

class Dart:
    API_KEY = os.environ.get("DART_API_KEY")

    @staticmethod
    def try_get_raw_disclosure_data(start_date: str, end_date: str) -> Tuple[bool, List]:
        BASE_URL = "https://opendart.fss.or.kr/api/list.json"
        params = {
            "crtfc_key": Dart.API_KEY,
            "bgn_de": start_date,
            "end_de": end_date,
            "pblntf_detail_ty": "C001",
            "page_count": 100
        }
        res = requests.get(BASE_URL, params=params)
        if res.status_code == 200:
            data = res.json()
            status = data["status"]
            message = data["message"]
            if status == '000':
                raw_disclosure_data = data["list"]
                return True, raw_disclosure_data
            elif status == "011":
                print(f"Invalid key: {message}")
                return False, []
            elif status == "020":
                print(f"Exceed request limit: {message}")
                return False, []
            elif status == "100":
                print(f"Invalid parameter field error: {message}")
                return False, []
            elif status == "800":
                print(f"API service is now in maintainance: {message}")
                return False, []
            else:
                print(f"Unknown Error: {message}")
                return False, []
        else:
            print("Request failure")
            return False, []

    def get_ipo_data_from_disclosure_data(raw_disclosure_data: List) -> Dict:
        ipo_data = {}
        
        for data in raw_disclosure_data:
            stock_code = data["stock_code"]
            corp_name = data["corp_name"]
            if not stock_code:
                del data["stock_code"]
                ipo_data[corp_name] = data
        
        return ipo_data