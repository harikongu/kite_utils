import unittest
from kite_utils import KiteUtil


class KiteUtilsTest(unittest.TestCase):

    def test_profit(self):
        self.assertEqual(KiteUtil.get_profit(100, 110, 1, KiteUtil.EXCHANGE_NSE, KiteUtil.TRADE_TYPE_INTRADAY), (9.944675, 0.055325))

    def test_market_hour(self):
        # Before 9:00 AM or After 3:30 PM
        self.assertEqual(KiteUtil.is_market_hour(), False)

    def test_timezone(self):
        # Confirm system timezone is IST
        self.assertEqual(KiteUtil.is_indian_timezone(), True)

if __name__ == '__main__':
    unittest.main()

