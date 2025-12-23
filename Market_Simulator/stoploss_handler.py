# if you buy 50 shares with stoploss s1 at day 1 and 100 shares with stoploss s2 at day 2,and at day3 you sell 50 shares
# since 150 > 100 therefore a stoploss order must be canceled
# and the order which was placed recently gets canceled

import bisect


class StopLoss:
    def __init__(self):
        self.total_stoploss_orders = 0
        self.stoploss_orders = [] # stores in increasing stoploss
        self.index = 0 # index is used to remove recently added order

    def append(self,stoploss,quantity):
        if quantity <= 0:
            return

        bisect.insort(self.stoploss_orders,[stoploss,quantity,self.index])
        self.index += 1
        self.total_stoploss_orders += quantity

    def pop(self):
        # will pop order with highest stoploss
        if len(self.stoploss_orders) != 0:
            self.total_stoploss_orders -= self.stoploss_orders[-1][1]
            return self.stoploss_orders.pop(-1)

        return -1

    def pop_recent(self,holdings):
        # pops all stoploss order till holding > stoploss order
        # pops the order which was placed recently
        # if len(self.stoploss_orders) == 0:
        #     return
        while self.total_stoploss_orders > holdings and len(self.stoploss_orders):
            index = 0
            for i in range(len(self.stoploss_orders)):
                if self.stoploss_orders[i][2] > self.stoploss_orders[index][2]:
                    index = i

            self.total_stoploss_orders -= self.stoploss_orders[index][1]
            # self.stoploss_orders.remove(self.stoploss_orders[index])
            self.stoploss_orders.pop(index)



class TakeProfit:
    def __init__(self):
        self.total_take_profit_orders = 0
        self.take_profit_orders = [] # stores in increasing stoploss
        self.index = 0 # index is used to remove recently added order

    def append(self,take_profit,quantity):
        # increasing take profit
        if quantity <= 0:
            return
        bisect.insort(self.take_profit_orders,[take_profit,quantity,self.index])
        self.index += 1
        self.total_take_profit_orders += quantity

    def pop(self):
        # will pop order with lowest take_profit
        if len(self.take_profit_orders) != 0:
            self.total_take_profit_orders -= self.take_profit_orders[-1][1]
            return self.take_profit_orders.pop(0)

        return -1

    def pop_recent(self,holdings):
        # pops all stoploss order till holding > stoploss order
        # pops the order which was placed recently
        # if len(self.stoploss_orders) == 0:
        #     return
        while self.total_take_profit_orders > holdings and len(self.take_profit_orders):
            index = 0
            for i in range(len(self.take_profit_orders)):
                if self.take_profit_orders[i][2] < self.take_profit_orders[index][2]:
                    index = i

            self.total_take_profit_orders -= self.take_profit_orders[index][1]
            # self.stoploss_orders.remove(self.stoploss_orders[index])
            self.take_profit_orders.pop(index)


# class Stoploss_TakeProfit_Handler:
#     handles stoploss and takeprofit
    # def __init__(self):
    #     self.stoploss_orders = StopLoss()
    #     self.take_profit_orders = TakeProfit()
    #     self.index = 0
    #
    # def append(self,take_profit,stoploss = -1):
        
