from collections import defaultdict, deque

import pandas as pd

import gainloss.settings as st

from .base import ClosedTrade, Trade
from .conventions import Direction, TradeNames

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
        self.trades = None
        self.pnl = 0.0

    def process_trade(self, trade):
        """FIFO trade processing.

        Parameters
        ----------
        trade : gainloss.Trade
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

            pnl = quant_traded * round(trade.price - open_trades[0].price, st.ROUNDING)

            # Invert if we shorted
            if trade.buying:
                pnl *= -1

            pnl = round(pnl, st.ROUNDING)
            self.pnl += pnl

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
            file_name,
            delimiter=st.DELIMITER,
            index_col=TradeNames.TIME,
            parse_dates=True,
            dayfirst=True,
        )

        trades = trades.sort_index(ascending=True)

        self.trades = trades.copy()

        # Loop through each trade
        for time, tr in trades.iterrows():
            buying = tr[TradeNames.SIDE] == Direction.BUY
            trade = Trade(
                time,
                tr[TradeNames.SYMBOL],
                buying,
                float(tr[TradeNames.PRICE]),
                int(tr[TradeNames.QUANTITY]),
            )

            self.process_trade(trade)

    def print_closed_trades(self):
        for ct in self.closed_trades:
            print(ct)
