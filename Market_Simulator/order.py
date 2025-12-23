class Order:
    def __init__(self,order_id : int,trader_id : int,price : float,quantity : int,trade_type : int,timestamp : int):
        # order id : each order has some unique no
        # trader id : the id of the trader who placed this order
        # price : the price at which this order is placed
        # quantity : the no of units
        # trade_type : buying or selling order -> 0 for buy , 1 -> sell
        # timestamp : in sec from start of market when order was placed
        # status : tells about order status , 0 = open,1 = completed,2 = canceled
        self.order_id = order_id
        self.trader_id = trader_id
        self.price = price
        # self.price = round(price,2)
        self.quantity = quantity
        self.trade_type = trade_type
        self.timestamp = timestamp
        self.status = 0

    def cancel_order(self):
        # if order canceled by trader
        self.status = 2
        pass

    def order_filled(self):
        # order has been filled/matched
        self.status = 1
        pass

    def print_details(self):
        print()
        print(" ==== Order ", self.order_id , " details ====")
        print("Trader Id : ", self.trader_id)
        print("Quantity : ", self.quantity , " Price Ask/Bid : ", self.price)
        print("Total Order Value : ", self.price * self.quantity)
        print("Order Type : ", ["Buy","Sell"][self.trade_type])
        print("Timestamp : ", self.timestamp)

