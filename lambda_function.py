import io
import os
import json
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def lambda_handler(event, context):
    today = datetime.today()
    start_date = today - timedelta(days=61)
    today = today.strftime("%Y%m%d")
    start_date = start_date.strftime("%Y%m%d")
    
    raw_disclosure_data= get_raw_disclosure_data(start_date=start_date, end_date=today)
    ipo_data = get_ipo_data_from_disclosure_data(raw_disclosure_data)
    
    return {
        'statusCode': 200,
        'headers': {"content-type":"application/json; charset=utf-8"},
        'body': json.dumps(f'{ipo_data}')
    }

def get_raw_disclosure_data(start_date, end_date):
    BASE_URL = "https://opendart.fss.or.kr/api/list.json"
    API_KEY = os.environ.get("DART_API_KEY")
    params = {
        "crtfc_key": API_KEY,
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
            return raw_disclosure_data
        elif status == "011":
            print(f"Invalid key: {message}")
            return []
        elif status == "020":
            print(f"Exceed request limit: {message}")
            return []
        elif status == "100":
            print(f"Invalid parameter field error: {message}")
            return []
        elif status == "800":
            print(f"API service is now in maintainance: {message}")
            return []
        else:
            print(f"Unknown Error: {message}")
            return []
    else:
        print("Request failure")
        return []
        
def get_ipo_data_from_disclosure_data(raw_disclosure_data):
    ipo_data = {}
    
    for data in raw_disclosure_data:
        stock_code = data["stock_code"]
        corp_name = data["corp_name"]
        if not stock_code:
            del data["stock_code"]
            ipo_data[corp_name] = data
    
    return ipo_data