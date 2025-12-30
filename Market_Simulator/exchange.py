
import heapq
import random
import bisect
from collections import deque

from order import Order
from trader_engine import TraderEngine
from level2data import Level2Data
from distributor import Distributor
import data


class Transaction:
    def __init__(self,buyer_id,seller_id,price,quantity):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.price = price
        self.quantity = quantity
        self.time = data.TIME

    def print_transaction(self):
        print("==== Transaction ====")
        print("Buyer id : " , self.buyer_id , " Seller Id : ",self.seller_id)
        print("Price : ", self.price ," Quantity : ",self.quantity)
        print("Time of Transactions : " , self.time)


class Exchange:
    def __init__(self,starting_price):
        # starting price = starting price of stock
        self.starting_price = starting_price
        self.traders = [] # list of all traders. ith trader has id "i"
        self.buy_orders = []
        self.sell_orders = []
        self.price = self.starting_price
        self.volume = 0
        # self.completed_order = [] # list of all completed orders
        self.completed_order = deque(maxlen=1000)

        self.level_2_data = Level2Data(data.WINDOW_LEVEL2_MAX_ROWS)

        # self.rebate = 0 # rebate is given by exchange to big market makers

    def initialize_traders(self,indicators,level_2_data):
        TraderEngine.initialize_random_traders(self.traders,level_2_data) # random traders
        TraderEngine.initialize_level1_traders(self.traders,level_2_data) # level1 traders
        TraderEngine.initialize_level2_traders(self.traders,indicators,level_2_data) # level1 traders
        TraderEngine.initialize_level3_traders(self.traders,indicators,level_2_data) # level1 traders

        Distributor(self.traders,data.TOTAL_SHARES).distribute() # initial public distribution of shares

        print(data.TRADER_ID , " Traders added !!")

    def get_price(self):
        return self.price

    def get_price_volume(self):
        return self.price,self.volume

    def add_buy_order(self,order : Order):
        # appends in unfilled orders
        # max heap
        # max buy order is filled first
        # if price is same than whoever places the order first gets priority
        if not order:
            return
        if order.status == 0:
            # order is open to be completed
            # heapq.heappush(self.buy_orders,(-order.price,order.timestamp,-order.quantity,order.order_id,order))
            heapq.heappush(self.buy_orders,(-order.price,order.timestamp,order.order_id,order))
            self.level_2_data.append_buy_price(order.price,order.quantity)

    def add_sell_order(self,order : Order):
        # appends in unfilled orders
        # min heap
        # min sell order is filled first
        # if price is same than whoever places the order first gets priority
        if not order:
            return
        if order.status == 0:
            # heapq.heappush(self.sell_orders,(order.price,order.timestamp,-order.quantity,order.order_id,order))
            heapq.heappush(self.sell_orders,(order.price,order.timestamp,order.order_id,order))
            self.level_2_data.append_sell_price(order.price,order.quantity)


    def match_order(self,order : Order):
        # matches order with best order if not matched then puts in the order book
        if order.trade_type == 0:
            # buy order will be matched with best ask order i.e lowest sell order
            if len(self.sell_orders) == 0:
                self.add_buy_order(order)
                return

            buyer = self.traders[order.trader_id]


            # if self.sell_orders[0][4].price <= order.price:
            #     # the matching order available
            #     # new price == resting price i.e the new price becomes equal to the order price lying in the book
            #     self.price = self.sell_orders[0][4].price
            #
            #     if self.sell_orders[0][4].quantity <= order.quantity:
            #         # new order requires more quantity
            #         self.completed_order.append(Transaction(order.trader_id, self.sell_orders[0][4].trader_id, self.price, self.sell_orders[0][4].quantity))
            #         order.quantity -= self.sell_orders[0][4].quantity
            #         heapq.heappop(self.sell_orders)
            #
            #         # if order.quantity > 0:
            #             # remaining order will be matched with next best ask
            #             # self.match_order(order)
            #
            #
            #         return
            while order.quantity > 0 and self.sell_orders:

                if self.sell_orders[0][3].price <= order.price:
                    # the matching order available
                    # new price == resting price i.e the new price becomes equal to the order price lying in the book
                    # self.price = self.sell_orders[0][4].price
                    self.price = self.sell_orders[0][3].price
                    # seller = self.traders[self.sell_orders[0][4].trader_id]
                    seller = self.traders[self.sell_orders[0][3].trader_id]

                    if self.sell_orders[0][3].quantity <= order.quantity:
                        # new order requires more quantity
                        # buyer.add_holding(self.price,self.sell_orders[0][4].quantity)
                        buyer.add_holding(self.price,self.sell_orders[0][3].quantity)
                        # seller.add_balance(self.price,self.sell_orders[0][4].quantity)
                        seller.add_balance(self.price,self.sell_orders[0][3].quantity)
                        # self.level_2_data.pop_sell_data(self.price, self.sell_orders[0][4].quantity) # as sell order is lying in the order book
                        self.level_2_data.pop_sell_data(self.price, self.sell_orders[0][3].quantity) # as sell order is lying in the order book
                        self.completed_order.append(
                            Transaction(order.trader_id, self.sell_orders[0][3].trader_id, self.price,
                                        self.sell_orders[0][3].quantity))
                        order.quantity -= self.sell_orders[0][3].quantity
                        self.volume += self.sell_orders[0][3].quantity
                        self.sell_orders[0][3].quantity = 0
                        heapq.heappop(self.sell_orders)


                        # if order.quantity > 0:
                        # remaining order will be matched with next best ask
                        # self.match_order(order)

                    else:
                        # buy quantity = sell quantity
                        buyer.add_holding(self.price,order.quantity)
                        seller.add_balance(self.price,order.quantity)
                        self.level_2_data.pop_sell_data(self.price, order.quantity) # as sell order is lying in the order book
                        self.sell_orders[0][3].quantity -= order.quantity # -> this line dangerous as in heap quantity was also there but quantity not changing
                        self.volume += order.quantity
                        self.completed_order.append(Transaction(order.trader_id, self.sell_orders[0][3].trader_id, self.price, order.quantity))
                        return
                else:
                    # order not matched so placed in order book
                    self.add_buy_order(order)
                    return
        else:
            # sell order will be matched with best bid order i.e highest bidder
            if len(self.buy_orders) == 0:
                self.add_sell_order(order)
                return

            seller = self.traders[order.trader_id]
            # seller = self.traders[self.sell_orders[0][4].trader_id]

            while order.quantity > 0 and self.buy_orders:

                buyer = self.traders[self.buy_orders[0][3].trader_id]

                if self.buy_orders[0][3].price >= order.price:
                    # the matching order available
                    # new price == resting price i.e the new price becomes equal to the order price lying in the book
                    self.price = self.buy_orders[0][3].price

                    if self.buy_orders[0][3].quantity <= order.quantity:
                        # new order requires more quantity
                        buyer.add_holding(self.price, self.buy_orders[0][3].quantity)
                        seller.add_balance(self.price, self.buy_orders[0][3].quantity)

                        self.completed_order.append(Transaction(self.buy_orders[0][3].trader_id, order.trader_id, self.price, self.buy_orders[0][3].quantity))

                        self.level_2_data.pop_buy_data(self.price, self.buy_orders[0][3].quantity) # as sell order is lying in the order book

                        order.quantity -= self.buy_orders[0][3].quantity
                        self.buy_orders[0][3].quantity = 0
                        heapq.heappop(self.buy_orders)
                        # if order.quantity > 0:
                            # remaining order will be matched with next best bid
                            # self.match_order(order)
                        # return
                    else:
                        buyer.add_holding(self.price, self.buy_orders[0][3].quantity)
                        seller.add_balance(self.price, self.buy_orders[0][3].quantity)
                        self.completed_order.append(Transaction(self.buy_orders[0][3].trader_id, order.trader_id, self.price, order.quantity))
                        self.buy_orders[0][3].quantity -= order.quantity # -> this line is dangerous as heap also contains quantity and it must be updates as well
                        self.level_2_data.pop_buy_data(self.price, order.quantity) # as sell order is lying in the order book
                        # self.buy_orders[0][3] = self.buy_orders[0][4].quantity
                        return
                else:
                    # order not matched so placed in order book
                    self.add_sell_order(order)
                    return


    # def match_order(self):
    #     # if buyer wants to buy at 102 and seller wants to sell at 99
    #     # then price will become equal to the order whichever came first in the order book
    #
    #     # will match buying orders with selling orders
    #     # if person A wants to sell at 102 and person B wants to buy at 103 then
    #     # person A will get 103 and his order will be filled
    #     if len(self.sell_orders) == 0 or len(self.buy_orders) == 0:
    #         # order cannot be matched
    #         return
    #
    #     if self.sell_orders[0][4].status == 2 or self.buy_orders[0][4].status == 2:
    #         # order has been canceled
    #         print()
    #         print("======= ORDER CANCELED ======")
    #         if self.buy_orders[0].status == 2:
    #             print(self.buy_orders[0].print_details())
    #             heapq.heappop(self.buy_orders)
    #         else:
    #             print(self.sell_orders[0].print_details())
    #             heapq.heappop(self.sell_orders)
    #
    #
    #     if self.sell_orders[0][4].price <= self.buy_orders[0][4].price:
    #         # comment
    #         # price = self.sell_orders[0][4].price
    #         price = self.sell_orders[0][4].price
    #
    #         if self.buy_orders[0][4].timestamp < self.sell_orders[0][4].timestamp:
    #             # if buy order came first price will become equal to it
    #             price = self.buy_orders[0][4].price
    #
    #         buy_quantity = self.buy_orders[0][4].quantity
    #         sell_quantity = self.sell_orders[0][4].quantity
    #         buyer = self.traders[self.buy_orders[0][4].trader_id]
    #         seller = self.traders[self.sell_orders[0][4].trader_id]
    #
    #         # price of share will change
    #         self.price = price
    #
    #         if buy_quantity <= sell_quantity:
    #             if buy_quantity == 0:
    #                 return
    #             self.volume = buy_quantity
    #             # buyer.add_holding(price,buy_quantity)
    #             buyer.add_holding(price,buy_quantity,self.buy_orders[0][4])
    #
    #             # seller.add_balance(price,buy_quantity)
    #             seller.add_balance(price,buy_quantity,self.sell_orders[0][4])
    #             if sell_quantity > buy_quantity:
    #                 # selling quantity is more than buying quantity
    #                 # order of sell_quantity is not completed
    #                 # partially filled
    #                 self.sell_orders[0][4].quantity -= buy_quantity # partially filled
    #                 # print("####### ORDER MATCHED #########")
    #                 # print("Price : " ,self.price)
    #                 # self.completed_order.append(Transaction(buyer.trader_id,seller.trader_id,price,buy_quantity))
    #
    #                 # self.sell_orders[0].balance -= buy_quantity * price
    #             else:
    #                 heapq.heappop(self.sell_orders)
    #             heapq.heappop(self.buy_orders)
    #             self.completed_order.append(Transaction(buyer.trader_id, seller.trader_id, price, buy_quantity))
    #         else:
    #             if sell_quantity == 0:
    #                 return
    #
    #             # sell_quantity < buy_quantity
    #             self.volume = sell_quantity
    #
    #             buyer.add_holding(price,sell_quantity)
    #             seller.add_balance(price,sell_quantity)
    #             self.buy_orders[0][4].quantity -= sell_quantity # partially filled
    #             # heapq.heappop(self.buy_orders)
    #             heapq.heappop(self.sell_orders)
    #             # self.buy_orders[0][2].quantity -= sell_quantity # partially filled
    #
    #             self.completed_order.append(Transaction(buyer.trader_id, seller.trader_id, price, sell_quantity))

                # print("####### ORDER MATCHED #########")
                # print("Price : ", self.price)

        # order not placed


