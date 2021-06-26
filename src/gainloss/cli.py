import click
from tabulate import tabulate

from gainloss.pnl import TradeManager

from .conventions import HEADER_CLOSED


@click.command()
@click.option("--path", "-p", type=str, help="CSV file with trades.")
@click.option(
    "--print-trades",
    type=bool,
    default=False,
    show_default=True,
    help="Print trades matrix.",
)
def compute_pnl(path, print_trades):

    tm = TradeManager()

    tm.process_csv(path)

    if print_trades:
        print("\n")
        print(tm.trades)
        print("\n")

    closed = [str(trade).split(",") for trade in tm.closed_trades]

    print(tabulate(closed, headers=HEADER_CLOSED))

    print("\nPnL = {:.2f}".format(tm.pnl))
