from datetime import date
from dataclasses import dataclass, asdict

from utils.formatter import Formatter

@dataclass
class SecurityCompany:
    company_name: str
    stock_amount: int

    def __init__(self, **kwargs):
        self.company_name = kwargs["인수인"]
        self.stock_amount = kwargs["인수수량"]

@dataclass
class Ipo:
    company_code: str
    company_name: str
    start_date: str
    payment_date: str
    security_company_set: list
    max_price_band: int
    min_price_band: int
    price: int
    receipt_num: int

    def __init__(self, **kwargs):
        self.company_code = kwargs["company_code"]
        self.company_name = kwargs["company_name"]
        self.start_date = Formatter.change_date_string_format(kwargs["청약공고일"])
        self.payment_date = Formatter.change_date_string_format(kwargs["납입기일"])
        self.security_company_set = [SecurityCompany(**security_company) for security_company in kwargs["security_company_data"]]
        self.max_price_band = kwargs["max_price_band"]
        self.min_price_band = kwargs["min_price_band"]
        self.price = kwargs.get("price", 0)
        self.receipt_num = kwargs["receipt_num"]
    
    def asdict(self):
        return asdict(self)
