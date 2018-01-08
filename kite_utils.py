from datetime import date
from datetime import datetime
from time import tzname
from datetime import time


class KiteUtil(object):

    PRE_MARKET_OPEN_TIME = '09:00'
    PHYSICAL_MARKET_OPEN_TIME = '09:15'
    MARKET_CLOSE_TIME = '15:15'
    PHYSICAL_MARKET_CLOSE_TIME = '15:30'

    EXCHANGE_BSE = 'BSE'
    EXCHANGE_NSE = 'NSE'

    TRADE_TYPE_INTRADAY = 'INTRADAY'
    TRADE_TYPE_DELIVERY = 'DELIVERY'

    # All these values are subject to change
    BROKERAGE_INTRADAY = 0.01/100
    BROKERAGE_INTRADAY_FLAT = 20
    BROKERAGE_DELIVERY = 0
    STT_CTT_INTRADAY = 0.025/100
    STT_CTT_DELIVERY = 0.1/100
    TRANSACTION_CHARGES_BSE = 1.50
    TRANSACTION_CHARGES_NSE = 0.00325/100
    GST = 18/100
    SEBI_CHARGES = 15/10000000
    STAMP_CHARGES = None

    # Every year we need to update holiday list
    # http://www.bseindia.com/markets/marketinfo/listholi.aspx
    # https://www.nseindia.com/global/content/market_timings_holidays/market_timings_holidays.htm
    # https://zerodha.com/z-connect/traders-zone/holidays/trading-holidays-2018-nse-bse-mcx

    holiday_list = ['26-01-2018',  # 1	Republic Day
                    '13-02-2018',  # 2	Mahashivratri
                    '02-03-2018',  # 3	Holi
                    '29-03-2018',  # 4	Mahavir Jayanti
                    '30-03-2018',  # 5	Good Friday
                    '01-05-2018',  # 6	Maharashtra Day
                    '15-08-2018',  # 7	Independence Day
                    '22-08-2018',  # 8	Bakri Id
                    '13-09-2018',  # 9	Ganesh Chaturthi
                    '20-09-2018',  # 10	Muharram
                    '02-10-2018',  # 11	Mahatma Gandhi Jayanti
                    '18-10-2018',  # 12	Dussehra
                    '07-11-2018',  # 13	Diwali  Laxmi Pujan*
                    '08-11-2018',  # 14	Diwali Balipratipada
                    '23-11-2018',  # 15	Gurunanak Jayanti
                    '25-12-2018']  # 16	Christmas

    def get_profit(self, buy_price, sell_price, qty, exchange, trade_type):
        # price_diff = (sell_price - buy_price) * QTY
        total_buy_price = buy_price * qty
        total_sell_price = sell_price * qty

        if exchange == self.EXCHANGE_BSE:
            transaction_charges = 3
        elif exchange == self.EXCHANGE_NSE:
            buy_transaction = total_buy_price * self.TRANSACTION_CHARGES_NSE
            sell_transaction = total_sell_price * self.TRANSACTION_CHARGES_NSE
            transaction_charges = buy_transaction + sell_transaction

        if trade_type == self.TRADE_TYPE_INTRADAY:
            buy_brokerage = total_buy_price * self.BROKERAGE_INTRADAY
            sell_brokerage = total_sell_price * self.BROKERAGE_INTRADAY

            buy_brokerage = buy_brokerage if buy_brokerage < self.BROKERAGE_INTRADAY_FLAT else self.BROKERAGE_INTRADAY_FLAT
            sell_brokerage = sell_brokerage if sell_brokerage < self.BROKERAGE_INTRADAY_FLAT else self.BROKERAGE_INTRADAY_FLAT

            brokerage = buy_brokerage + sell_brokerage
            stt_ctt = sell_price * self.STT_CTT_INTRADAY
        elif trade_type == self.TRADE_TYPE_DELIVERY:
            stt_ctt = (sell_price * self.STT_CTT_DELIVERY) + (buy_price * self.STT_CTT_DELIVERY)
            brokerage = 0

        gst = (brokerage + transaction_charges) * self.GST
        sebi_buy_charges = buy_price * qty * self.SEBI_CHARGES
        sebi_sell_charges = sell_price * qty * self.SEBI_CHARGES
        sebi_charges = sebi_buy_charges + sebi_sell_charges

        total_charges = brokerage + transaction_charges + stt_ctt + gst + sebi_charges
        profit_loss = total_buy_price - total_sell_price
        final_profit_loss = profit_loss - total_charges

        return (final_profit_loss, total_charges)

    def is_tradingday(self):
        today = date.today()
        weekday_index = today.weekday()
        # Saturday and Sunday
        if weekday_index == 5 or weekday_index == 6:
            return False
        else:
            if today in [datetime.strptime(d, "%d/%m/%Y").date() for d in self.holiday_list]:
                return False
            else:
                return True

    def is_indian_timezone(self):
        if tzname[1] == 'IST':
            return True
        else:
            return False

    def is_pre_market_hour(self):
        now = datetime.now()

        pre_market_open_time = time(*map(int, self.PRE_MARKET_OPEN_TIME.split(':')))
        pre_market_close_time = time(*map(int, self.PHYSICAL_MARKET_OPEN_TIME.split(':')))

        if pre_market_open_time <= now.time() <= pre_market_close_time:
            return True
        else:
            return False

    def is_market_hour(self):
        now = datetime.now()

        physical_market_open_time = time(*map(int, self.PHYSICAL_MARKET_OPEN_TIME.split(':')))
        physical_market_close_time = time(*map(int, self.PHYSICAL_MARKET_CLOSE_TIME.split(':')))

        if physical_market_open_time <= now.time() <= physical_market_close_time:
            return True
        else:
            return False
