# 1 = green candle
# 0 = red candle

from collections import deque

from Algorithmic_Trading.Market_Simulator.level2data import Level2Data
from Algorithmic_Trading.Market_Simulator.order import Order
from Algorithmic_Trading.Market_Simulator.trader import Company
from trader import Trader
from exchange import Exchange
from candle import Candle
from indicators import IndicatorEngine
import data

import random


class Simulation:
    def __init__(self,starting_price = 100):
        self.starting_price = starting_price
        # self.candles = deque(maxlen=50) # will show last 50 candles
        self.candles = deque() # will show last 50 candles
        self.candles.append(Candle(self.starting_price,self.starting_price,self.starting_price,self.starting_price))

        self.indicators = IndicatorEngine() # stores different indicators
        # self.indicators.add_ema(9)
        # self.indicators.add_ema(15)
        # self.indicators.add_ema(21)
        # self.indicators.add_ema(50)
        for i in data.EMA_PERIODS:
            self.indicators.add_ema(i)

        self.indicators.update(self.candles[0])

        # self.time = 1
        self.open_price = self.close_price = self.high_price = self.low_price = self.starting_price
        self.volume = 0
        self.exchange = Exchange(self.starting_price)
        self.exchange.initialize_traders(self.indicators,self.exchange.level_2_data)

        # company = Trader(1000000,{100.5:200},0,data.TRADER_ID)
        # company = Trader(1000000,200,0,data.TRADER_ID)
        # company = Trader(100000000,200000,0,data.TRADER_ID)
        # self.company = Company(10000000000,10000,data.TRADER_ID)
        # t2 = Trader(10000,{},0,data.TRADER_ID)
        # self.exchange.traders.append(self.company)

        # self.exchange.traders.append(t2)

        # b = Order(data.ORDER_ID,data.TRADER_ID,100.5,1000,1,data.TIME)
        # data.TRADER_ID += 1
        # s = Order(0,1,102,10,1,1)
        # data.ORDER_ID += 1
        #
        # self.exchange.add_buy_order(b)
        # self.exchange.add_sell_order(b)
        # self.exchange.match_order()
        # print(self.exchange.get_price())

    # def execute_traders(self):
    #     for trader in self.exchange.traders:
    #         orders = trader.place_order(self.candles)
    #         for order in orders:
    #             if order:
    #                 data.TIME += 1
    #                 self.exchange.match_order(order)

    # def execute_traders(self):
    #     # self.exchange.level_2_data = Level2Data()
    #     for trader in self.exchange.traders:
    #         # order = trader.place_order(self.candles)
    #         stoploss_order = trader.place_stoploss_orders(self.exchange.price)
    #         orders = trader.place_order(self.candles)
    #
    #         if len(orders) != 0:
    #             for order in orders:
    #                 # if not order:
    #                 #     continue
    #                 if order.trade_type == 0:
    #                     # buy order
    #                     self.exchange.add_buy_order(order)
    #                 else:
    #                     # sell order
    #                     self.exchange.add_sell_order(order)

    def execute_traders(self):
        # d = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        for trader in self.exchange.traders:
            orders = trader.place_order(self.candles)
            for order in orders:
                if order:
                    self.exchange.match_order(order)
                    # d[self.exchange.traders[order.trader_id].trader_type] += order.quantity

        # print("#######")
        # for i in d:
        #     print(i, d[i])
        #
        # print()

        x = random.betavariate(5,5)  # in [0,1]

        data.MARKET_SENTIMENT = 2 * x -1
        # print(data.MARKET_SENTIMENT)

    def next_candle(self):
        self.execute_traders()
        # self.exchange.match_order()
        if data.TIME % data.TIME_FRAME == 0:
            # new candle formation
            self.open_price = self.exchange.get_price()
            self.close_price = self.open_price
            self.high_price = self.open_price
            self.low_price = self.open_price
            self.volume = 0
            self.candles.append(Candle(self.open_price,self.close_price,self.high_price,self.low_price,self.volume))
            self.indicators.update(self.candles[-1]) # will update indicators values
            # self.candles.append(Candle(self.open_price,self.high_price,self.low_price,self.close_price))
        else:
            # same candle
            self.high_price = max(self.high_price,self.exchange.get_price())
            self.low_price = min(self.low_price,self.exchange.get_price())
            self.close_price,self.volume = self.exchange.get_price_volume()

            self.candles[-1].Close = self.close_price
            self.candles[-1].High = self.high_price
            self.candles[-1].Low = self.low_price
            self.candles[-1].Volume = self.volume

        data.TIME += 1

