import unittest
from kite_utils import KiteUtil


class KiteUtilsTest(unittest.TestCase):

    def test_profit(self):
        self.assertEqual(KiteUtil.get_profit(100, 110, 1, KiteUtil.EXCHANGE_NSE, KiteUtil.TRADE_TYPE_INTRADAY), (9.944675, 0.055325))

if __name__ == '__main__':
    unittest.main()

