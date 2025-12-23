# will distribute initial shares to traders
import random

import data
from order import Order


class Distributor:
    def __init__(self,traders,total_shares : int):
        self.traders = traders
        self.total_shares = total_shares

    def distribute(self):
        # will distribute shares between 0 to 1% among traders
        total = self.total_shares
        for trader in self.traders:
            if trader.trader_type == 8:
                # company
                price = random.uniform(data.STARTING_PRICE * 0.95, data.STARTING_PRICE * 0.99)
                shares = data.COMPANY_HOLDINGS
                order = Order(data.ORDER_ID, trader.trader_id, price, shares, 0, 0)
                trader.add_holding(price, shares, order)

            elif trader.trader_type == 9:
                # whales
                price = random.uniform(data.STARTING_PRICE * 0.95, data.STARTING_PRICE * 0.99)
                shares = random.randint(data.WHALES_HOLDINGS_MIN,data.WHALES_HOLDINGS_MAX)
                order = Order(data.ORDER_ID, trader.trader_id, price, shares, 0, 0)
                trader.add_holding(price, shares, order)

            elif trader.trader_type == 4:
                # agressive
                price = random.uniform(data.STARTING_PRICE * 0.95, data.STARTING_PRICE * 1.05)
                shares = random.randint(100,1000)
                order = Order(data.ORDER_ID, trader.trader_id, price, shares, 0, 0)
                trader.add_holding(price, shares, order)

            elif trader.trader_type == 6:
                # bears
                price = random.uniform(data.STARTING_PRICE * 0.95, data.STARTING_PRICE * 1.05)
                # shares = random.randint(1000,10000)
                shares = random.randint(5000,10000)
                order = Order(data.ORDER_ID, trader.trader_id, price, shares, 0, 0)
                trader.add_holding(price, shares, order)

            elif trader.trader_type >= 3 and trader.trader_type < 5:
                # give more to them
                # percentage = random.uniform(0, 0.005)
                percentage = random.uniform(0.002, 0.005)
                # shares = min(int(total * percentage), self.total_shares)
                shares = random.randint(1,100)
                if shares > 0:
                    # traders get stock like ipo at different prices with range += 5%
                    price = random.uniform(data.STARTING_PRICE * 0.90, data.STARTING_PRICE * 1.10)
                    self.total_shares -= shares
                    order = Order(data.ORDER_ID, trader.trader_id, price, shares, 0, 0)
                    trader.add_holding(price, shares, order)
            # if random.random() < 0.2:
            elif random.random() < 0.03:
                percentage = random.uniform(0, 0.001)
                shares = min(int(total * percentage),self.total_shares)
                if shares > 0:
                    # traders get stock like ipo at different prices with range += 5%
                    price = random.uniform(data.STARTING_PRICE * 0.95,data.STARTING_PRICE * 1.05)
                    self.total_shares -= shares
                    order = Order(data.ORDER_ID,trader.trader_id,price,shares,0,0)
                    trader.add_holding(price,shares,order)
                    if random.random() < 0.05:
                        percentage = random.uniform(1.01,2.999)
                        trader.take_profit_orders.append(price * percentage,shares)

        # print(total - self.total_shares)