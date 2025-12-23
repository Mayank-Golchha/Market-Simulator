class Candle:
    def __init__(self,Open,Close,High,Low,Volume = 0):
        self.Open = Open
        self.Close = Close
        self.High = High
        self.Low = Low
        self.Volume = Volume

    def isGreen(self):
        # 1 = green candle
        # 0 = red candle
        return self.Close > self.Open
