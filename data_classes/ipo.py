from datetime import date
from dataclasses import dataclass, asdict

from utils.formatter import Formatter

@dataclass
class SecurityCompany:
    company_name: str
    stock_amount: int

    def __init__(self, **kwargs):
        self.company_name = kwargs.get("인수인")
        self.stock_amount = kwargs.get("인수수량")

@dataclass
class Ipo:
    company_code: int
    company_name: str
    start_date: str
    payment_date: str
    security_company_set: list[SecurityCompany]

    def __init__(self, **kwargs):
        self.company_code = kwargs.get("company_code")
        self.company_name = kwargs.get("company_name")
        self.start_date = Formatter.change_date_string_format(kwargs.get("청약공고일"), "%Y년 %m %d")
        self.payment_date = Formatter.change_date_string_format(kwargs.get("납입기일"))
        self.security_company_set = [SecurityCompany(**security_company) for security_company in kwargs.get("security_company_data")]
    
    def asdict(self):
        return asdict(self)

if __name__ == "__main__":
    data = {'company_code': '00527011', 'company_name': '엘비루셈', '청약기일': '20210603', '납입기일': '20210607', '청약공고일': '20210602', 'security_company_data': [{'인수인': '한국투자증권', '인수수량': 4200000}, {'인수인': 'KB증권', '인수수량': 1800000}]}
    data = Ipo(**data)
    print(data.asdict())