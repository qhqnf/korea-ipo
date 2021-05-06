import os
import io
import re
import zipfile
import logging
from datetime import datetime
from traceback import print_exc
from typing import List, Dict, Tuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

class Dart:
    API_KEY = os.environ.get("DART_API_KEY")

    @staticmethod
    def try_get_raw_disclosure_data(start_date: str=None, end_date: str=None) -> Tuple[bool, List]:
        BASE_URL = "https://opendart.fss.or.kr/api/list.json"
        if end_date is None:
            end_date = datetime.today().strftime("%Y%m%d")
        if start_date is None:
            start_date = end_date
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
                logging.error(f"Invalid key: {message}")
                return False, []
            elif status == "020":
                logging.error(f"Exceed request limit: {message}")
                return False, []
            elif status == "100":
                logging.error(f"Invalid parameter field error: {message}")
                return False, []
            elif status == "800":
                logging.error(f"API service is now in maintainance: {message}")
                return False, []
            else:
                logging.error(f"Unknown Error: {message}")
                return False, []
        else:
            logging.error("Request failure")
            return False, []

    @staticmethod
    def get_ipo_data_from_disclosure_data(raw_disclosure_data: List) -> Dict:
        ipo_data = {}
        
        for data in raw_disclosure_data:
            stock_code = data["stock_code"]
            corp_code = data["corp_code"]
            corp_name = data["corp_name"]

            if not stock_code and "인수목적" not in corp_name:
                ipo_data[corp_code] = data
                del data["stock_code"]
                del data["corp_code"]
        
        return ipo_data

    @staticmethod
    def get_ipo_xml_data(receipt_num:int) -> str:
        params = {
            "crtfc_key": Dart.API_KEY,
            "rcept_no": receipt_num
        }
        url = "https://opendart.fss.or.kr/api/document.xml"
        res = requests.get(url, params=params)
        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_file:
            xml_file = f"{receipt_num}.xml"
            with zip_file.open(xml_file) as f:
                ipo_xml_data = f.read()
        
        return ipo_xml_data

    @staticmethod
    def get_ipo_detail_from_xml(ipo_xml_data) -> Dict:
        soup = BeautifulSoup(ipo_xml_data, 'html.parser')
        detail_data_part = soup.find('body').find_all('part')[1].find("section-1").find_all("section-2")
        price_band_data_table = detail_data_part[2].find_all("table")[3]
        detail_data_part = detail_data_part[0].find_all("table")[1:]
        security_company_data_table = detail_data_part[1]
        schedule_data_table = detail_data_part[2]

        schedule_data = Dart.get_schedule_data_from_table(schedule_data_table)
        security_company_data = Dart.get_security_company_data_from_table(security_company_data_table)
        price_band_data = Dart.get_price_band_data_from_table(price_band_data_table)

        ipo_detail_data = {
            **schedule_data,
            "security_company_data": security_company_data,
            **price_band_data
        }
        
        return ipo_detail_data

    @staticmethod
    def get_schedule_data_from_table(schedule_data_table):
        headers = schedule_data_table.find('thead').find_all('th')
        rows = schedule_data_table.find('tbody').find_all('td')
        headers = [cell.text for cell in headers]
        rows = [cell.text for cell in rows]
        schedule_data = {}
        for header, row in zip(headers, rows):
            if header == "청약기일":
                row = row.split("~")[1].strip()
            schedule_data[header] = re.sub("[^0-9]", "", row)
        return schedule_data

    @staticmethod
    def get_security_company_data_from_table(security_company_data_table):
        security_company_data = []
        headers = security_company_data_table.find('thead').find_all('th')[0:3:2]
        headers = [cell.text for cell in headers]
        rows = security_company_data_table.find('tbody').find_all('tr')
        rows = [row.find_all('td')[1:4:2] for row in rows]
        for row in rows:
            temp = {}
            for header, cell in zip(headers, row):
                if header == "인수인":
                    temp[header] = cell.text
                elif header == "인수수량":
                    temp[header] = int(cell.text.replace(",", "").rstrip())
            security_company_data.append(temp)
        return security_company_data

    @staticmethod
    def get_price_band_data_from_table(price_band_data_table):
        rows = price_band_data_table.find("tbody").find("tr").find_all("td")
        price_band = rows[1].text.split('~')
        min_price_band = "".join(filter(lambda x: x.isnumeric(), price_band[0]))
        max_price_band = "".join(filter(lambda x: x.isnumeric(), price_band[1]))
        price_band_data = {
            "min_price_band": int(min_price_band),
            "max_price_band": int(max_price_band)
        }
        return price_band_data