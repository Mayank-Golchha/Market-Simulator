# # TODO : stoploss and take profit are both linked ie if one gets executed other gets canceled
#
#
# # 0 : random trader, 1 : level_1_trader, 2 : level_2_trader
# import bisect
# # level_1_trader
# # buy and sell seeing candle
# # eg : if last n candles are green they buy
#
#
# # you must explicitly call stop_loss order for each trader
#
#
# from collections import deque
# import random
#
# from pygame.examples.music_drop_fade import volume
#
# from order import Order
# from candle import Candle
# from indicators import IndicatorEngine
# from strategies import Strategies
# from level2data import Level2Data
# from stoploss_handler import StopLoss,TakeProfit
# from positions import Position
# import data
#
#
# class Trader:
#     def __init__(self,balance : float,holdings : int,trader_type : int,trader_id : int):
#         # balance is the amount of money the trader is having
#         # holdings represents total no of shares that the trader has been holding
#         # trader type denotes which kind of trader eg: random,Institute etc
#         # trader id : as there can be many traders of same type
#         # balance will be deducted the moment you place a order
#         # stock will be added in the holdings only when order gets filled
#         self.trader_type = trader_type
#         self.trader_id = trader_id
#         self.starting_balance = balance # the actual balance the trader starts with
#         self.balance = balance
#         self.holdings = holdings
#         self.total_trades = 0
#         self.new_starting_balance = self.starting_balance # will change starting balance after all holding are sold
#         self.all_orders = deque() # contains all active orders.
#         self.p_l = 0
#         # self.buy_orders = {} # only contains active buy orders with id as key. and when order is sold it would be removed
#         # self.stop_loss_orders = [] # contains [stop_loss,quantity] ,stores in increasing stoploss
#         self.stop_loss_orders = StopLoss() # contains all stoploss orders
#         self.take_profit_orders = TakeProfit() # contains all stoploss orders
#         # self.take_profit_orders = {} # contains price as key and [stop_loss,quantity]
#
#     def place_order(self,price_data) -> list:
#         # price_data contains all candles
#         # price_data = list[Candle]
#         return []
#
#     def place_stoploss_orders(self,current_price) -> list:
#         # if you bought 100 shares and put a stoploss on it
#         # and sold even one share then stoploss order will be canceled
#
#         # if you bought 50 shares today with stoploss on day 1 and 50 shares next day with no stoploss on day 2
#         # and next to next day you sold 50 shares ,the day 1 shares will be sold first and
#         # stoploss order will be still active
#         if len(self.stop_loss_orders.stoploss_orders) == 0:
#             return []
#
#         orders = []
#         top_order = self.stop_loss_orders.stoploss_orders[-1]
#         # while top_order[0] < current_price:
#
#         # ie price went below stoploss
#         while current_price <= top_order[0]:
#             order = self.place_sell_order(top_order[0],top_order[1])
#             if order:
#                 orders.append(order)
#             self.stop_loss_orders.pop()
#             if len(self.stop_loss_orders.stoploss_orders) == 0:
#                 break
#             top_order = self.stop_loss_orders.stoploss_orders[-1]
#
#         return orders
#
#     def place_take_profit_order(self,current_price) -> list:
#         # places take_profit orders
#         # if you bought 100 shares and put a take profit on it
#         # and sold even one share then takeprofit order will be canceled
#
#         # if you bought 50 shares today with takeprofit on day 1 and 50 shares next day with no takeprofit on day 2
#         # and next to next day you sold 50 shares ,the day 1 shares will be sold first and
#         # takeprofit order will be still active
#         if len(self.take_profit_orders.take_profit_orders) == 0:
#             return []
#
#         orders = []
#         top_order = self.take_profit_orders.take_profit_orders[0]
#         # while top_order[0] < current_price:
#         # ie price went above take_profit
#         while current_price >= top_order[0]:
#             order = self.place_sell_order(top_order[0], top_order[1])
#             if order:
#                 orders.append(order)
#             self.take_profit_orders.pop()
#             if len(self.take_profit_orders.take_profit_orders) == 0:
#                 break
#             top_order = self.take_profit_orders.take_profit_orders[0]
#
#         return orders
#
#     def is_stoploss_hit(self,current_price) -> bool:
#         # returns true if stop_loss hit
#         return self.stop_loss_orders.stoploss_orders and current_price <= self.stop_loss_orders.stoploss_orders[-1][0]
#
#     def is_takeprofit_hit(self,current_price) -> bool:
#         # returns true if take_profit hit
#         return self.take_profit_orders.take_profit_orders and current_price >= self.take_profit_orders.take_profit_orders[0][0]
#
#     # def place_multiple_orders(self,price_data) -> list:
#         # places multiple orders
#         # return []
#
#     # def place_stoploss_orders(self,current_price) -> list:
#         # sell when price go below stoploss
#         # stop_loss orders contains
#         # order = self.stop_loss_orders[0]
#         # s_o = []
#         # while order[-1] < current_price:
#         #     s_o.append(self.place_sell_order())
#         # return s_o
#
#     def place_buy_order(self,price,quantity):
#         # stop_loss is exact price below which sell order will be placed
#         if quantity <= 0 or price <= 0:
#             return None
#             # return
#         buy_order = Order(data.ORDER_ID, self.trader_id, price, quantity, 0, data.TIME)
#         if self.balance < price * quantity:
#             return None
#         self.balance -= price * quantity
#         data.ORDER_ID += 1
#
#         # if stop_loss > 0:
#         #     self.stop_loss_orders.append(stop_loss,quantity)
#
#         return buy_order
#
#     def sell_order_util(self,price,quantity):
#         # will remove active orders from queue
#         if len(self.all_orders) == 0:
#             return
#         top_order = self.all_orders[0]
#         while quantity >= top_order.quantity:
#             quantity -= top_order.quantity
#             top_order.quantity = 0
#             self.all_orders.pop()
#             if quantity == 0 or len(self.all_orders) == 0:
#                 return
#             top_order = self.all_orders[0]
#
#         top_order.quantity -= quantity
#
#     def place_sell_order(self,price,quantity):
#         # while selling if after selling total stoploss order > total holding
#         # then remove the stoploss order which is recently added
#         # if quantity <= 0 :
#         if quantity <= 0 or self.holdings <= 0:
#             self.holdings = 0
#             return None
#         sell_order = Order(data.ORDER_ID, self.trader_id, price, quantity, 1, data.TIME)
#         self.holdings -= quantity
#
#         self.stop_loss_orders.pop_recent(self.holdings) # if stoploss orders > holding pop recently added stoploss order
#
#         data.ORDER_ID += 1
#         self.sell_order_util(price,quantity)
#         if self.holdings == 0:
#             # all holdings are sold now new balance
#             # used for profit and loss finding
#             self.new_starting_balance = self.balance
#
#         # self.all_orders[sell_order.order_id] = sell_order
#         return sell_order
#
#     def place_short_order(self,price,quantity):
#         # shorting stock means taking share from someone and promising him to return the share within some days with interest
#         # you sell the share immadiately and if price decrease you get profit
#         amount = price * quantity
#         self.holdings -= quantity
#
#     def add_holding(self,price,quantity,order = None):
#         # order has been matched
#         # for buying
#         # used by exchange
#         self.holdings += quantity
#         # self.all_orders.append(order) # appending active order in queue
#         self.all_orders.append(Position(price,quantity)) # appending active order in queue
#
#     def add_balance(self,price,quantity,order = None) -> bool:
#         # order has been matched
#         # for selling
#         # used by exchange
#         self.balance += quantity * price
#         return False
#
#     def momentum(self, price_data: list, n: int, threshold: float = 0.01) -> int:
#         # helper function
#         # tells whether there is a momentum in price
#         # n = no of candles to look for
#         # if there is a change in price of more than threshold and if more no of green candles
#         # threshold = percent/100
#         # 1 : buy,-1 = sell,0 = hold
#         if not len(price_data) >= n+1:
#             return 0
#         min_price = price_data[-1].Close
#         max_price = price_data[-1].Close
#         green = red = 0
#
#         for i in range(n):
#             min_price = min(min_price, price_data[-(i + 1)].Low)
#             max_price = max(max_price, price_data[-(i + 1)].High)
#             if price_data[-(n+1)].isGreen():
#                 green += 1
#             else:
#                 red += 1
#
#         p = (max_price - min_price) / min_price
#         if p > threshold and abs(price_data[-2].Close - price_data[-2].Open)/price_data[-2].Open > threshold:
#             if green > red:
#                 return 1
#             return -1
#
#         return 0
#
#     def cancel_order(self,order : Order):
#         # will be called by exchange
#         # TODO : canceled order must be put in the active orders again
#         order.status = 2
#         if order.trade_type == 0:
#             # buy order cancel
#             self.balance += order.quantity * order.price
#         else:
#             # sell order cancel
#             self.holdings += order.quantity
#         # self.all_orders.remove(order)
#         del order
#
#     def print_summary(self):
#         print()
#         print("==== Trader Summary ====")
#         print("Trader Id : ", self.trader_id , " Trader Type : ", self.trader_type)
#         print("Total Trades made : ", self.total_trades)
#         print("Starting Balance : ", self.starting_balance , " Final Balance : " , self.balance)
#
#
# class Company(Trader):
#     # they are needed to supply with liquidity in market
#     # TODO : complete company code
#     def __init__(self,balance,quantity,trader_id):
#         super().__init__(balance,quantity,10,trader_id)
#
#     def place_order(self,price_data) -> list:
#         return []
#
#         # if order_:
#         #     return order_
#         # if self.holdings == 0:
#         #     return []
#         # quantity = int(self.holdings % 0.01)
#         # quantity = 1000
#         # percentage = random.uniform(-0.01,0.05)
#         # price = random.uniform(100,105)
#         # price = price_data[-1].Close * (1 + percentage)
#         # return [self.place_sell_order(price_data[-1].Close * (1 + percentage),quantity)]
#         # order = self.place_sell_order(price,quantity)
#         # if order:
#             # return [order]
#         # return []
#
#
# class RandomTrader(Trader):
#     def __init__(self,trader_id : int,balance : float = 0):
#         if balance == 0:
#             balance = random.uniform(data.RANDOM_MIN_BALANCE,data.RANDOM_MAX_BALANCE)
#
#         # ini = random.randint(0,2)
#         # if random.random() > 0.3:
#         #     ini = 0
#         super().__init__(balance,0,0,trader_id)
#
#         # buy_probability/sell_probability = probability threshold below which the trader will buy/sell.
#         # sell_probability will increase if the trader has holding
#         # self.buy_probability = 0.001
#         self.buy_probability = 0.0005
#         # self.sell_probability = 0.001
#         self.sell_probability = 0.0005
#         # if self.holdings == 0:
#         #     self.sell_probability = 0.02
#
#     def random_price(self,price,buyer,min_price):
#         # percentage = random.uniform(-0.01, 0.01)  # -1% to +1%
#         # return price * (1 + percentage)
#         percentage = 0
#         if buyer:
#             # buyer wants to buy in cheap
#             percentage = random.uniform(-0.05, 0.01)  # -5% to +1%
#             # percentage = random.uniform(-0.07, 0.01)  # -5% to +1%
#             # return random.uniform(min_price * (1-0.001),price * (1 + 0.001))
#             return price * (1 + percentage)
#         else:
#             # seller want to buy at more price
#             # percentage = random.uniform(-0.05, 0.02)  # -1% to +5%
#             percentage = random.uniform(-0.001, 0.005)  # -1% to +5%
#             # return random.uniform(min_price * (0.999),price * (1 + 0.001))
#             return price * (1 + percentage)
#
#         # return 0
#         # return price * (1 + percentage)
#
#     def get_random_selling_quantity(self):
#         # m = self.holdings[min(self.holdings.keys())]
#         return random.randint(1,max(1,int(self.holdings//2)))
#
#     # def place_order(self,price_data) -> Order:
#     def place_order(self, price_data) -> list:
#         p = random.random()
#         buy_sell = random.randint(0,1) # if 0 buy else sell
#         # current_price = price_data[-1].Close
#         # nth_candle = min(1, len(price_data) - 1) # random trader can choose between open of nth candle and current price + 1%
#         # nth_candle_price = price_data[nth_candle].Open
#         current_price = price_data[-1].Close
#         # current_price = price_data[-1].High
#
#         # if self.is_takeprofit_hit(current_price):
#         #     return self.place_take_profit_order(current_price)
#
#         # if self.is_stoploss_hit(current_price):
#         #     return self.place_stoploss_orders(current_price)
#
#         if buy_sell == 0 and self.balance >= current_price:
#             # buy
#             if p < self.buy_probability:
#                 # make_price = self.random_price(current_price,1,nth_candle_price)
#                 make_price = self.random_price(current_price,1,current_price)
#                 max_quantity = max(1,int(self.balance // current_price * 0.1)) # any random trader don't put all his income in trading
#                 # quantity = random.randint(1,int(self.balance // current_price * 0.3)) # any random trader don't put all his income in trading
#                 quantity = random.randint(1,max_quantity) # any random trader don't put all his income in trading
#
#                 buy_order = self.place_buy_order(make_price,quantity)
#                 # if random.random() < 0.2:
#                 #     stoploss_percent = random.uniform(0.5, 0.95)
#                 #     self.stop_loss_orders.append(current_price * stoploss_percent,quantity)
#                 if buy_order:
#                     percent = random.uniform(1.01,1.99)
#                     self.take_profit_orders.append(make_price * percent,max_quantity)
#                     return [buy_order]
#                 return []
#
#         # elif buy_sell == 1 and len(self.holdings):
#         elif buy_sell == 1 and self.holdings > 0:
#             # sell
#             if p < self.sell_probability:
#                 # make_price = self.random_price(current_price,0,nth_candle_price)
#                 make_price = self.random_price(current_price,0,current_price)
#                 quantity = self.get_random_selling_quantity()
#                 # if quantity * current_price + self.balance < self.starting_balance * (1-0.1):
#                 #     return None
#                 sell_order = self.place_sell_order(make_price,quantity)
#
#                 # if len(self.holdings) == 0:
#                 # if self.holdings == 0:
#                 #     self.sell_probability = 0
#                 # else:
#                 #     self.sell_probability -= 0.005 * quantity
#                 if sell_order:
#                     return [sell_order]
#                 return []
#
#         return []
#
#
# class Level1Trader(Trader):
#     # Level1 Trader
#     # will buy and sell by seeing last n candles
#     # eg : if last 3 candles are green buy
#     # if price goes below 20% of what they bought at sell
#     def __init__(self,trader_id : int,balance : float = 0):
#         if balance == 0:
#             balance = random.randint(data.LEVEL1_TRADER_MIN_BALANCE,data.LEVEL1_TRADER_MAX_BALANCE)
#         super().__init__(balance,0,1,trader_id)
#
#         self.n = random.randint(1,data.MAX_LAST_CANDLE_VIEW)
#
#     def buy_condition(self,price_data) -> bool:
#         # buy when last n candles are green
#         n = self.n
#         if random.random() >= 0.01:
#             return False
#         for i in range(len(price_data)-1,-1,-1):
#             if n == 0:
#                 return True
#             if not price_data[i].isGreen():
#                 return False
#             n -= 1
#         return False
#
#     def sell_condition(self,price_data) -> bool:
#         # buy when last n candles are green
#         n = self.n
#         if random.random() >= 0.005:
#             # else all traders will place orders at same time
#             return False
#
#         if len(price_data) >= 2:
#             diff = (price_data[-2].Close - price_data[-2].Open) / price_data[-2].Open
#             if diff >= 0.01:
#                 return True
#
#         balance = self.balance + price_data[-1].Close * self.holdings
#         # if balance < self.new_starting_balance * (1-data.LEVEL1_TRADER_LOSS):
#             # loss is more than 20%
#             # return True
#         for i in range(len(price_data)-1,-1,-1):
#             if n == 0:
#                 return True
#             # if price_data[i].isGreen():
#             if not price_data[i].isGreen():
#                     return False
#             n -= 1
#         return False
#
#     # def place_order(self,price_data) -> Order:
#     def place_order(self, price_data) -> list:
#         price = price_data[-1].Close
#         if self.is_takeprofit_hit(price):
#             return self.place_take_profit_order(price)
#         if self.holdings != 0:
#             # sell
#             if self.sell_condition(price_data):
#                 price = random.uniform(price * 0.98,price * 1.02)
#                 order = self.place_sell_order(price,self.holdings)
#                 if order:
#                     percent = random.uniform(1.001,1.999)
#                     # self.place_take_profit_order(price * 1.02)
#                     self.place_take_profit_order(price * percent)
#                     return [order]
#                 return []
#         else:
#             # buy
#             if self.buy_condition(price_data):
#                 # percentage = [0.10, 0.20, 0.30, 0.40] # percentage. will help to determine how much % of balance to use
#                 percentage = random.randint(10,40)
#                 # money = self.balance * random.choice(percentage)
#                 money = self.balance * percentage / 100
#                 quantity = int(money//price)
#                 order = self.place_buy_order(price,quantity)
#                 if order:
#                     return [order]
#                 return []
#         return []
#
#
# class Level2Trader(Trader):
#     # Level2 trader are better than level1 trader
#     # they use different indicators to buy and sell with stoploss
#     def __init__(self,indicators : IndicatorEngine,trader_id : int,balance : float = 0):
#         if balance == 0:
#             balance = random.randint(data.LEVEL2_TRADER_MIN_BALANCE,data.LEVEL2_TRADER_MAX_BALANCE)
#         # indicators = a class which contains all indicators
#         super().__init__(balance,0,2,trader_id)
#
#         self.thresholds = [random.random() for _ in range(5)] # contains different thresholds for different strategies
#         self.indicators = indicators
#         self.strategies = Strategies()
#         self.three_emas = [data.EMA_PERIODS[-1],random.choice([data.EMA_PERIODS[1],data.EMA_PERIODS[2]]),data.EMA_PERIODS[0]] #  long term,slow,fast
#         self.single_ema = random.choice(data.EMA_PERIODS) # single ema
#         self.bought_price = 0 # last bought price
#         self.start = 0
#
#     def strategy(self,price_data) -> int:
#         current_price = price_data[-1].Close
#         # 1 buy,-1 sell,0 hold
#         # if self.bought_price and current_price < self.bought_price * (1-data.LEVEL2_TRADER_STOPLOSS):
#         #     return -1
#
#         positions = []
#
#         if self.thresholds[0] < 0.2:
#             # single ema
#             output = self.strategies.single_ema(self.indicators.ema_values[self.single_ema],current_price)
#             positions.append(output)
#
#         elif self.thresholds[0] < 0.4:
#             # double ema crossover
#             positions.append(self.strategies.ema_crossover(self.three_emas[1],self.three_emas[2],current_price))
#
#         elif self.thresholds[0] < 0.6:
#             # triple ema strategy
#             trend_ema = self.indicators.ema_values[self.three_emas[0]]
#             slow_ema = self.indicators.ema_values[self.three_emas[1]]
#             fast_ema = self.indicators.ema_values[self.three_emas[2]]
#             positions.append(self.strategies.triple_ema_crossover(trend_ema, slow_ema, fast_ema, current_price))
#
#         if self.thresholds[1] > 0.5:
#             # rsi strategy
#             positions.append(self.strategies.rsi_strategy(self.indicators.rsi_value))
#
#         if self.thresholds[2] > 0.5:
#             # bollinger band strategy
#             positions.append(self.strategies.bollinger_strategy(current_price,self.indicators.bb_upper,self.indicators.bb_lower))
#
#         if self.thresholds[3] > 0.5:
#             # macd strategy
#             macd_val, signal_val, hist_val = self.indicators.macd_data()
#             positions.append(self.strategies.macd_strategy(macd_val, signal_val, hist_val, current_price))
#
#         if self.thresholds[4] > 0.5:
#             # vwap strategy
#             positions.append(self.strategies.vwap_strategy(current_price,self.indicators.vwap_value()))
#
#         # buy = 5
#         # sell = 5
#         # buy/sell only if all indicators say
#         # for i in positions:
#         #     if i == buy:
#         #         buy -= 1
#         #     elif i == sell:
#         #         sell -= 1
#         #     return 0
#         # if buy == 0:
#         #     return 1
#         # return -1
#         buy = sell = len(positions)
#
#         for i in positions:
#             if i == 1:
#                 buy -= 1
#             elif i == -1:
#                 sell -= 1
#         if buy == 0:
#             return 1
#         elif sell == 0:
#             return -1
#         return 0
#
#     def strategy1(self,price_data) -> int:
#         current_price = price_data[-1].Close
#         output = self.strategies.single_ema(self.indicators.ema_values[self.single_ema], current_price)
#         return output
#
#     # def place_order(self,price_data) -> Order:
#     def place_order(self, price_data) -> list:
#         if self.is_takeprofit_hit(price_data[-1].Close):
#             return self.place_take_profit_order(price_data[-1].Close)
#         # if self.start == 0:
#             # else all traders will trade at the same time
#             # p = random.random()
#             # if p < 0.01:
#             #     self.start = 1
#             # else:
#             #     return []
#         if random.random() >= 0.01:
#             return []
#         outcome = self.strategy(price_data)
#         current_price = price_data[-1].Close
#         if outcome == 1:
#             # buy
#             percentage = random.uniform(-0.01, 0.002)
#             # price = current_price * (1 + percentage)
#             price = current_price
#             budget = self.balance * random.randint(5,40) / 100
#             order_size = int(budget // price)
#             buy_order = self.place_buy_order(price,order_size)
#             self.take_profit_orders.append(price * 1.05,order_size)
#             if buy_order:
#                 return [buy_order]
#             return []
#         elif outcome == -1 and self.holdings > 0:
#             # sell
#             percentage = random.uniform(-0.002, 0.01)
#             price = current_price * (1 + percentage)
#             # return [self.place_sell_order(price,self.holdings)]
#             sell_order = self.place_sell_order(price,self.holdings)
#             if sell_order:
#                 return [sell_order]
#         return []
#
#
# class MarketMaker(Trader):
#     # they are called market makers because they provide liquidity
#     # they earn from spread if share at 100 to buy at 100 at same time sell at 100.01
#     # they should have good amount of initial shares
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:
#             balance = 30000000
#
#         super().__init__(balance,0,3,trader_id)
#
#         self.level2_data = level2_data
#
#         self.ticks_held = 0 # for how much time latest order has been held
#
#         # self.holdings = random.randint(1000,50000)
#
#         # self.cooldown_tick  = random.randint(1,1000) # the min ticks after which next action is allowed
#         self.cooldown_tick  = 10 # the min ticks after which next action is allowed
#         # self.delta = random.uniform(0.001,1) # by this difference they earn
#         # self.delta = 0.001 # by this difference they earn
#         self.delta = 0.0005 # by this difference they earn
#
#     def place_order(self,price_data) -> list:
#         self.ticks_held += 1
#
#         if self.ticks_held < self.cooldown_tick:
#             return []
#
#         if len(self.level2_data.buy_data) == 0 or len(self.level2_data.sell_data) == 0:
#             return []
#
#         best_bid = self.level2_data.buy_prices[0]
#
#         best_ask = self.level2_data.sell_prices[-1]
#
#         buy_volume = int(self.level2_data.buy_data[best_bid] * 0.2) # 20%
#         sell_volume = int(self.level2_data.sell_data[best_ask] * 0.2) # 20%
#
#         buy_price = random.uniform(best_bid,best_bid * 1.005)
#         sell_price = random.uniform(best_ask,best_ask * 1.01)
#
#         buy_volume = min(buy_volume,int(self.balance/buy_price))
#         sell_volume = min(sell_volume,self.holdings)
#
#         buy_order = self.place_buy_order(buy_price,buy_volume)
#         sell_order = self.place_sell_order(sell_price,sell_volume)
#
#         return [buy_order,sell_order]
#
#         # if best_ask - best_bid > 2 * self.delta:
#             # there can be profit
#             # buy_price = best_bid + self.delta
#             # sell_price = best_ask - self.delta
#             #
#             # buy_volume = int(self.level2_data.buy_data[best_bid] * 0.1) # 20%
#             # sell_volume = int(self.level2_data.sell_data[best_ask] * 0.1) # 20%
#             #
#             # buy_volume = min(buy_volume,int(self.balance/buy_price))
#             # sell_volume = min(sell_volume,self.holdings)
#             #
#             # buy_order = self.place_buy_order(buy_price,buy_volume)
#             # sell_order = self.place_sell_order(sell_price,sell_volume)
#             #
#             # self.ticks_held = 0
#             #
#             # return [buy_order,sell_order]
#
#         return []
#
#
# class AgressiveTraders(Trader):
#     # they are agressive buyers and seller. ie they sell at lowest ask, and buy at best bid
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:
#             # balance = random.randint(100000,10000000)
#             balance = random.randint(data.AGRESSIVE_TRADER_MAX_ABALANCE,data.AGRESSIVE_TRADER_MAX_ABALANCE)
#
#         super().__init__(balance,0,4,trader_id)
#         self.level2_data = level2_data
#
#         # self.holdings = random.randint(5000,100000)
#
#         self.ticks_held = 0 # for how much time latest order has been held
#
#         self.cooldown_tick  = 100 # the min ticks after which next action is allowed
#
#     def place_order(self,price_data) -> list:
#         p = random.random()
#         if self.is_takeprofit_hit(price_data[-1].Close):
#             return self.place_take_profit_order(price_data[-1].Close)
#         if p <= 0.01 and len(self.level2_data.sell_data):
#             # buy
#             # if self.level2_data.total_buy_volume > 5 * self.level2_data.total_sell_volume:
#             #     return []
#             price = self.level2_data.sell_prices[-1] * (1 + random.uniform(0,0.05))
#             # price = self.level2_data.sell_prices[-1]
#             # volume = int(self.level2_data.total_sell_volume * 0.01)
#             # volume = int(self.level2_data.total_sell_volume * 0.4)
#             volume = int(self.level2_data.total_sell_volume * 0.8)
#             volume = min(volume,int(self.balance/price))
#
#             buy_order = self.place_buy_order(price,volume)
#             if buy_order:
#                 percent = random.uniform(1.02,1.999)
#                 # self.take_profit_orders.append(price * 1.05, volume)
#                 self.take_profit_orders.append(price * percent, volume)
#                 # buy_order.print_details()
#                 # self.place_take_profit_order()
#                 return [buy_order]
#             # for price in self.level2_data.sell_data:
#             #     volume = int(self.level2_data.sell_data[price] * 0.01)
#             #     volume = min(volume,int(self.balance/price))
#             #     buy_order = self.place_buy_order(price,volume)
#             #     orders.append(buy_order)
#
#             # return orders
#
#         # elif p <= 0.01 and len(self.level2_data.buy_data):
#
#         elif p <= 0.012 and len(self.level2_data.buy_data):
#             # sell
#             price = self.level2_data.buy_prices[0]
#             volume = int(self.level2_data.total_buy_volume * 0.4)
#             volume = min(volume, self.holdings)
#
#             sell_order = self.place_sell_order(price,volume)
#             if sell_order:
#                 # sell_order.print_details()
#                 return [sell_order]
#
#             # orders = []
#             # for price in self.level2_data.buy_data:
#             #     volume = int(self.level2_data.buy_data[price] * 0.01)
#             #     volume = min(volume,self.holdings)
#             #     sell_order = self.place_sell_order(price,volume)
#             #     orders.append(sell_order)
#             #
#             # return orders
#
#         return []
#
#
#
# class LiquidityAbsorber(Trader):
#     # they buy opposite to what all do.If alot are selling they buy,absorb liquidity
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:
#             # balance = 100000000
#             balance = random.randint(data.LIQUIDITY_TRADERS_MIN_BALANCE,data.LIQUIDITY_TRADERS_MAX_BALANCE)
#
#         super().__init__(balance,0,5,trader_id)
#         self.level2_data = level2_data
#
#         # self.current_tick = 0
#         self.cooldown_tick  = random.randint(50,100) # the min ticks after which next action is allowed
#         self.ticks_held = self.cooldown_tick # for how much time latest order has been held
#         self.max_holding_ticks = random.randint(1,1000) # after which have to sell
#
#     def place_order(self,price_data) -> list:
#         # self.current_tick += 1
#         self.ticks_held += 1
#         if self.is_takeprofit_hit(price_data[-1].Close):
#             return self.place_take_profit_order(price_data[-1].Close)
#         if self.ticks_held < self.cooldown_tick:
#             return []
#
#         budget = self.balance / 10
#         imbalance = (self.level2_data.total_buy_volume - self.level2_data.total_sell_volume)/(self.level2_data.total_buy_volume + self.level2_data.total_sell_volume)
#
#         momentum = self.momentum(price_data, 3)
#
#         # if imbalance < -0.2 and momentum == 1:
#         if imbalance < -0.55 :
#         # if imbalance < -0.55 and momentum == 1:
#             # means selling pressure in market
#             # ok time to absorb selling pressure
#             # price_change = (price_data[-1].Close - price_data[-2].Close) / price_data[-2].Close
#
#             # if random.random() < 0.1 and price_change < -0.002: # make trade only if price is changing
#             if random.random() < 0.1 :  # make trade only if price is changing
#                 # as there can be many such traders so to avoid every trader to buy and sell at same time
#                 buy_price = self.level2_data.sell_prices[0]
#                 buy_price = random.uniform(buy_price * 0.99,buy_price * 1.01)
#
#                 # buy_volume = int(self.level2_data.total_sell_volume * 0.1) # 10 % of total sell volume
#                 # buy_volume = int((self.level2_data.total_sell_volume - self.level2_data.total_buy_volume) * 0.02) # 20 % of total sell volume
#                 # buy_volume = int((self.level2_data.total_sell_volume - self.level2_data.total_buy_volume) * 0.2) # 2 % of total sell volume
#                 buy_volume = int((self.level2_data.total_sell_volume - self.level2_data.total_buy_volume) * 0.6) # 2 % of total sell volume
#
#                 if buy_price * buy_volume > budget:
#                     # if required amount more than budget
#                     buy_volume = int(budget / buy_price)
#
#                 self.ticks_held = 0
#                 buy_order = self.place_buy_order(buy_price,buy_volume)
#                 self.take_profit_orders.append(buy_price * 1.02,buy_volume)
#                 return [buy_order]
#
#         elif (imbalance >= 0 or self.ticks_held >= self.max_holding_ticks) and momentum == -1:
#             # buy pressure time to sell
#             # sell_volume = int((self.level2_data.total_buy_volume-self.level2_data.total_sell_volume) * 0.02)  # 2 % of total sell volume
#             # sell_volume = int((self.level2_data.total_buy_volume-self.level2_data.total_sell_volume) * 0.2)  # 2 % of total sell volume
#             sell_volume = int((self.level2_data.total_buy_volume-self.level2_data.total_sell_volume) * 0.6)  # 2 % of total sell volume
#
#             sell_quantity = min(self.holdings,sell_volume)
#             # sell_price = price_data[-1].Close
#             sell_price = self.level2_data.buy_prices[-1]
#             self.ticks_held = 0
#             sell_order = self.place_sell_order(sell_price,sell_quantity)
#             return [sell_order]
#
#         return []
#
#
# class Bears(Trader):
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:
#             balance = 1000000
#         super().__init__(balance,0,6,trader_id)
#         self.level2_data = level2_data
#
#     def place_order(self,price_data) -> list:
#         if random.random() < 0.01 and len(self.level2_data.buy_prices):
#             max_c = 8
#             if len(price_data) >= max_c + 1:
#                 n = random.randint(4,max_c)
#                 for i in range(n):
#                     if not price_data[-(i + 1)].isGreen():
#                         return []
#                 sell_orders = []
#                 k = random.randint(5,30)
#                 volume = int(self.holdings * 0.25/k)
#                 for i in range(k):
#                     price = random.uniform(price_data[-1].Close * 0.98,price_data[-1].Close * 1.02)
#                     order = self.place_sell_order(price,volume)
#                     sell_orders.append(order)
#                 return sell_orders
#                 # volume = int(self.holdings * 0.25)
#                 # volume = min(volume,self.holdings)
#                 # price = self.level2_data.buy_prices[0]
#                 # sell_order = self.place_sell_order(price,volume)
#                 # return [sell_order]
#
#         return []
#
#
#
# class LiquidityAbsorber2(Trader):
#     # they buy opposite to what all do.If alot are selling they buy,absorb liquidity
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:
#             # balance = 100000000
#             balance = random.randint(data.LIQUIDITY_TRADERS_MIN_BALANCE,data.LIQUIDITY_TRADERS_MAX_BALANCE)
#
#         super().__init__(balance,0,7,trader_id)
#         self.level2_data = level2_data
#
#         # self.current_tick = 0
#         self.cooldown_tick  = random.randint(50,10000) # the min ticks after which next action is allowed
#         self.max_holding_ticks = random.randint(1,1000) # after which have to sell
#         self.ticks_held = self.cooldown_tick # for how much time latest order has been held
#
#     def place_order(self,price_data) -> list:
#         # self.current_tick += 1
#         self.ticks_held += 1
#         if self.ticks_held < self.cooldown_tick:
#             return []
#
#         budget = self.balance / 10
#         imbalance = (self.level2_data.total_buy_volume - self.level2_data.total_sell_volume)
#         momentum = self.momentum(price_data, 5)
#
#         # if imbalance < 0:
#         if self.level2_data.total_sell_volume > 2 * self.level2_data.total_buy_volume and momentum == 1:
#             # means selling pressure in market
#             # ok time to absorb selling pressure
#             # price_change = (price_data[-1].Close - price_data[-2].Close) / price_data[-2].Close
#
#             if random.random() < 0.01: # make trade only if price is changing
#                 # as there can be many such traders so to avoid every trader to buy and sell at same time
#                 # buy_price = self.level2_data.sell_prices[0]
#                 buy_price = price_data[-1].Close * 1.01
#                 # buy_volume = int((self.level2_data.total_sell_volume - self.level2_data.total_buy_volume) * 0.01) # 2 % of total sell volume
#                 buy_volume = int((self.level2_data.total_sell_volume - self.level2_data.total_buy_volume) * 0.3) # 2 % of total sell volume
#
#                 if buy_price * buy_volume > budget:
#                     # if required amount more than budget
#                     buy_volume = int(budget / buy_price)
#
#                 self.ticks_held = 0
#                 buy_order = self.place_buy_order(buy_price,buy_volume)
#                 return [buy_order]
#
#         # elif imbalance >= 0 or self.ticks_held >= self.max_holding_ticks:
#         elif (self.level2_data.total_buy_volume > 2 * self.level2_data.total_sell_volume or self.ticks_held >= self.max_holding_ticks) and momentum == -1:
#             # buy pressure time to sell
#             # sell_volume = int((self.level2_data.total_buy_volume-self.level2_data.total_sell_volume) * 0.01)  # 2 % of total sell volume
#             sell_volume = int((self.level2_data.total_buy_volume-self.level2_data.total_sell_volume) * 0.3)  # 2 % of total sell volume
#
#             sell_quantity = min(self.holdings,sell_volume)
#             # sell_price = price_data[-1].Close
#             sell_price = price_data[-1].Close * 0.99
#             self.ticks_held = 0
#             sell_order = self.place_sell_order(sell_price,sell_quantity)
#             return [sell_order]
#
#         return []
#
#
# # class BigInstitute(Trader):
# #     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
# #         if balance == 0:
#
#
# # class Level3Trader
# # :
# #     def __init__(self,indicators : IndicatorEngine,trader_id : int,balance : float = 0):
# #         if balance == 0:
# #
# #         super().__init__(balance, 0, 3, trader_id)














# TODO : stoploss and take profit are both linked ie if one gets executed other gets canceled


# 0 : random trader, 1 : level_1_trader, 2 : level_2_trader
import bisect
# level_1_trader
# buy and sell seeing candle
# eg : if last n candles are green they buy


# you must explicitly call stop_loss order for each trader


from collections import deque
import random

from pygame.examples.music_drop_fade import volume

from order import Order
from candle import Candle
from indicators import IndicatorEngine
from strategies import Strategies
from level2data import Level2Data
from stoploss_handler import StopLoss,TakeProfit
from positions import Position
import data


class Trader:
    def __init__(self,balance : float,holdings : int,trader_type : int,trader_id : int):
        # balance is the amount of money the trader is having
        # holdings represents total no of shares that the trader has been holding
        # trader type denotes which kind of trader eg: random,Institute etc
        # trader id : as there can be many traders of same type
        # balance will be deducted the moment you place a order
        # stock will be added in the holdings only when order gets filled
        self.trader_type = trader_type
        self.trader_id = trader_id
        self.starting_balance = balance # the actual balance the trader starts with
        self.balance = balance
        self.holdings = holdings
        self.total_trades = 0
        self.new_starting_balance = self.starting_balance # will change starting balance after all holding are sold
        self.all_orders = deque() # contains all active orders.
        self.p_l = 0
        # self.buy_orders = {} # only contains active buy orders with id as key. and when order is sold it would be removed
        # self.stop_loss_orders = [] # contains [stop_loss,quantity] ,stores in increasing stoploss
        self.stop_loss_orders = StopLoss() # contains all stoploss orders
        self.take_profit_orders = TakeProfit() # contains all stoploss orders
        # self.take_profit_orders = {} # contains price as key and [stop_loss,quantity]

    def place_order(self,price_data) -> list:
        # price_data contains all candles
        # price_data = list[Candle]
        return []

    def place_stoploss_orders(self,current_price) -> list:
        # if you bought 100 shares and put a stoploss on it
        # and sold even one share then stoploss order will be canceled

        # if you bought 50 shares today with stoploss on day 1 and 50 shares next day with no stoploss on day 2
        # and next to next day you sold 50 shares ,the day 1 shares will be sold first and
        # stoploss order will be still active
        if len(self.stop_loss_orders.stoploss_orders) == 0:
            return []

        orders = []
        top_order = self.stop_loss_orders.stoploss_orders[-1]
        # while top_order[0] < current_price:

        # ie price went below stoploss
        while current_price <= top_order[0]:
            order = self.place_sell_order(top_order[0],top_order[1])
            if order:
                orders.append(order)
            self.stop_loss_orders.pop()
            if len(self.stop_loss_orders.stoploss_orders) == 0:
                break
            top_order = self.stop_loss_orders.stoploss_orders[-1]

        return orders

    def place_take_profit_order(self,current_price) -> list:
        # places take_profit orders
        # if you bought 100 shares and put a take profit on it
        # and sold even one share then take profit order will be canceled

        # if you bought 50 shares today with take profit on day 1 and 50 shares next day with no take profit on day 2
        # and next to next day you sold 50 shares ,the day 1 shares will be sold first and
        # take profit order will be still active

        if len(self.take_profit_orders.take_profit_orders) == 0:
            return []

        orders = []
        top_order = self.take_profit_orders.take_profit_orders[0]
        # while top_order[0] < current_price:
        # ie price went above take_profit
        while current_price >= top_order[0]:
            order = self.place_sell_order(top_order[0], top_order[1])
            if order:
                orders.append(order)
            self.take_profit_orders.pop()
            if len(self.take_profit_orders.take_profit_orders) == 0:
                break
            top_order = self.take_profit_orders.take_profit_orders[0]

        return orders

    def is_stoploss_hit(self,current_price) -> bool:
        # returns true if stop_loss hit
        return self.stop_loss_orders.stoploss_orders and current_price <= self.stop_loss_orders.stoploss_orders[-1][0]

    def is_takeprofit_hit(self,current_price) -> bool:
        # returns true if take_profit hit
        return self.take_profit_orders.take_profit_orders and current_price >= self.take_profit_orders.take_profit_orders[0][0]

    def place_buy_order(self,price,quantity):
        # stop_loss is exact price below which sell order will be placed

        if quantity <= 0 or price <= 0:
            return None

        buy_order = Order(data.ORDER_ID, self.trader_id, price, quantity, 0, data.TIME)

        if self.balance < price * quantity:
            return None

        self.balance -= price * quantity
        data.ORDER_ID += 1

        # if stop_loss > 0:
        #     self.stop_loss_orders.append(stop_loss,quantity)

        return buy_order

    def sell_order_util(self,price,quantity):
        # will remove active orders from queue
        if len(self.all_orders) == 0:
            return
        top_order = self.all_orders[0]
        while quantity >= top_order.quantity:
            quantity -= top_order.quantity
            top_order.quantity = 0
            self.all_orders.pop()
            if quantity == 0 or len(self.all_orders) == 0:
                return
            top_order = self.all_orders[0]

        top_order.quantity -= quantity

    def place_sell_order(self,price,quantity):
        # while selling if after selling total stoploss order > total holding
        # then remove the stoploss order which is recently added
        # if quantity <= 0 :
        if quantity <= 0 or self.holdings <= 0:
            self.holdings = 0
            return None
        sell_order = Order(data.ORDER_ID, self.trader_id, price, quantity, 1, data.TIME)
        self.holdings -= quantity

        self.stop_loss_orders.pop_recent(self.holdings) # if stoploss orders > holding pop recently added stoploss order

        self.take_profit_orders.pop_recent(self.holdings) # if takeprofit orders > holding pop recently added takeprofit order

        data.ORDER_ID += 1
        self.sell_order_util(price,quantity)
        if self.holdings == 0:
            # all holdings are sold now new balance
            # used for profit and loss finding
            self.new_starting_balance = self.balance

        # self.all_orders[sell_order.order_id] = sell_order
        return sell_order

    def place_short_order(self,price,quantity):
        # shorting stock means taking share from someone and promising him to return the share within some days with interest
        # you sell the share immadiately and if price decrease you get profit
        # till now no margin is added
        # at end of short place buy order with same quantity
        amount = price * quantity
        if self.balance > amount:
            self.holdings -= quantity
            self.balance -= amount

    def add_holding(self,price,quantity,order = None):
        # order has been matched
        # for buying
        # used by exchange
        self.holdings += quantity
        # self.all_orders.append(order) # appending active order in queue
        self.all_orders.append(Position(price,quantity)) # appending active order in queue

    def add_balance(self,price,quantity,order = None) -> bool:
        # order has been matched
        # for selling
        # used by exchange
        self.balance += quantity * price
        return False

    def momentum(self, price_data: list, n: int, threshold: float = 0.01) -> int:
        # helper function
        # tells whether there is a momentum in price
        # n = no of candles to look for
        # if there is a change in price of more than threshold and if more no of green candles
        # threshold = percent/100
        # 1 : buy,-1 = sell,0 = hold
        if not len(price_data) >= n+1:
            return 0
        min_price = price_data[-1].Close
        max_price = price_data[-1].Close
        green = red = 0

        for i in range(n):
            min_price = min(min_price, price_data[-(i + 1)].Low)
            max_price = max(max_price, price_data[-(i + 1)].High)
            if price_data[-(n+1)].isGreen():
                green += 1
            else:
                red += 1

        p = (max_price - min_price) / min_price
        if p > threshold and abs(price_data[-2].Close - price_data[-2].Open)/price_data[-2].Open > threshold:
            if green > red:
                return 1
            return -1

        return 0

    def get_price(self,price_data,level2_data : Level2Data,buy_price = True):
        # returns a price at which the trader can buy or sell
        # there are two options 1. the moment it gets placed it will be matched 2. it will sit in the order book
        # buy_price means price for buying will be return else sell_price
        # return price_data[-1].Close * random.uniform(0.99,1.01)
        threshold = 0.8
        if buy_price == True:
            p =  random.random()
            # if p < 0.7:
            if p < threshold:
                # order will get matched
                # meaning buying at price > best ask price -> immadiate execution
                # return random.uniform(level2_data.sell_prices[0],level2_data.sell_prices[-1])
                if len(level2_data.sell_prices) == 0:
                    return price_data[-1].Close * random.uniform(1,1.02) # they are ready to pay more so order placed immadiately

                return level2_data.sell_prices[-1] * random.uniform(1,1.001)
            else:
                # order will sit in the order book
                # meaning price < best ask price -> will not be matched therefore will sit in order book
                if len(level2_data.sell_prices) == 0:
                    return price_data[-1].Close * random.uniform(0.98,1)

                # return level2_data.sell_prices[0] * random.uniform(0.995,0.998)
                return level2_data.sell_prices[0] * random.uniform(0.9,0.999)

        else:
            p = random.random()
            # if p < 0.7:
            if p < threshold:
                # order will get matched
                # meaning selling at price < best bid price -> immadiate execution
                # return random.uniform(level2_data.buy_prices[0],level2_data.buy_prices[-1])
                if len(level2_data.buy_prices) == 0:
                    return price_data[-1].Close * random.uniform(0.99,1)
                return level2_data.buy_prices[0] * random.uniform(0.999,1)
            else:
                # order will sit in the order book
                # meaning price > best bid price -> will not be matched therefore will sit in order book
                if len(level2_data.buy_prices) == 0:
                    return price_data[-1].Close * random.uniform(1,1.01)
                # return level2_data.buy_prices[-1] * random.uniform(1.001,1.003)
                return level2_data.buy_prices[-1] * random.uniform(1.001,1.01)


    def cancel_order(self,order : Order):
        # will be called by exchange
        # TODO : canceled order must be put in the active orders again
        order.status = 2
        if order.trade_type == 0:
            # buy order cancel
            self.balance += order.quantity * order.price
        else:
            # sell order cancel
            self.holdings += order.quantity
        # self.all_orders.remove(order)
        del order

    def print_summary(self):
        print()
        print("==== Trader Summary ====")
        print("Trader Id : ", self.trader_id , " Trader Type : ", self.trader_type)
        print("Total Trades made : ", self.total_trades)
        print("Starting Balance : ", self.starting_balance , " Final Balance : " , self.balance)


class Company(Trader):
    # they are needed to supply with liquidity in market
    # they will sell in huge quantity and market sentiment will become little negative seeing this so more people will sell
    # problem : company placing a lot of order at same price and at a same time
    def __init__(self,trader_id):
        super().__init__(data.COMPANY_BALANCE,0,8,trader_id)
        self.ticks_held = 0
        self.cool_down_ticks = 100 # dont do before 100 ticks
        # self.action_ticks = 10 # company announces before that they are going to buy or sell and 10 is the ticks before which they will execute
        # self.action_t = 0 # counts action tick
        # self.action_quantity = 0 # the quantity the company is going to buy or sell , + for buy ,- for sell

    def place_order(self,price_data) -> list:
        self.ticks_held += 1
        # self.action_ticks += 1

        return []

        # if self.action_quantity and self.action_t < self.action_ticks:
            # return []

        if self.ticks_held < self.cool_down_ticks or random.random() > 0.1:
            return []

        buy_sell = random.random()

        if buy_sell < 0.5:
            # buy
            # company will buy at price more than current_price
            orders = []
            # price = price_data[-1].Close * 1.05
            quantity = random.randint(1000,20000)
            n = random.randint(10,30)
            per_quantity = int(quantity/n)
            for i in range(n):
                price = price_data[-1].Close * random.uniform(1,1.01)
                if price * per_quantity <= self.balance:
                    buy_order = self.place_buy_order(price,per_quantity)
                    orders.append(buy_order)
                    # return [self.place_buy_order(price,quantity)]

            self.ticks_held = 0
            return orders

        else:
            # sell
            # company will sell at cheaper than current price
            quantity = random.randint(1000,20000)
            n = random.randint(10,30)
            per_quantity = int(quantity/n)
            orders = []
            for i in range(n):
                if self.holdings > per_quantity:
                    price = price_data[-1].Close * random.uniform(0.99,1)
                    sell_order = self.place_sell_order(price,per_quantity)
                    orders.append(sell_order)

            self.ticks_held += 1
            return orders




class Whales(Trader):
    # whales buy and sell in huge quantity
    def __init__(self,level_2_data : Level2Data,trader_id):
        super().__init__(data.COMPANY_BALANCE,0,9,trader_id)

        self.cool_down_ticks = random.randint(70,200) # dont do before 100 ticks
        self.ticks_held = self.cool_down_ticks - 50
        # self.action_ticks = 10 # company announces before that they are going to buy or sell and 10 is the ticks before which they will execute
        # self.action_t = 0 # counts action tick
        # self.action_quantity = 0 # the quantity the company is going to buy or sell , + for buy ,- for sell
        self.level_2_data = level_2_data

    def make_decision(self,price_data):
        # sentiment
        # +1 -> strong bullish
        # 0 -> neutral
        # -1 -> strong bearish
        if self.level_2_data.total_buy_volume + self.level_2_data.total_sell_volume == 0:
            sentiment = 0
        else:
            sentiment = (self.level_2_data.total_buy_volume - self.level_2_data.total_sell_volume) / (self.level_2_data.total_buy_volume + self.level_2_data.total_sell_volume)

        if sentiment > 0.8 and data.MARKET_SENTIMENT <= -0.6:
            # bullish therefore sell
            return -1
        elif sentiment < -0.8 and data.MARKET_SENTIMENT >= 0.6:
            # bearish therefore bull
            return 1

        return 0

        # if sentiment >= 0.5
        #     return 1

    def place_order(self,price_data) -> list:
        self.ticks_held += 1

        if self.ticks_held <= self.cool_down_ticks:
            return []

        if random.random() >= 0.001:
            return []

        out = self.make_decision(price_data)
        if self.level_2_data.total_buy_volume + self.level_2_data.total_sell_volume == 0:
            sentiment = 0
        else:
            sentiment = (self.level_2_data.total_buy_volume - self.level_2_data.total_sell_volume) / (self.level_2_data.total_buy_volume + self.level_2_data.total_sell_volume)

        if out == 1:
            # buy
            # quantity = int(self.level_2_data.total_sell_volume / 10)
            # quantity = int(abs(sentiment) * self.level_2_data.total_sell_volume)
            quantity = int(abs(sentiment) * abs(self.level_2_data.total_sell_volume-self.level_2_data.total_buy_volume))
            quantity = min(quantity,10000)
            # price = self.get_price(price_data,self.level_2_data)
            price = price_data[-1].Close * random.uniform(0.99,1)
            if self.balance >= price * quantity:
                # print(quantity, " buy")

                buy_order = self.place_buy_order(price,quantity)
                self.ticks_held = 0
                return [buy_order]

        elif out == -1:
            # price = self.get_price(price_data,self.level_2_data,False)
            # quantity = int(self.level_2_data.total_buy_volume / 10)
            price = price_data[-1].Close * random.uniform(1,1.01)
            # quantity = int(abs(sentiment) * self.level_2_data.total_buy_volume)
            quantity = int(abs(sentiment) * abs(self.level_2_data.total_sell_volume-self.level_2_data.total_buy_volume))
            quantity = min(quantity,10000)

            quantity = min(quantity,self.holdings)
            # print(quantity, " sell")

            sell_order = self.place_sell_order(price,quantity)
            self.ticks_held = 0

            return [sell_order]

        return []
        # self.action_ticks += 1

        # if self.action_quantity and self.action_t < self.action_ticks:
            # return []

        # if self.ticks_held < self.cool_down_ticks or random.random() > 0.1:
        #     return []
        #
        # buy_sell = random.random()
        #
        # if buy_sell < 0.5:
            # buy
            # company will buy at price more than current_price
            # orders = []
            # quantity = random.randint(1000,20000)
            # n = random.randint(10,30)
            # per_quantity = int(quantity/n)
            # for i in range(n):
            #     price = price_data[-1].Close * random.uniform(1,1.01)
            #     if price * per_quantity <= self.balance:
            #         buy_order = self.place_buy_order(price,per_quantity)
            #         orders.append(buy_order)
            #         return [self.place_buy_order(price,quantity)]
            #
            # self.ticks_held = 0
            # return orders

        # else:
        #     sell
        #     company will sell at cheaper than current price
        #     quantity = random.randint(1000,20000)
        #     n = random.randint(10,30)
        #     per_quantity = int(quantity/n)
        #     orders = []
        #     for i in range(n):
        #         if self.holdings > per_quantity:
        #             price = price_data[-1].Close * random.uniform(0.99,1)
        #             sell_order = random.uniform(price,per_quantity)
        #             orders.append(sell_order)
        #
        #     self.ticks_held += 1
        #     return orders
#

class RandomTrader(Trader):
    # random traders
    # they buy and sell randomly to create noise
    def __init__(self,level_2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            balance = random.uniform(data.RANDOM_MIN_BALANCE,data.RANDOM_MAX_BALANCE)

        super().__init__(balance,0,0,trader_id)

        self.cool_down = random.randint(5,30)
        self.ticks_held = self.cool_down
        self.level_2_data = level_2_data

    def place_order(self, price_data) -> list:
        self.ticks_held += 1

        if self.ticks_held <= self.cool_down:
            return []

        p = random.random()

        if p < 0.001:
            if random.random() < 0.5:
                # buy
                price = price_data[-1].Close * random.uniform(0.99,1.01)
                # price = self.get_price(price_data,level2_data=self.level_2_data,buy_price = True)
                budget = int(self.balance / 10) # their budget is 10 % of their total balance
                quantity = int(budget / price)
                if quantity == 0:
                    budget = self.balance
                    quantity = int(budget / price)
                return [self.place_buy_order(price,quantity)]

            elif self.holdings:
                # sell
                price = price_data[-1].Close * random.uniform(0.99,1.01)
                # price = self.get_price(price_data,level2_data=self.level_2_data,buy_price = False)
                quantity = random.randint(1,self.holdings)
                return [self.place_sell_order(price,quantity)]

        return []


class Level1Trader(Trader):
    # Level1 Trader -> momentum trader
    # they are also intraday trader so they must sell all holdings after some time in the day
    # will buy and sell by seeing last n candles
    # eg : if last 3 candles are green buy
    # if price goes below 20% of what they bought at sell
    def __init__(self,level_2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            balance = random.randint(data.LEVEL1_TRADER_MIN_BALANCE,data.LEVEL1_TRADER_MAX_BALANCE)
        super().__init__(balance,0,1,trader_id)

        self.level_2_data = level_2_data

        self.n = random.randint(1,data.MAX_LAST_CANDLE_VIEW)
        self.ticks_held = 0
        self.cooldown = random.randint(1,20)
        self.intraday_threshold = random.randint(data.LEVEL1_TRADER_INTRADAY_MIN_THRESHOLD,data.DAY_LENGTH_TICKS) # at this time they forcibly sell all their holdings
        self.intraday_threshold = self.intraday_threshold * random.randint(0,1)

    def make_decision(self,price_data) -> int:
        # 1 = buy,-1 = sell,0 = do nothing
        # will sell last 3 candles
        n = 3
        if len(price_data) >= n + 1:
            min_price = max_price = price_data[-2].Close
            green = 0
            for i in range(n):
                min_price = min(min_price,price_data[-(i+1)].Low)
                max_price = max(max_price,price_data[-(i+1)].High)
                if price_data[-(i+1)].isGreen():
                    green += 1

            if (max_price - min_price) / min_price > 0.01: # change is greater than 1 %
                if green >= n/2:
                    return 1
                return -1

        return 0

    def place_order(self, price_data) -> list:
        self.ticks_held += 1

        if self.intraday_threshold > 0 and not True:
        # if self.intraday_threshold > 0:
            r = data.TIME % data.DAY_LENGTH_TICKS

            if r == self.intraday_threshold:
                # now they must sell all
                if self.holdings:
                    # now must sell
                    # price = price_data[-1].Close * random.uniform(0.999,1.001)
                    price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=False)
                    return [self.place_sell_order(price,self.holdings)]

                return []

            elif r > self.intraday_threshold:
                # no buying at this point
                return []

        if self.is_takeprofit_hit(price_data[-1].Close):
            return self.place_take_profit_order(price_data[-1].Close)

        if random.random() < 0.001:
            price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=False)
            self.ticks_held = 0

            return [self.place_sell_order(price, self.holdings)]

        # if self.ticks_held <= self.cooldown or random.random() >= 0.01:
        if self.ticks_held <= self.cooldown:
            return []

        if random.random() > 0.01:
            return []

        buy_sell = self.make_decision(price_data)

        if buy_sell == 1:
            # buy
            # price = price_data[-1].Close * random.uniform(0.99,1.01)
            price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=True)
            budget = int(self.balance / 10)  # their budget is 10 % of their total balance
            quantity = int(budget/price)

            if quantity == 0:
                budget = self.balance
                quantity = int(budget/price)

            self.ticks_held = 0

            buy_order = self.place_buy_order(price,quantity)

            if buy_order:
                self.take_profit_orders.append(price * 1.1,quantity)
                return [buy_order]

        elif buy_sell == -1 and self.holdings > 0:
            # sell
            # price = price_data[-1].Close * random.uniform(0.99,1.01)
            price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=False)
            quantity = random.randint(1,self.holdings)

            self.ticks_held = 0

            return [self.place_sell_order(price,quantity)]

        return []


class Level2Trader(Trader):
    # Level2 trader are better than level1 trader
    # they use ema ,rsi to buy and sell
    def __init__(self,level_2_data : Level2Data,indicators : IndicatorEngine,trader_id : int,balance : float = 0):
        if balance == 0:
            balance = random.randint(data.LEVEL2_TRADER_MIN_BALANCE,data.LEVEL2_TRADER_MAX_BALANCE)
        # indicators = a class which contains all indicators
        super().__init__(balance,0,2,trader_id)

        self.indicators = indicators
        self.strategies = Strategies()
        self.level_2_data = level_2_data
        # self.three_emas = [data.EMA_PERIODS[-1],random.choice([data.EMA_PERIODS[1],data.EMA_PERIODS[2]]),data.EMA_PERIODS[0]] #  long term,slow,fast
        # self.single_ema = random.choice(data.EMA_PERIODS) # single ema

        self.ticks_held = 0
        self.cool_down = random.randint(5,100)

        # 0 : simple ema strategy -> buy if price above ema and sell if below
        # 1 : if rsi below 30 buy else if rsi above 70 sell
        # 2 : bollinger band
        self.strategy_type = random.randint(0,2)

    def make_decision(self,price_data):
        # 1 : buy,-1 : sell,0 : do nothing
        p = random.uniform(0.6, 1)

        # if data.MARKET_SENTIMENT >= p:
        #     return 1
        # elif data.MARKET_SENTIMENT <= -p:
        #     return -1

        if self.strategy_type == 0:
            # simple ema crossover
            ema_period = random.choice(data.EMA_PERIODS)
            output = self.strategies.single_ema(self.indicators.ema_values[ema_period],price_data[-1].Close)
            return output

        elif self.strategy_type == 1:
            # rsi strategy
            output = self.strategies.rsi_strategy(self.indicators.rsi_value)
            return output

        elif self.strategy_type == 2:
            # bollinger band strategy
            output = self.strategies.bollinger_strategy(price_data[-1].Close,self.indicators.bb_upper,self.indicators.bb_lower)
            return output

        return 0

    def place_order(self, price_data) -> list:
        self.ticks_held += 1

        if self.is_takeprofit_hit(price_data[-1].Close):
            return self.place_take_profit_order(price_data[-1].Close)

        if self.ticks_held <= self.cool_down or random.random() >= 0.01:
            return []

        buy_sell = self.make_decision(price_data)

        # print(self.indicators.rsi_value)

        if buy_sell == 1:
            # buy
            price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=True)
            # price = price_data[-1].Close * random.uniform(0.99,1.01)
            budget = int(self.balance / 20)
            quantity = int(budget / price)

            if quantity == 0:
                budget = self.balance
                quantity = int(budget / price)

            buy_order = self.place_buy_order(price,quantity)

            if buy_order:
                pr = random.uniform(1,2)
                self.take_profit_orders.append(price * pr,quantity)
                self.ticks_held = 0
                return [buy_order]

        elif buy_sell == -1 and self.holdings > 0:
            # price = price_data[-1].Close * random.uniform(0.99,1.01)
            price = self.get_price(price_data, level2_data=self.level_2_data, buy_price=False)
            quantity = random.randint(1,self.holdings)
            sell_order = self.place_sell_order(price,quantity)

            if sell_order:
                self.ticks_held = 0
                return [sell_order]

        return []


class MarketMaker(Trader):
    # they are called market makers because they provide liquidity
    # they earn from spread if share at 100 to buy at 100 at same time sell at 100.01
    # they should have good amount of initial shares
    def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            balance = 30000000

        super().__init__(balance,0,3,trader_id)

        self.level2_data = level2_data

        self.ticks_held = 0 # for how much time latest order has been held

        self.cooldown_tick  = 30 # the min ticks after which next action is allowed
        # self.delta = 0.0005 # by this difference they earn

    def place_order(self,price_data) -> list:
        self.ticks_held += 1

        if self.ticks_held <= self.cooldown_tick:
            return []

        if random.random() >= 0.05:
            return []

        quantity = 50
        orders = []

        if len(self.level2_data.buy_prices) > 0 and len(self.level2_data.sell_prices) > 0:
            fair_price = (self.level2_data.buy_prices[-1] + self.level2_data.sell_prices[0])/2
        else:
            fair_price = price_data[-1].Close
        spread = fair_price * 0.001

        buy_price = fair_price - spread
        sell_price = fair_price + spread

        # price = self.get_price(price_data, self.level2_data)
        price = self.level2_data

        if self.balance > quantity * buy_price:
            buy_order = self.place_buy_order(buy_price,quantity)
            orders.append(buy_order)

        if quantity < self.holdings:
            # sell
            # price = self.get_price(price_data,self.level2_data,False)
            sell_order = self.place_sell_order(sell_price,quantity)
            orders.append(sell_order)

        self.ticks_held = 0
        return orders


class AgressiveTraders(Trader):
    # they are agressive buyers and seller. ie they sell at lowest ask, and buy at best bid
    def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            balance = random.randint(data.AGRESSIVE_TRADER_MAX_ABALANCE,data.AGRESSIVE_TRADER_MAX_ABALANCE)

        super().__init__(balance,0,4,trader_id)
        self.level2_data = level2_data

        self.strategies = Strategies()
        self.indicators = indicators

        self.ticks_held = 0 # for how much time latest order has been held
        self.cooldown_tick  = random.randint(30,200) # the min ticks after which next action is allowed
        self.ema_period = random.choice(data.EMA_PERIODS)

    def make_decision(self,price_data) -> int:
        # 1 : buy,-1 : sell,0 : do nothing
        bollinger_output = self.strategies.bollinger_strategy(price_data[-1].Close, self.indicators.bb_upper,self.indicators.bb_lower)
        rsi = self.indicators.rsi()
        output = self.strategies.single_ema(self.indicators.ema_values[self.ema_period], price_data[-1].Close)
        vwap = self.indicators.vwap_value()

        # p = random.uniform(0.6, 1)
        #
        # if data.MARKET_SENTIMENT >= p:
        #     return 1
        # elif data.MARKET_SENTIMENT <= -p:
        #     return -1

        change = (price_data[-1].Close - vwap) / vwap
        # threshold = 0.01
        threshold = random.uniform(0.001,0.05)

        # if change >= threshold and not len(self.level2_data.sell_prices) > 4 * len(self.level2_data.buy_prices):
        #         return -1
        # elif change <= -threshold and not len(self.level2_data.buy_prices) > 4 * len(self.level2_data.sell_prices):
        #     return 1
        return bollinger_output

        # if output == -1:
        # if rsi < 30:
            # buy
            # return 1
        #
        # elif output == 1:
        # elif rsi > 70:
            # sell
            # return -1

        return 0

    def place_order(self,price_data) -> list:
        self.ticks_held += 1

        if self.is_takeprofit_hit(price_data[-1].Close):
            return self.place_take_profit_order(price_data[-1].Close)

        if self.ticks_held <= self.cooldown_tick:
            return []

        if random.random() >= 0.005:
            return []

        out = self.make_decision(price_data)

        if out == 1:
            # buy
            # quantity = int(0.4 * (price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume)/3)
            # quantity = int(0.05 * (price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume)/3)
            quantity = int(0.01 * (price_data[-2].Volume + price_data[-3].Volume)/2)
            quantity = max(quantity,150)
            n = random.randint(5,30)

            per_quantity = int(quantity / n)

            orders = []

            for i in range(n):
                # price = price_data[-1].Close * random.uniform(0.99, 1.01)
                price = self.get_price(price_data, level2_data=self.level2_data, buy_price=True)
                if price * per_quantity > self.balance:
                    break

                buy_order = self.place_buy_order(price,quantity)
                self.take_profit_orders.append(price * random.uniform(1,1.3),per_quantity)

                orders.append(buy_order)

            self.ticks_held = 0

            return orders

        elif out == -1 and self.holdings > 0:
            # sell
            # quantity = int(0.01 * (price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume)/3)
            quantity = int(0.01 * (price_data[-2].Volume + price_data[-3].Volume)/2)
            quantity = max(quantity,100)
            quantity = min(quantity,self.holdings)

            n = random.randint(5,30)

            per_quantity = int(quantity / n)

            orders = []

            for i in range(n):
                # price = price_data[-1].Close * random.uniform(0.98, 1)
                price = self.get_price(price_data, level2_data=self.level2_data, buy_price=False)
                sell_order = self.place_sell_order(price,per_quantity)
                orders.append(sell_order)

            self.ticks_held = 0

            return orders

        return []



class LiquidityAbsorber(Trader):
    # they buy opposite to what all do.If alot are selling they buy,absorb liquidity
    def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            # balance = 100000000
            balance = random.randint(data.LIQUIDITY_TRADERS_MIN_BALANCE,data.LIQUIDITY_TRADERS_MAX_BALANCE)

        super().__init__(balance,0,5,trader_id)
        self.level2_data = level2_data

        # self.current_tick = 0
        self.cooldown_tick  = random.randint(50,100) # the min ticks after which next action is allowed
        self.ticks_held = self.cooldown_tick # for how much time latest order has been held
        self.max_holding_ticks = random.randint(1,1000) # after which have to sell

    def place_order(self,price_data) -> list:
        return []


class Bears(Trader):
    def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            # balance = 100000
            balance = random.randint(10000,100000)
        super().__init__(balance,0,6,trader_id)
        self.indicators = indicators
        self.level2_data = level2_data
        self.strategies = Strategies()

        self.cool_down = random.randint(30,200)
        self.ticks_held = self.cool_down - 30

        self.buy_rsi_threshold = random.uniform(0,50)
        self.sell_rsi_threshold = random.uniform(50,100)

    def make_decision(self,price_data) -> int:
        # 1 : buy,-1 : sell,0 : do nothing
        # they will use rsi and vwap
        # sell if rsi > 70 and price and vwap difference is >= 5%
        # rsi_output = self.strategies.rsi_strategy(self.indicators.rsi_value)
        rsi_output = self.indicators.rsi()
        vwap = self.indicators.vwap_value()
        change = (price_data[-1].Close - vwap)/vwap

        if rsi_output < self.buy_rsi_threshold:
            return 1
        elif rsi_output > self.sell_rsi_threshold:
            return -1

        return 0
        # print("rsi " ,self.indicators.rsi())
        # print(rsi_output)

        # if rsi_output == -1 and change >= 0.01:
        # if rsi_output == -1 :
        #     sell
        #     return -1

        # return rsi_output
        # return 0

    def place_order(self,price_data) -> list:
        self.ticks_held += 1

        # print(self.ticks_held,self.cool_down)

        if self.ticks_held <= self.cool_down:
            return []

        if random.random() >= 0.01:
        # if random.random() >= 0.001:
            return []

        out = self.make_decision(price_data)

        if out == 1:
            # buy
            # quantity = int(0.05 * ((price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume)/3))
            # quantity = max(quantity,200)
            # quantity = int(0.4 * (price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume) / 3)
            quantity = int(0.01 * (price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume) / 3)
            quantity = max(quantity, 350)
            # print(quantity)

            n = random.randint(5, 30)

            per_quantity = int(quantity / n)

            orders = []

            for i in range(n):
                # price = price_data[-1].Close * random.uniform(0.99, 1.01)
                price = self.get_price(price_data, level2_data=self.level2_data, buy_price=True)
                if price * per_quantity > self.balance:
                    break

                buy_order = self.place_buy_order(price, quantity)
                self.take_profit_orders.append(price * random.uniform(1, 1.3), per_quantity)

                orders.append(buy_order)

            self.ticks_held = 0

            return orders

        elif out == -1:
            # sell
            quantity = int(0.01 * ((price_data[-1].Volume + price_data[-2].Volume + price_data[-3].Volume)/3))
            quantity = max(quantity,200)
            quantity = min(quantity,self.holdings)

            # print(quantity)

            # print(price_data[-1].Volume)

            # print(quantity)

            n = random.randint(5,20)
            orders = []
            per_quantity = int(quantity/n)

            for i in range(n):
                # price = price_data[-1].Close * random.uniform(0.998,1)
                # price = price_data[-1].Close * random.uniform(0.99,1)
                price = self.get_price(price_data, level2_data=self.level2_data, buy_price=False)

                sell_order = self.place_sell_order(price,per_quantity)
                orders.append(sell_order)

            self.ticks_held = 0

            return orders

        return []



class LiquidityAbsorber2(Trader):
    # they buy opposite to what all do.If alot are selling they buy,absorb liquidity
    def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
        if balance == 0:
            # balance = 100000000
            balance = random.randint(data.LIQUIDITY_TRADERS_MIN_BALANCE,data.LIQUIDITY_TRADERS_MAX_BALANCE)

        super().__init__(balance,0,7,trader_id)
        self.level2_data = level2_data

        # self.current_tick = 0
        self.cooldown_tick  = random.randint(50,10000) # the min ticks after which next action is allowed
        self.max_holding_ticks = random.randint(1,1000) # after which have to sell
        self.ticks_held = self.cooldown_tick # for how much time latest order has been held

    def place_order(self,price_data) -> list:
        return []

# class BigInstitute(Trader):
#     def __init__(self,indicators : IndicatorEngine,level2_data : Level2Data,trader_id : int,balance : float = 0):
#         if balance == 0:


# class Level3Trader
# :
#     def __init__(self,indicators : IndicatorEngine,trader_id : int,balance : float = 0):
#         if balance == 0:
#
#         super().__init__(balance, 0, 3, trader_id)
