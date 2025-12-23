# import numpy as np
#
# class IndicatorEngine:
#     def __init__(self):
#         self.close = []
#         self.high = []
#         self.low = []
#         self.vol = []
#
#         self.ema_values = {} # stores different ema's
#         self.ema_multiplier = {}
#
#         # RSI
#         self.prev_close = None
#         self.avg_gain = 0
#         self.avg_loss = 0
#         self.rsi_value = None
#
#         # MACD
#         self.fast_ema = None
#         self.slow_ema = None
#         self.signal_ema = None
#         self.macd = None
#         self.signal = None
#         self.hist = None
#
#         # Bollinger bands
#         self.bb_mid = None
#         self.bb_upper = None
#         self.bb_lower = None
#
#         # VWAP
#         self.vwap_pv = 0
#         self.vwap_vol = 0
#         self.vwap = None
#
#     def update(self, candle):
#         c = candle.Close
#         h = candle.High
#         l = candle.Low
#         v = candle.Volume
#
#         self.close.append(c)
#         self.high.append(h)
#         self.low.append(l)
#         self.vol.append(v)
#
#         # Update indicators
#         self._update_registered_emas(c)
#         self._update_rsi(c)
#         self._update_macd(c)
#         self._update_bollinger(20)
#         self._update_vwap(h, l, c, v)
#
#     def sma(self, length: int):
#         if len(self.close) < length:
#             return None
#         return sum(self.close[-length:]) / length
#
#     def add_ema(self, length: int):
#         # will store different ema's
#         if length not in self.ema_multiplier:
#             self.ema_multiplier[length] = 2 / (length + 1)
#         self.ema_values[length] = []
#
#     def _update_registered_emas(self, close):
#         for length in self.ema_values:
#             k = self.ema_multiplier[length]
#             arr = self.ema_values[length]
#
#             if not arr:
#                 arr.append(close)
#             else:
#                 prev = arr[-1]
#                 arr.append(prev + k * (close - prev))
#
#     def ema(self, length):
#         arr = self.ema_values.get(length, None)
#         return arr[-1] if arr else None
#
#     def _update_rsi(self, close, period=14):
#         if self.prev_close is None:
#             self.prev_close = close
#             return
#
#         change = close - self.prev_close
#         gain = max(change, 0)
#         loss = max(-change, 0)
#
#         if self.avg_gain == 0 and self.avg_loss == 0:
#             self.avg_gain = gain
#             self.avg_loss = loss
#         else:
#             self.avg_gain = (self.avg_gain * (period - 1) + gain) / period
#             self.avg_loss = (self.avg_loss * (period - 1) + loss) / period
#
#         if self.avg_loss == 0:
#             self.rsi_value = 100
#         else:
#             rs = self.avg_gain / self.avg_loss
#             self.rsi_value = 100 - (100 / (1 + rs))
#
#         self.prev_close = close
#
#     def rsi(self):
#         return self.rsi_value
#
#     def _update_macd(self, close):
#         fast = 12
#         slow = 26
#         signal = 9
#
#         kf = 2 / (fast + 1)
#         ks = 2 / (slow + 1)
#         ks2 = 2 / (signal + 1)
#
#         # fast EMA -> small period
#         if self.fast_ema is None:
#             self.fast_ema = close
#         else:
#             self.fast_ema = self.fast_ema + kf * (close - self.fast_ema)
#
#         # slow EMA -> long period
#         if self.slow_ema is None:
#             self.slow_ema = close
#         else:
#             self.slow_ema = self.slow_ema + ks * (close - self.slow_ema)
#
#         self.macd = self.fast_ema - self.slow_ema
#
#         # signal line
#         if self.signal_ema is None:
#             self.signal_ema = self.macd
#         else:
#             self.signal_ema = self.signal_ema + ks2 * (self.macd - self.signal_ema)
#
#         self.signal = self.signal_ema
#         self.hist = self.macd - self.signal
#
#     def _update_bollinger(self, length):
#         if len(self.close) < length:
#             return
#
#         window = self.close[-length:]
#         mid = sum(window) / length
#         std = np.std(window)
#
#         self.bb_mid = mid
#         self.bb_upper = mid + 2 * std
#         self.bb_lower = mid - 2 * std
#
#     def _update_vwap(self, high, low, close, vol):
#         tp = (high + low + close) / 3
#         self.vwap_pv += tp * vol
#         self.vwap_vol += vol
#
#         self.vwap = self.vwap_pv / self.vwap_vol if self.vwap_vol else close
#
#     def macd_data(self):
#         return self.macd, self.signal, self.hist
#
#     def bollinger(self):
#         return self.bb_upper, self.bb_mid, self.bb_lower
#
#     def vwap_value(self):
#         return self.vwap













import numpy as np

class IndicatorEngine:
    def __init__(self):
        self.close = []
        self.high = []
        self.low = []
        self.vol = []

        self.ema_values = {} # stores different ema's
        self.ema_multiplier = {}

        # RSI
        self.prev_close = None
        self.avg_gain = 0
        self.avg_loss = 0
        self.rsi_value = None

        # Bollinger bands
        self.bb_mid = None
        self.bb_upper = None
        self.bb_lower = None

        # VWAP
        self.vwap_pv = 0
        self.vwap_vol = 0
        self.vwap = None

    def update(self, candle):
        c = candle.Close
        h = candle.High
        l = candle.Low
        v = candle.Volume

        self.close.append(c)
        self.high.append(h)
        self.low.append(l)
        self.vol.append(v)

        # Update indicators
        self._update_registered_emas(c)
        self._update_rsi(c)
        self._update_bollinger(20)
        self._update_vwap(h, l, c, v)

    def sma(self, length: int):
        if len(self.close) < length:
            return None
        return sum(self.close[-length:]) / length

    def add_ema(self, length: int):
        # will store different ema's
        if length not in self.ema_multiplier:
            self.ema_multiplier[length] = 2 / (length + 1)
        self.ema_values[length] = []

    def _update_registered_emas(self, close):
        for length in self.ema_values:
            k = self.ema_multiplier[length]
            arr = self.ema_values[length]

            if not arr:
                arr.append(close)
            else:
                prev = arr[-1]
                arr.append(prev + k * (close - prev))

    def ema(self, length):
        arr = self.ema_values.get(length, None)
        return arr[-1] if arr else None

    def _update_rsi(self, close, period=14):
        if self.prev_close is None:
            self.prev_close = close
            return

        change = close - self.prev_close
        gain = max(change, 0)
        loss = max(-change, 0)

        if self.avg_gain == 0 and self.avg_loss == 0:
            self.avg_gain = gain
            self.avg_loss = loss
        else:
            self.avg_gain = (self.avg_gain * (period - 1) + gain) / period
            self.avg_loss = (self.avg_loss * (period - 1) + loss) / period

        if self.avg_loss == 0:
            self.rsi_value = 100
        else:
            rs = self.avg_gain / self.avg_loss
            self.rsi_value = 100 - (100 / (1 + rs))

        self.prev_close = close

    def rsi(self):
        return self.rsi_value

    def _update_bollinger(self, length):
        if len(self.close) < length:
            return

        window = self.close[-length:]
        mid = sum(window) / length
        std = np.std(window)

        self.bb_mid = mid
        self.bb_upper = mid + 2 * std
        self.bb_lower = mid - 2 * std

    def _update_vwap(self, high, low, close, vol):
        tp = (high + low + close) / 3
        self.vwap_pv += tp * vol
        self.vwap_vol += vol

        self.vwap = self.vwap_pv / self.vwap_vol if self.vwap_vol else close

    def bollinger(self):
        return self.bb_upper, self.bb_mid, self.bb_lower

    def vwap_value(self):
        return self.vwap
