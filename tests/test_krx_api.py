import unittest
from financial_data_api.krx import Krx

class KrxApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f"{cls.__name__} starts")

    @classmethod
    def tearDownClass(cls):
        print(f"\n{cls.__name__} ends")

    def test_connection(self):
        pass
    