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

        fifo_trade = open_trades[0]
        # If inventory exists, all trades must be same way (buy or sell)
        # If new trade is same way, again just add it
        if fifo_trade.buying == trade.buying:
            open_trades.append(trade)
            return

        # Otherwise, consume the trades
        while len(open_trades) > 0 and trade.quantity > 0:

            quant_traded = min(trade.quantity, fifo_trade.quantity)

            pnl = quant_traded * round(trade.price - fifo_trade.price, st.ROUNDING)

            # Invert if we shorted
            if trade.buying:
                pnl *= -1

            pnl = round(pnl, st.ROUNDING)
            self.pnl += pnl

            # Create closed trade
            ct = ClosedTrade(
                open_time=fifo_trade.time,
                close_time=trade.time,
                symbol=trade.symbol,
                quantity=quant_traded,
                pnl=pnl,
                bought_first=fifo_trade.buying,
                open_price=fifo_trade.price,
                close_price=trade.price,
                open_fees=fifo_trade.fees,
                close_fees=trade.fees,
            )

            self.closed_trades.append(ct)

            # Remove closed shares from the trade
            trade.quantity -= quant_traded
            fifo_trade.quantity -= quant_traded

            if fifo_trade.quantity == 0:
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
                time=time,
                symbol=tr[TradeNames.SYMBOL],
                buying=buying,
                price=float(tr[TradeNames.PRICE]),
                quantity=int(tr[TradeNames.QUANTITY]),
                fees=float(tr[TradeNames.FEES]),
            )

            self.process_trade(trade)

    def print_closed_trades(self):
        for ct in self.closed_trades:
            print(ct)
