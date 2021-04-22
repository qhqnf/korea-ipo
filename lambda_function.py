import io
import os
import json
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from financial_data_api.dart import Dart

def lambda_handler(event, context):
    today = datetime.today()
    start_date = today - timedelta(days=61)
    today = today.strftime("%Y%m%d")
    start_date = start_date.strftime("%Y%m%d")
    
    is_ok, raw_disclosure_data= Dart.try_get_raw_disclosure_data(start_date=start_date, end_date=today)
    if is_ok:
        ipo_data = Dart.get_ipo_data_from_disclosure_data(raw_disclosure_data)
    else:
        return {
            'statusCode': 400,
            'body': "Dart api error"
        }
    
    return {
        'statusCode': 200,
        'headers': {"content-type":"application/json; charset=utf-8"},
        'body': json.dumps(f'{ipo_data}')
    }
