import io
import os
import json
import zipfile
import logging
from traceback import print_exc

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from financial_data_api.dart import Dart
from data_classes.ipo import Ipo

def lambda_handler(event, context):
    BASE_URL = os.environ["DJANGO_URL"]
    today = datetime.today()
    start_date = today - timedelta(days=61)
    today = today.strftime("%Y%m%d")
    start_date = start_date.strftime("%Y%m%d")

    is_ok, raw_disclosure_data= Dart.try_get_raw_disclosure_data(start_date=start_date, end_date=today)
    if is_ok:
        ipo_data = Dart.get_ipo_data_from_disclosure_data(raw_disclosure_data)
        print(ipo_data)
    else:
        return {
            'statusCode': 400,
            'body': "Dart api error"
        }

    # get ipo data from database
    ipo_list_url = os.path.join(BASE_URL, "ipo/")
    ipos = requests.get(ipo_list_url).json()
    company_codes = [ipo["company_code"] for ipo in ipos]
    
    new_data = []
    update_needed_data = []
    for company_code, data in ipo_data.items():
        company_name = data["corp_name"]
        receipt_num = int(data["rcept_no"])
        try:
            ipo_xml_data = Dart.get_ipo_xml_data(receipt_num)
            ipo_detail_data = Dart.get_ipo_detail_from_xml(ipo_xml_data)
            ipo = Ipo(
                company_code=company_code,
                company_name=company_name,
                receipt_num=receipt_num,
                **ipo_detail_data
            )
            print(ipo.asdict())
            if company_code in company_codes:
                update_needed_data.append(ipo.asdict())
            else:
                new_data.append(ipo.asdict())
        except Exception as e:
            logging.error(f"[xml parsing error] receipt_num: {receipt_num}, company_name: {company_name}\n")

    # update db
    headers = {
        "content-type":"application/json; charset=utf-8"
    }
    request_body = {
        "data": new_data
    }
    res = requests.post(ipo_list_url, headers=headers, data=json.dumps(request_body))
    new_data_locations = res.json()

    updated_data = []
    for data in update_needed_data:
        company_code = data["company_code"]
        request_body = {
            "data": data
        }
        ipo_put_url = os.path.join(ipo_list_url, f"{company_code}/")
        res = requests.put(ipo_put_url, headers=headers, data=json.dumps(request_body))
        if res.status_code == 200:
            updated_data.append(company_code)
        else:
            logging.error(f"[update db error] company code: {company_code}")
    
    res_body = {
        "new_data_locations": new_data_locations,
        "updated_data": updated_data
    }
        
    return {
        'statusCode': 200,
        'headers': {"content-type":"application/json; charset=utf-8"},
        'body': json.dumps(res_body)
    }

if __name__ == "__main__":
    result = lambda_handler("", "")
    print(result)