import bisect

class Level2Data:
    def __init__(self,n = 5):
        # shows top n bid price and least n sell price
        self.n = n
        self.buy_data = {} # will store n buy prices in increasing order. show in decreasing order
        self.sell_data = {} # will store n sell prices in increasing order

        self.buy_prices = [] # will store only keys of buy data in increasing order
        self.sell_prices = [] # will store keys of sell data in increasing order

        self.total_buy_volume = self.total_sell_volume = 0 # stores total volume of all orders indide level2data

    def pop_buy_data(self,price,volume):
        # we will pop when order gets matched
        # and we pop last element because order with highest bid gets matched
        price = round(price,2)
        if len(self.buy_prices) != 0 and self.buy_prices[-1] == price:
            self.buy_data[price] -= volume
            self.total_buy_volume -= volume
            self.total_buy_volume = max(self.total_buy_volume,0)
            if self.buy_data[price] <= 0:
                self.buy_prices.pop(-1)
                del self.buy_data[price]

    def pop_sell_data(self,price,volume):
        # we will pop when order gets matched
        # and we pop first element because order with lowest ask gets matched
        price = round(price,2)
        if len(self.sell_prices) != 0 and self.sell_prices[0] == price:
            self.sell_data[price] -= volume
            self.total_sell_volume -= volume
            self.total_sell_volume = max(self.total_sell_volume,0)

            if self.sell_data[price] <= 0:
                self.sell_prices.pop(0)
                del self.sell_data[price]

    def append_buy_price(self,price,volume):
        price = round(price,2)

        if len(self.buy_prices) == 0:
            self.buy_data[price] = volume
            self.total_buy_volume += volume
            bisect.insort(self.buy_prices,price)
            return

        elif price < self.buy_prices[0] and len(self.buy_prices) != self.n:
            # no need to put in level2 data
            return

        # if price in self.buy_prices:
        if self.buy_prices[0] <= price <= self.buy_prices[-1] and price in self.buy_data:
            self.buy_data[price] += volume
            self.total_buy_volume += volume
            return
        elif len(self.buy_prices) == self.n:
            least_price = self.buy_prices[0]
            self.total_buy_volume -= self.buy_data[least_price]
            del self.buy_data[least_price]
            self.buy_prices.pop(0)
        bisect.insort(self.buy_prices,price)
        self.buy_data[price] = volume
        self.total_buy_volume += volume

    def append_sell_price(self,price,volume):
        price = round(price,2)
        # if price in self.sell_prices:
        if len(self.sell_prices) == 0:
            self.sell_data[price] = volume
            self.total_sell_volume += volume
            bisect.insort(self.sell_prices,price)
            return
        elif price > self.sell_prices[-1] and len(self.sell_prices) != self.n:
            # no need to put in level2 data
            return

        if self.sell_prices[0] <= price <= self.sell_prices[-1] and price in self.sell_data:
            self.sell_data[price] += volume
            self.total_sell_volume += volume
            return
        if len(self.sell_prices) == self.n:
            highest_price = self.sell_prices[-1]
            self.total_sell_volume -= self.sell_data[highest_price]
            del self.sell_data[highest_price]
            self.sell_prices.pop(-1)
        bisect.insort(self.sell_prices,price)
        self.sell_data[price] = volume
        self.total_sell_volume += volume
