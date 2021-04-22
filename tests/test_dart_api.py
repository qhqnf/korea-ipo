import unittest
from datetime import datetime, timedelta
from financial_data_api.dart import Dart

class DartApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f"{cls.__name__} starts")

    @classmethod
    def tearDownClass(cls):
        print(f"\n{cls.__name__} ends\n")
    
    def test_connection(self):
        today = datetime.today()
        start_date = today - timedelta(days=61)
        today = today.strftime("%Y%m%d")
        start_date = start_date.strftime("%Y%m%d")
        is_ok, _ = Dart.try_get_raw_disclosure_data(start_date=start_date, end_date=today)
        self.assertTrue(is_ok)


