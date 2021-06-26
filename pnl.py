import csv
import sys
from collections import defaultdict, deque

import pandas as pd
from tabulate import tabulate

# ASSUMPTIONS MADE
# only one trade for a particular symbol at one time tick
# csv always sorted by time (instructions kind of say this, unclear)
#   necessary or else my usage of deque is not right
# can't trade for fractions of cent
# csv always right: price: 2 degree of precision float, quantity: int


class TradeManager:
    def __init__(self):

        self.open_trades = defaultdict(deque)
        self.closed_trades = []
        self._pnl = 0.0

    def process_trade(self, trade):
        """FIFO trade processing.

        Parameters
        ----------
        trade : [type]
            [description]
        """
        open_trades = self.open_trades[trade.symbol]

        # If no inventory, just add it
        if len(open_trades) == 0:
            open_trades.append(trade)
            return

        # If inventory exists, all trades must be same way (buy or sell)
        # If new trade is same way, again just add it
        if open_trades[0].buying == trade.buying:
            open_trades.append(trade)
            return

        # Otherwise, consume the trades
        while len(open_trades) > 0 and trade.quantity > 0:

            quant_traded = min(trade.quantity, open_trades[0].quantity)

            pnl = quant_traded * round(trade.price - open_trades[0].price, 2)

            # Invert if we shorted
            if trade.buying:
                pnl *= -1

            pnl = round(pnl, 2)
            self._pnl += pnl

            # Create closed trade
            ct = ClosedTrade(
                open_trades[0].time,
                trade.time,
                trade.symbol,
                quant_traded,
                pnl,
                open_trades[0].buying,
                open_trades[0].price,
                trade.price,
            )

            self.closed_trades.append(ct)

            # Remove closed shares from the trade
            trade.quantity -= quant_traded
            open_trades[0].quantity -= quant_traded

            if open_trades[0].quantity == 0:
                open_trades.popleft()

        # if the new trade still has quantity left over
        # then add it
        if trade.quantity > 0:
            open_trades.append(trade)

    def process_csv(self, file_name):
        """Process CSV file with trades.

        Parameters
        ----------
        file_name : string
        """
        trades = pd.read_csv(
            file_name, delimiter=",", index_col="TIME", parse_dates=True, dayfirst=True
        )

        trades = trades.sort_index(ascending=True)

        # Loop through each trade
        for time, tr in trades.iterrows():
            buying = tr["SIDE"] == "B"
            trade = Trade(
                time,
                tr["SYMBOL"],
                buying,
                float(tr["PRICE"]),
                int(tr["QUANTITY"]),
            )

            self.process_trade(trade)

    def print_closed_trades(self):
        for ct in self.closed_trades:
            print(ct)

    def get_pnl(self):
        return self._pnl

    def get_copy_of_closed_trades(self):
        """returns shallow copy of closed trades"""
        return self.closed_trades[:]


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
            "B" if self.bought_first else "S",
            "S" if self.bought_first else "B",
            self.open_p,
            self.close_p,
        )

        return s

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":

    tm = TradeManager()

    HEADER_CLOSED = "OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE".split(
        ","
    )

    tm.process_csv("pnl_transactions_etfs.csv")

    closed = [str(trade).split(",") for trade in tm.closed_trades]

    print(tabulate(closed, headers=HEADER_CLOSED))

    print("\nPnL = {:.2f}".format(tm.get_pnl()))
