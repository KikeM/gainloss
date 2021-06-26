from .conventions import Direction


class Trade:
    def __init__(self, time, symbol, buying, price, quantity):
        self.time = time
        self.symbol = symbol
        self.buying = buying
        self.price = price
        self.quantity = quantity

    def __str__(self):

        s = str(vars(self))

        return s

    def __repr__(self) -> str:
        return self.__str__()


class ClosedTrade:
    def __init__(
        self, open_t, close_t, symbol, quantity, pnl, bought_first, open_p, close_p
    ):
        self.open_t = open_t
        self.close_t = close_t
        self.symbol = symbol
        self.quantity = quantity
        self.pnl = pnl
        self.bought_first = bought_first
        self.open_p = open_p
        self.close_p = close_p

    def __str__(self):
        s = "{},{},{},{},{:.2f},{},{},{:.2f},{:.2f}"
        s = s.format(
            self.open_t,
            self.close_t,
            self.symbol,
            self.quantity,
            self.pnl,
            Direction.BUY if self.bought_first else Direction.SELL,
            Direction.SELL if self.bought_first else Direction.BUY,
            self.open_p,
            self.close_p,
        )

        return s

    def __repr__(self) -> str:
        return self.__str__()
