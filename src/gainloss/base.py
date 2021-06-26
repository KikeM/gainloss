import pandas as pd
from .conventions import Direction


class Trade:
    def __init__(self, time, symbol, buying, price, quantity, fees=None):
        self.time = time
        self.symbol = symbol
        self.buying = buying
        self.price = price
        self.quantity = quantity
        self.fees = abs(fees) if fees else 0.0

    def __str__(self):

        s = str(vars(self))

        return s

    def __repr__(self) -> str:
        return self.__str__()


class ClosedTrade:
    def __init__(
        self,
        open_time,
        close_time,
        symbol,
        quantity,
        pnl,
        bought_first,
        open_price,
        close_price,
        open_fees,
        close_fees,
    ):
        self.open_t = open_time
        self.close_t = close_time
        self.symbol = symbol
        self.quantity = quantity
        self.pnl = pnl
        self.bought_first = bought_first
        self.open_p = open_price
        self.close_p = close_price
        self.open_fees = open_fees
        self.close_fees = close_fees

    @property
    def adquisition(self):
        _adquisition = self.open_p * self.quantity + self.open_fees
        return _adquisition

    @property
    def transmition(self):
        _transmition = self.close_p * self.quantity - self.close_fees
        return _transmition

    @property
    def pnl_fees(self):

        adquisition = self.adquisition
        transmition = self.transmition
        _pnl_fees = transmition - adquisition

        return _pnl_fees

    def __str__(self):
        s = "{},{},{},{},{:.2f},{:.2f},{:.2f},{:.2f},{},{},{:.2f},{:.2f},{:.2f},{:.2f}"
        s = s.format(
            pd.to_datetime(self.open_t).strftime("%Y-%m-%d"),
            pd.to_datetime(self.close_t).strftime("%Y-%m-%d"),
            self.symbol,
            self.quantity,
            self.pnl,
            self.pnl_fees,
            self.adquisition,
            self.transmition,
            Direction.BUY if self.bought_first else Direction.SELL,
            Direction.SELL if self.bought_first else Direction.BUY,
            self.open_p,
            self.close_p,
            self.open_fees,
            self.close_fees,
        )

        return s

    def __repr__(self) -> str:
        return self.__str__()
