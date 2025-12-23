# to be used by trader to maintain all active positions

class Position:
    def __init__(self,price,quantity,take_profit = 0,stop_loss = 0):
        self.price = price # buying price
        self.quantity = quantity
        self.take_profit = take_profit # 0 if no take_profit
        self.stop_loss = stop_loss # 0 if no stop_loss

