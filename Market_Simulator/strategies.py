class Strategies:
    @classmethod
    def single_ema(cls, ema, price) -> int:
        # buy if price above give ema
        if price > ema[-1]:
            return 1
        elif price < ema[-1]:
            return -1
        return 0

    # @classmethod
    # def ema_crossover(cls, slow_ema, fast_ema, price) -> int:
        # buy when two ema cross
        # slow ema = longer time period
        # fast ema = shorter time period
        # if price > fast_ema[-1] > slow_ema[-1]:
        # if price > fast_ema > slow_ema:
        #         return 1
        # elif price < fast_ema[-1] < slow_ema[-1]:
        # elif price < fast_ema < slow_ema:
        #
        #     return -1
        # return 0

    # @classmethod
    # def triple_ema_crossover(cls, trend_ema, slow_ema, fast_ema, price) -> int:
        # trend_ema = ema with very long time period around 50,100,200
        # buy when both ema cross and above trend_ema and price above all ema
        # if price > fast_ema[-1] > slow_ema[-1] > trend_ema[-1]:
        #     return 1
        # elif price < fast_ema[-1] < slow_ema[-1] < trend_ema[-1]:
        #     return -1
        # return 0

    # @classmethod
    # def macd_strategy(cls, macd, signal, macd_prev=None, signal_prev=None) -> int:
    #     if macd is None or signal is None:
    #         return 0
    #
    #     if macd_prev is None or signal_prev is None:
    #         return 1 if macd > signal else -1 if macd < signal else 0
    #
    #     if (macd_prev <= signal_prev) and (macd > signal):
    #         return 1
    #     elif (macd_prev >= signal_prev) and (macd < signal):
    #         return -1
    #     return 0

    @classmethod
    def rsi_strategy(cls, rsi_val: float, lower=30, upper=70) -> int:
        # buy when rsi <= 30 and sell when rsi >= 70
        if rsi_val is None:
            return 0
        if rsi_val < lower:
            return 1
        elif rsi_val > upper:
            return -1
        return 0

    @classmethod
    def bollinger_strategy(cls, price, bb_upper, bb_lower) -> int:
        # if price above bb_upper then price tends to go down and reverse for bb_lower
        # print(bb_lower,bb_upper,price)
        if bb_upper is None or bb_lower is None:
            return 0
        if price <= bb_lower:
            return 1
        elif price >= bb_upper:
            return -1
        return 0

    @classmethod
    def vwap_strategy(cls, price, vwap_val) -> int:
        # price is above the price at which most people bought
        if vwap_val is None:
            return 0
        if price > vwap_val:
            return 1
        elif price < vwap_val:
            return -1
        return 0
