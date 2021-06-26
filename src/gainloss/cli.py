import click
from tabulate import tabulate

from gainloss.pnl import TradeManager

from .conventions import HEADER_CLOSED


@click.command()
@click.option("--path", "-p", type=str)
def compute_pnl(path):

    tm = TradeManager()

    tm.process_csv(path)

    closed = [str(trade).split(",") for trade in tm.closed_trades]

    print(tabulate(closed, headers=HEADER_CLOSED))

    print("\nPnL = {:.2f}".format(tm.pnl))
